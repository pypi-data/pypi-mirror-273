from pydantic import BaseModel
from typing import Optional
import base64


class Message(BaseModel):
    conn_id: str
    data: Optional[str] = None

    def get_bytes(self):
        return base64.b64decode(self.data)

    def set_bytes(self, data: bytes):
        self.data = base64.b64encode(data).decode("utf-8")
