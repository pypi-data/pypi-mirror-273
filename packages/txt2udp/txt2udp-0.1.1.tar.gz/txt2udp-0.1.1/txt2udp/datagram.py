from typing import Callable, Awaitable, Tuple
from loguru import logger
import asyncio


class TXT2UDPProtocol(asyncio.DatagramProtocol):
    transport: asyncio.DatagramTransport
    received_callback: Callable[[bytes, Tuple[str, int]], Awaitable[None]]

    def __init__(
        self, received_callback: Callable[[bytes, Tuple[str, int]], Awaitable[None]]
    ):
        self.received_callback = received_callback
        super().__init__()

    def connection_made(self, transport):
        self.transport = transport
        logger.debug(
            f"UDP connection made, local address: {transport.get_extra_info('sockname')}"
        )

    def datagram_received(self, data: bytes, addr: tuple[str, int]):
        try:
            logger.debug(f"Received {len(data)} bytes from {addr}")
            asyncio.create_task(self.received_callback(data, addr))
        except Exception:
            logger.exception("Error handling received data:")
