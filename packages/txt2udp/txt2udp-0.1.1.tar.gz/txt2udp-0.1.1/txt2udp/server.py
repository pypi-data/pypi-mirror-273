from .conn import TXT2UDPConnection, ConnectionManager
from .datagram import TXT2UDPProtocol
from .messages import Message

from typing import Tuple
from loguru import logger
import asyncio


class TXT2UDPServer:
    remote_addr: Tuple[str, int]
    connections: ConnectionManager
    input_queue: asyncio.Queue
    output_queue: asyncio.Queue

    def __init__(
        self,
        input_queue: asyncio.Queue,
        output_queue: asyncio.Queue,
        remote_addr: Tuple[str, int],
    ):
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.remote_addr = remote_addr
        self.connections = ConnectionManager()

    async def __aenter__(self):
        logger.info(f"TXT2UDPServer started for {self.remote_addr}")
        await self.output_queue.put("<|txt2udp:start|>")
        asyncio.create_task(self.heartbeat())
        return self

    async def __aexit__(self, exc_type, exc, tb):
        for connection in self.connections:
            connection.transport.close()
        self.connections.reset()

    async def create_connection(self, conn_id: str) -> TXT2UDPConnection:

        async def handle_received_data(data: bytes, addr: Tuple[str, int]):
            message = Message(conn_id=conn_id)
            message.set_bytes(data)
            await self.output_queue.put(message.model_dump_json())

        loop = asyncio.get_event_loop()
        transport, _protocol = await loop.create_datagram_endpoint(
            lambda: TXT2UDPProtocol(handle_received_data),
            remote_addr=self.remote_addr,
        )
        connection = TXT2UDPConnection(transport, self.remote_addr, conn_id)
        self.connections.add_connection(connection)

        return connection

    async def worker(self):
        while True:
            text_message = await self.input_queue.get()

            if text_message in ["<|txt2udp:start|>", "<|txt2udp:heartbeat|>"]:
                logger.debug(f"Received heartbeat message: {text_message}")
                continue

            try:
                message = Message.model_validate_json(text_message)
            except Exception as e:
                logger.warning(f"Error parsing message: {text_message}")
                logger.opt(exception=True).debug("Error parsing message, traceback:")
                continue

            try:
                connection = self.connections.get_connection(message.conn_id)
                if not connection:
                    connection = await self.create_connection(message.conn_id)

                connection.send_data(message.get_bytes())
            except Exception as e:
                logger.warning(f"Error sending message")
                logger.opt(exception=True).debug("Error sending message, traceback:")
                continue

    async def heartbeat(self):
        while True:
            await asyncio.sleep(5)
            await self.output_queue.put("<|txt2udp:heartbeat|>")
