# -*- coding: utf-8 -*-

__author__ = r'wsb310@gmail.com'

import os
import typing
import socket
import asyncio
import contextlib
import contextvars

import grpc

from .server import GRPCServer, Router
from .server import UNARY_UNARY_MODE, UNARY_STREAM_MODE, STREAM_UNARY_MODE, STREAM_STREAM_MODE
from .client import GRPCClient

from ...extend.asyncio.base import Utils
from ...extend.asyncio.command import MainProcess, SubProcess


GRPC_UDS_ENTRYPOINT = r'/tmp/grpc_balance_{}.sock'


@contextlib.contextmanager
def grpc_context(
        client_peer: str,
        server_stream_stub: typing.Union[grpc.aio.UnaryStreamCall, grpc.aio.StreamStreamCall] = None
):

    try:
        Utils.log.info(f'create connection: {client_peer}')
        yield
    except grpc.aio.UsageError:
        pass
    except Exception as err:
        Utils.log.error(str(err))
    finally:
        if server_stream_stub is not None:
            server_stream_stub.cancel()
        Utils.log.info(f'closed connection: {client_peer}')


class ProxyUnaryStream:

    def __init__(self, server_proxy: GRPCClient, server_method: str, client_request: bytes, client_context: grpc.aio.ServicerContext):

        self._server_proxy: GRPCClient = server_proxy
        self._server_stream_stub: grpc.aio.UnaryStreamCall = self._server_proxy.unary_stream(server_method, client_request)

        self._client_context: grpc.aio.ServicerContext = client_context

        self._stream_task: asyncio.Task = asyncio.create_task(self._do_stream_task())

    async def _do_stream_task(self):

        with grpc_context(self._client_context.peer(), self._server_stream_stub):
            async for _message in self._server_stream_stub:
                await self._client_context.write(_message)

    async def join(self) -> typing.Any:
        return await self._stream_task


class ProxyStreamUnary:

    def __init__(self, server_proxy: GRPCClient, server_method: str, client_request: typing.AsyncIterator, client_context: grpc.aio.ServicerContext):

        self._server_proxy: GRPCClient = server_proxy
        self._server_stream_stub: grpc.aio.StreamUnaryCall = self._server_proxy.stream_unary(server_method)

        self._client_request: typing.AsyncIterator = client_request
        self._client_context: grpc.aio.ServicerContext = client_context

        self._stream_task: asyncio.Task = asyncio.create_task(self._do_stream_task())

    async def _do_stream_task(self):

        with grpc_context(self._client_context.peer()):
            async for _message in self._client_request:
                await self._server_stream_stub.write(_message)

    async def join(self) -> typing.Any:
        return await self._server_stream_stub


class ProxyStreamStream:

    def __init__(self, server_proxy: GRPCClient, server_method: str, client_request: typing.AsyncIterator, client_context: grpc.aio.ServicerContext):

        self._server_proxy: GRPCClient = server_proxy
        self._server_stream_stub: grpc.aio.StreamStreamCall = self._server_proxy.stream_stream(server_method)

        self._client_request: typing.AsyncIterator = client_request
        self._client_context: grpc.aio.ServicerContext = client_context

        self._stream_task: asyncio.Task = asyncio.create_task(self._do_stream_task())

    async def _read_upstream(self) -> bytes:

        try:
            return await anext(self._client_request)
        except StopAsyncIteration:
            pass
        except Exception as err:
            Utils.log.error(f'read upstream error: {str(err)}')
            raise asyncio.CancelledError()

    async def _read_downstream(self) -> bytes:

        try:
            return await self._server_stream_stub.read()
        except Exception as err:
            Utils.log.error(f'read downstream error: {str(err)}')
            raise asyncio.CancelledError()

    async def _do_stream_task(self):

        with grpc_context(self._client_context.peer(), self._server_stream_stub):

            upstream_task = asyncio.create_task(self._read_upstream())
            downstream_task = asyncio.create_task(self._read_downstream())

            while True:

                _tasks_done, _ = await asyncio.wait(
                    [upstream_task, downstream_task],
                    return_when=asyncio.FIRST_COMPLETED
                )

                for _task in _tasks_done:

                    _message = await _task

                    if _task is upstream_task:
                        await self._server_stream_stub.write(_message)
                        upstream_task = asyncio.create_task(self._read_upstream())
                    elif _task is downstream_task:
                        await self._client_context.write(_message)
                        downstream_task = asyncio.create_task(self._read_downstream())

    async def join(self) -> typing.Any:
        return await self._stream_task


