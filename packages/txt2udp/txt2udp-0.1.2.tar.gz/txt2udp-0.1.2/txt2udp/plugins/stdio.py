from . import BasePlugin

from loguru import logger
import platform
import asyncio
import sys

if platform.system() != "Windows":
    import termios
    import tty

    def disable_echo():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setcbreak(fd)
        return old_settings

    def enable_echo(old_settings):
        fd = sys.stdin.fileno()
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

else:
    logger.warning(
        "Stdio plugin has limited functionality on Windows, and will not disable echo automatically."
    )


class StdioPlugin(BasePlugin):

    async def worker(self):
        await asyncio.gather(self.output_worker(), self.input_worker())

    async def __aenter__(self):
        logger.info("Using stdio as input/output")
        if platform.system() != "Windows":
            self.old_settings = disable_echo()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if platform.system() != "Windows":
            enable_echo(self.old_settings)

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
