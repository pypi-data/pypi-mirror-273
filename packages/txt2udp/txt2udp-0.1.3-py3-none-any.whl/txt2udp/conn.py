from typing import Optional, Tuple, Dict
from loguru import logger
from uuid import uuid4
import asyncio


class TXT2UDPConnection:
    conn_id: str
    transport: asyncio.DatagramTransport
    remote_addr: Optional[Tuple[str, int]]

    def __init__(
        self,
        transport: asyncio.DatagramTransport,
        remote_addr: Optional[Tuple[str, int]] = None,
        conn_id: Optional[str] = None,
    ):
        self.transport = transport
        self.remote_addr = remote_addr

        if not conn_id:
            conn_id = str(uuid4())

        self.conn_id = conn_id

    def send_data(self, data: bytes):
        logger.debug(f"Sending {len(data)} bytes to {self.remote_addr}")
        self.transport.sendto(data, self.remote_addr)


class ConnectionManager:
    connections: Dict[str, TXT2UDPConnection]
    addr_to_id: Dict[Tuple[str, int], str]

    def __init__(self):
        self.connections = {}
        self.addr_to_id = {}

    def __iter__(self):
        return iter(self.connections.values())

    def get_connection(self, conn_id: str) -> Optional[TXT2UDPConnection]:
        return self.connections.get(conn_id)

    def get_connection_id(self, addr: Tuple[str, int]) -> Optional[str]:
        return self.addr_to_id.get(addr)

    def get_connection_by_addr(
        self, addr: Tuple[str, int]
    ) -> Optional[TXT2UDPConnection]:
        conn_id = self.get_connection_id(addr)
        if conn_id:
            return self.get_connection(conn_id)

    def add_connection(
        self, conn: TXT2UDPConnection, addr: Optional[Tuple[str, int]] = None
    ):
        self.connections[conn.conn_id] = conn

        if addr:
            self.addr_to_id[addr] = conn.conn_id

    def reset(self):
        self.connections = {}
        self.addr_to_id = {}
