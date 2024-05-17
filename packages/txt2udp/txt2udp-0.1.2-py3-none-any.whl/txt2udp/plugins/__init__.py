import asyncio


class BasePlugin:
    input_queue: asyncio.Queue
    output_queue: asyncio.Queue
    plugin_config: dict[str, str]

    def __init__(
        self,
        input_queue: asyncio.Queue,
        output_queue: asyncio.Queue,
        plugin_config: dict[str, str],
    ):
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.plugin_config = plugin_config

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def worker(self):
        raise NotImplementedError
