from . import BasePlugin

from loguru import logger
import asyncio
import sys


class StdioPlugin(BasePlugin):

    async def worker(self):
        await asyncio.gather(self.output_worker(), self.input_worker())

    async def __aenter__(self):
        logger.info("Using stdio as input/output")
        return self

    async def output_worker(self):
        while True:
            data = await self.output_queue.get()
            sys.stdout.write(data + "\r\n")
            sys.stdout.flush()

    async def input_worker(self):
        loop = asyncio.get_event_loop()
        while True:
            data = await loop.run_in_executor(None, sys.stdin.readline)
            await self.input_queue.put(data)


Plugin = StdioPlugin
