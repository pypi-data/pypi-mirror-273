from .conn import TXT2UDPConnection, ConnectionManager
from .datagram import TXT2UDPProtocol
from .messages import Message

from typing import Tuple
from loguru import logger
import asyncio


class TXT2UDPClient:
    local_addr: Tuple[str, int]
    connections: ConnectionManager
    transport: asyncio.DatagramTransport
    input_queue: asyncio.Queue
    output_queue: asyncio.Queue

    def __init__(
        self,
        input_queue: asyncio.Queue,
        output_queue: asyncio.Queue,
        local_addr: Tuple[str, int],
    ):
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.local_addr = local_addr
        self.connections = ConnectionManager()

    async def __aenter__(self):
        loop = asyncio.get_event_loop()
        self.transport, _protocol = await loop.create_datagram_endpoint(
            lambda: TXT2UDPProtocol(self.handle_received_data),
            local_addr=self.local_addr,
        )
        logger.info(f"TXT2UDPClient started on {self.local_addr}")
        await self.output_queue.put("<|txt2udp:start|>")
        asyncio.create_task(self.heartbeat())
        return self

    async def __aexit__(self, exc_type, exc, tb):
        self.transport.close()
        self.connections.reset()

    async def create_connection(self, addr: Tuple[str, int]) -> TXT2UDPConnection:
        connection = TXT2UDPConnection(self.transport, addr)
        self.connections.add_connection(connection, addr)
        return connection

    async def handle_received_data(self, data: bytes, addr: Tuple[str, int]):
        conn_id = self.connections.get_connection_id(addr)
        if not conn_id:
            conn_id = (await self.create_connection(addr)).conn_id
        message = Message(conn_id=conn_id)
        message.set_bytes(data)
        await self.output_queue.put(message.model_dump_json())

    async def worker(self):
        while True:
            text_message = await self.input_queue.get()

            if text_message in ["<|txt2udp:start|>", "<|txt2udp:heartbeat|>"]:
                logger.debug(f"Received heartbeat message: {text_message}")
                continue

            try:
                message = Message.model_validate_json(text_message)
            except Exception:
                logger.warning(f"Error parsing message: {text_message}")
                logger.opt(exception=True).debug("Error parsing message, traceback:")
                continue

            try:
                connection = self.connections.get_connection(message.conn_id)
                if connection:
                    connection.send_data(message.get_bytes())
                else:
                    logger.warning(f"Connection {message.conn_id} not found")
            except Exception:
                logger.warning(f"Error sending message")
                logger.opt(exception=True).debug("Error sending message, traceback:")
                continue

    async def heartbeat(self):
        while True:
            await asyncio.sleep(5)
            await self.output_queue.put("<|txt2udp:heartbeat|>")