class ProxyInterceptor(grpc.aio.ServerInterceptor):

    def __init__(self, client: GRPCClient, routers: typing.List[Router]):

        self._method_context: contextvars.ContextVar = contextvars.ContextVar[str](r'grpc_method_context', default=None)

        self._client: GRPCClient = client

        self._handlers: typing.Dict[str, grpc.RpcMethodHandler] = {}

        self._init_handlers(routers)

    def _init_handlers(self, routers: typing.List[Router]):

        for router in routers:

            _service = router.service

            for _func, _mode in router.handlers:

                _method = f'/{_service}/{_func.__name__}'

                if _mode is UNARY_UNARY_MODE:
                    self._handlers[_method] = grpc.unary_unary_rpc_method_handler(self._unary_unary_handler)
                elif _mode is UNARY_STREAM_MODE:
                    self._handlers[_method] = grpc.unary_stream_rpc_method_handler(self._unary_stream_handler)
                elif _mode is STREAM_UNARY_MODE:
                    self._handlers[_method] = grpc.stream_unary_rpc_method_handler(self._stream_unary_handler)
                elif _mode is STREAM_STREAM_MODE:
                    self._handlers[_method] = grpc.stream_stream_rpc_method_handler(self._stream_stream_handler)

    async def _unary_unary_handler(self, request: bytes, _: grpc.aio.ServicerContext) -> typing.Any:

        method = self._method_context.get()

        return await self._client.unary_unary(method, request)

    async def _unary_stream_handler(self, request: bytes, context: grpc.aio.ServicerContext) -> typing.Any:

        method = self._method_context.get()

        return await ProxyUnaryStream(self._client, method, request, context).join()

    async def _stream_unary_handler(self, request: typing.AsyncIterator, context: grpc.aio.ServicerContext) -> typing.Any:

        method = self._method_context.get()

        return await ProxyStreamUnary(self._client, method, request, context).join()

    async def _stream_stream_handler(self, request: typing.AsyncIterator, context: grpc.aio.ServicerContext) -> typing.Any:

        method = self._method_context.get()

        return await ProxyStreamStream(self._client, method, request, context).join()

    async def intercept_service(
            self,
            continuation: typing.Callable[[grpc.HandlerCallDetails], typing.Awaitable[grpc.RpcMethodHandler]],
            handler_call_details: grpc.HandlerCallDetails
    ) -> grpc.RpcMethodHandler:

        method = getattr(handler_call_details, r'method')

        self._method_context.set(method)

        return self._handlers.get(method)


class GRPCProxy:

    def __init__(
            self, address: typing.Union[str, typing.Tuple[str, int]], routers: typing.List[Router],
            grpc_family: int = socket.AF_INET, grpc_server_credentials: typing.Optional[grpc.ServerCredentials] = None
    ):

        self._routers: typing.List[Router] = routers

        self._grpc_client: typing.Optional[GRPCClient] = None
        self._grpc_server: typing.Optional[GRPCServer] = None

        self._grpc_address: typing.Union[str, typing.Tuple[str, int]] = address
        self._grpc_family: int = grpc_family
        self._grpc_server_credentials: typing.Optional[grpc.ServerCredentials] = grpc_server_credentials

    async def open(self, targets: typing.List[str]):

        self._grpc_client: GRPCClient = GRPCClient(
            request_serializer=None,
            response_deserializer=None
        )

        await self._grpc_client.open(targets)

        self._grpc_server: GRPCServer = GRPCServer(
            interceptors=[ProxyInterceptor(self._grpc_client, self._routers)],
            request_deserializer=None,
            response_serializer=None
        )

        await self._grpc_server.start(self._grpc_address, self._grpc_family, self._grpc_server_credentials)

    async def close(self):

        await self._grpc_server.stop()
        await self._grpc_client.close()


class GRPCMainProcess(MainProcess):

    def __init__(
            self, address: typing.Union[str, typing.Tuple[str, int]], routers: typing.List[Router],
            worker: typing.Type[r'GRPCWorker'], sub_process_num: int, *,
            grpc_family: int = socket.AF_INET, grpc_server_credentials: typing.Optional[grpc.ServerCredentials] = None,
            cpu_affinity: bool = False, join_timeout: int = 10
    ):

        super().__init__(
            worker.create, sub_process_num,
            cpu_affinity=cpu_affinity, join_timeout=join_timeout,
            routers=routers
        )

        self._grpc_proxy: GRPCProxy = GRPCProxy(address, routers, grpc_family, grpc_server_credentials)

    async def initialize(self):
        await self._grpc_proxy.open(
            [
                f'unix:{GRPC_UDS_ENTRYPOINT.format(_idx)}'
                for _idx in range(self._sub_process_num)
            ]
        )

    async def release(self):
        await self._grpc_proxy.close()


class GRPCWorker(SubProcess):

    def __init__(self, process_num: int, routers: typing.List[Router]):

        super().__init__(process_num)

        self._grpc_server: typing.Optional[GRPCServer] = None
        self._grpc_routers: typing.List[Router] = routers

    def close(self, *_):
        Utils.call_soon(self._grpc_server.stop)

    async def _execute(self):

        grpc_uds_entrypoint = GRPC_UDS_ENTRYPOINT.format(self._process_num)

        if os.path.exists(grpc_uds_entrypoint):
            os.remove(grpc_uds_entrypoint)

        self._grpc_server = GRPCServer()

        for _router in self._grpc_routers:
            self._grpc_server.bind_router(_router)

        await self._grpc_server.start(grpc_uds_entrypoint, family=socket.AF_UNIX)
        await self._grpc_server.wait()
