# -*- coding: utf-8 -*-

__author__ = r'wsb310@gmail.com'

import typing
import asyncio
import grpc
import msgpack

from abc import abstractmethod

from ...extend.struct import RoundRobin
from ...extend.asyncio.base import Utils


CHANNEL_USABLE_STATE = (grpc.ChannelConnectivity.READY, grpc.ChannelConnectivity.IDLE)


class GRPCClient:

    def __init__(
            self, *,
            credentials: typing.Optional[grpc.ChannelCredentials] = None,
            options: typing.Optional[grpc.aio.ChannelArgumentType] = None,
            compression: typing.Optional[grpc.Compression] = None,
            interceptors: typing.Optional[typing.Sequence[grpc.aio.ClientInterceptor]] = None,
            request_serializer: typing.Optional[typing.Callable] = msgpack.dumps,
            response_deserializer: typing.Optional[typing.Callable] = msgpack.loads
    ):

        self._credentials: typing.Optional[grpc.ChannelCredentials] = credentials
        self._options: typing.Optional[grpc.aio.ChannelArgumentType] = options
        self._compression: typing.Optional[grpc.Compression] = compression
        self._interceptors: typing.Optional[typing.Sequence[grpc.aio.ClientInterceptor]] = interceptors

        self._request_serializer: typing.Optional[typing.Callable] = request_serializer
        self._response_deserializer: typing.Optional[typing.Callable] = response_deserializer

        self._channels: typing.Optional[RoundRobin[grpc.aio.Channel]] = None

    async def _make_channel(self, target: str) -> grpc.aio.Channel:

        if self._credentials is None:
            return grpc.aio.insecure_channel(
                target, self._options, self._compression, self._interceptors
            )
        else:
            return grpc.aio.secure_channel(
                target, self._credentials, self._options, self._compression, self._interceptors
            )

    async def open(self, targets: typing.List[str]):

        self._channels = RoundRobin(
            [await self._make_channel(target) for target in targets]
        )

    async def close(self):

        for channel in self._channels.data:
            await channel.close()

        self._channels = None

    def get_channel(self) -> grpc.aio.Channel:

        channel = None

        for _ in range(len(self._channels)):

            channel = self._channels.get()

            if channel.get_state() in CHANNEL_USABLE_STATE:
                break

        return channel

    def unary_unary(
            self, method: str, call_params: typing.Union[bytes, typing.Dict],
            *, timout: typing.Optional[float] = None, metadata: typing.Optional[grpc.aio.Metadata] = None
    ) -> grpc.aio.UnaryUnaryCall:

        channel = self.get_channel()

        return channel.unary_unary(
            method,
            request_serializer=self._request_serializer,
            response_deserializer=self._response_deserializer,
        )(call_params, timeout=timout, wait_for_ready=True, metadata=metadata)

    def unary_stream(
            self, method: str, call_params: typing.Union[bytes, typing.Dict],
            *, timout: typing.Optional[float] = None, metadata: typing.Optional[grpc.aio.Metadata] = None
    ) -> grpc.aio.UnaryStreamCall:

        channel = self.get_channel()

        return channel.unary_stream(
            method,
            request_serializer=self._request_serializer,
            response_deserializer=self._response_deserializer,
        )(call_params, timeout=timout, wait_for_ready=True, metadata=metadata)

    def stream_unary(
            self, method: str,
            *, timout: typing.Optional[float] = None, metadata: typing.Optional[grpc.aio.Metadata] = None
    ) -> grpc.aio.StreamUnaryCall:

        channel = self.get_channel()

        return channel.stream_unary(
            method,
            request_serializer=self._request_serializer,
            response_deserializer=self._response_deserializer,
        )(timeout=timout, wait_for_ready=True, metadata=metadata)

    def stream_stream(
            self, method: str,
            *, timout: typing.Optional[float] = None, metadata: typing.Optional[grpc.aio.Metadata] = None
    ) -> grpc.aio.StreamStreamCall:

        channel = self.get_channel()

        return channel.stream_stream(
            method,
            request_serializer=self._request_serializer,
            response_deserializer=self._response_deserializer,
        )(timeout=timout, wait_for_ready=True, metadata=metadata)


class RobustStreamClient:

    def __init__(self, client: GRPCClient, method: str):

        self._grpc_client: GRPCClient = client

        self._stream_method: str = method

        self._stream_stub: typing.Optional[grpc.aio.StreamStreamCall] = None
        self._stream_task: typing.Optional[asyncio.Task] = None

    async def _do_stream_task(self):

        try:
            async for _message in self._stream_stub:
                await self.on_message(_message)
        except Exception as err:
            Utils.log.error(str(err))

    async def join(self) -> typing.Any:
        return await self._stream_task

    async def connect(self, *, timout: typing.Optional[float] = None, metadata: typing.Optional[grpc.aio.Metadata] = None) -> bool:

        try:

            self.cancel()

            self._stream_stub = self._grpc_client.stream_stream(self._stream_method, timout=timout, metadata=metadata)
            self._stream_stub.add_done_callback(lambda _: Utils.create_task(self.on_disconnect()))

            await self.on_connect()

            self._stream_task = asyncio.create_task(self._do_stream_task())

            return True

        except Exception as err:

            Utils.log.error(str(err))

            return False

    def cancel(self):

        if self._stream_task is not None and not self._stream_task.done():
            self._stream_task.cancel()

        if self._stream_stub is not None and not self._stream_stub.done():
            self._stream_stub.cancel()

        self._stream_task = None
        self._stream_stub = None

    async def read(self) -> typing.Any:

        data = await self._stream_stub.read()

        if data != grpc.aio.EOF:
            return data
        else:
            raise ConnectionAbortedError()

    async def send(self, message: typing.Any):
        await self._stream_stub.write(message)

    @abstractmethod
    async def on_message(self, message: typing.Any):
        """
        接收消息回调
        """

    @abstractmethod
    async def on_connect(self):
        """
        与服务端通信连接成功后回调
        """

    @abstractmethod
    async def on_disconnect(self):
        """
        与服务端通信失去连接后回调
        """
