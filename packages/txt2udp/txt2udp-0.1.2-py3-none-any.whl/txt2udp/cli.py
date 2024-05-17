from .config import TXT2UDPMode, config, parse_args
from .main import run_txt2udp, set_logger, main

from typing_extensions import Annotated
from typing import Tuple
import asyncio

try:
    import typer
except ModuleNotFoundError as e:
    e.add_note(
        """Typer is required for command line interface.
        Please install it with `pip install typer` or `pip install txt2udp[cli]`"""
    )
    raise e

app = typer.Typer()


def parse_plugin(plugin: str) -> Tuple[str, dict[str, str]]:
    if ":" in plugin:
        plugin_name, plugin_args_str = plugin.split(":", 1)
        plugin_args = parse_args(plugin_args_str)
    else:
        plugin_name = plugin
        plugin_args = {}
    return plugin_name, plugin_args


@app.command("server")
def server(
    remote_host: Annotated[str, typer.Option("--remote-host", "-h")] = config.host,
    remote_port: Annotated[int, typer.Option("--remote-port", "-p")] = config.port,
    plugin: Annotated[str, typer.Option("--plugin", "-P")] = config.plugin,
    log_dir: Annotated[str, typer.Option("--log-dir", "-l")] = config.log_dir,
    log_level: Annotated[str, typer.Option("--log-level", "-L")] = config.log_level,
):
    plugin_name, plugin_args = parse_plugin(plugin)
    set_logger(log_dir, log_level)
    asyncio.run(
        run_txt2udp(
            TXT2UDPMode.server, (remote_host, remote_port), plugin_name, plugin_args
        )
    )


@app.command("client")
def client(
    local_host: Annotated[str, typer.Option("--local-host", "-h")] = config.host,
    local_port: Annotated[int, typer.Option("--local-port", "-p")] = config.port,
    plugin: Annotated[str, typer.Option("--plugin", "-P")] = config.plugin,
    log_dir: Annotated[str, typer.Option("--log-dir", "-l")] = config.log_dir,
    log_level: Annotated[str, typer.Option("--log-level", "-L")] = config.log_level,
):
    plugin_name, plugin_args = parse_plugin(plugin)
    set_logger(log_dir, log_level)
    asyncio.run(
        run_txt2udp(
            TXT2UDPMode.client, (local_host, local_port), plugin_name, plugin_args
        )
    )


@app.command()
def run():
    main()


if __name__ == "__main__":
    app()
