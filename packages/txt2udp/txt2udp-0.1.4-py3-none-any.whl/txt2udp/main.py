from .server import TXT2UDPServer
from .client import TXT2UDPClient
from .plugins import BasePlugin
from .config import TXT2UDPMode, config

from loguru import logger
from typing import Tuple, Type
import importlib
import asyncio


def get_plugin(plugin_name: str) -> Type[BasePlugin]:
    try:
        module = importlib.import_module(f".plugins.{plugin_name}", "txt2udp")
    except ModuleNotFoundError:
        module = importlib.import_module(plugin_name)

    return module.Plugin


def set_logger(log_dir: str, log_level: str):
    logger.remove()
    logger.add(
        f"{log_dir}/txt2udp.log", rotation="1 day", retention="7 days", level=log_level
    )


async def run_txt2udp(
    mode: TXT2UDPMode,
    addr: Tuple[str, int],
    plugin_name: str,
    plugin_args: dict[str, str],
):

    input_queue = asyncio.Queue()
    output_queue = asyncio.Queue()

    Plugin = get_plugin(plugin_name)

    if mode == TXT2UDPMode.server:
        Txt2Udp = TXT2UDPServer
    else:
        Txt2Udp = TXT2UDPClient

    async with Txt2Udp(input_queue, output_queue, addr) as txt2udp:
        async with Plugin(input_queue, output_queue, plugin_args) as plugin:
            await asyncio.gather(txt2udp.worker(), plugin.worker())


def main():
    set_logger(config.log_dir, config.log_level)
    asyncio.run(
        run_txt2udp(
            config.mode,
            (config.host, config.port),
            config.plugin,
            config.get_plugin_args(),
        )
    )


if __name__ == "__main__":
    main()
