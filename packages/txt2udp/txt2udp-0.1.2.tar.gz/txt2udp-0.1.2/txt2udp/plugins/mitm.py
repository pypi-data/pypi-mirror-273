from . import BasePlugin

from pydantic import BaseModel, Field
from typing import Optional
from loguru import logger
import asyncio
import json
import re

try:
    from mitmproxy import http, ctx, options
    from mitmproxy.tools.dump import DumpMaster
except ModuleNotFoundError as e:
    e.add_note(
        """Mitmproxy is required for this plugin.
        Please install it with `pip install mitmproxy` or `pip install txt2udp[mitm]`"""
    )
    raise e


class MitmPluginConfig(BaseModel):
    proxy_host: str = Field(default="127.0.0.1")
    proxy_port: int = Field(default=8080)
    url_filter: str = Field(
        default=r"https://aistudio\.baidu\.com/.*/terminals/websocket"
    )


class MitmPlugin(BasePlugin):
    _working_flow: Optional[http.HTTPFlow]
    mitmproxy: DumpMaster

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._working_flow = None
        self.config = MitmPluginConfig.model_validate_strings(self.plugin_config)

    async def __aenter__(self):
        opts = options.Options(
            listen_host=self.config.proxy_host, listen_port=self.config.proxy_port
        )
        self.mitmdump = DumpMaster(opts, with_termlog=False)
        self.mitmdump.addons.add(self)
        ctx.master.options.update(flow_detail=0)
        asyncio.create_task(self.mitmdump.run())

        logger.info("Using mitmproxy plugin as input/output")
        logger.info(
            f"Proxy server listening on {self.config.proxy_host}:{self.config.proxy_port}"
        )

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        logger.info("Shutting down mitmproxy")
        self.mitmdump.shutdown()

    async def worker(self):
        while True:
            data = await self.output_queue.get()

            if self._working_flow:
                ctx.master.commands.call(
                    "inject.websocket",
                    self._working_flow,
                    False,
                    json.dumps(["stdin", data + "\r\n"]).encode(),
                )

    async def websocket_message(self, flow: http.HTTPFlow):
        """Handle websocket messages"""
        assert flow.websocket is not None

        if not re.match(self.config.url_filter, flow.request.url):
            return

        last_message = flow.websocket.messages[-1]

        # Ignore injected messages
        if last_message.injected:
            return

        # Ignore non-text messages
        if not last_message.is_text:
            return

        # Parse JSON
        try:
            json_obj = json.loads(last_message.text)
            message_type, message_text = json_obj
            message_text = message_text.strip()
        except json.JSONDecodeError:
            logger.warning("Failed to parse JSON. Ignoring message")
            return

        # Set working flow
        if (
            not last_message.from_client
            and message_type == "stdout"
            and message_text in ["<|txt2udp:start|>", "<|txt2udp:heartbeat|>"]
            and self._working_flow != flow
        ):
            logger.debug("Setting working flow")
            self._working_flow = flow

        if self._working_flow != flow:
            return

        # Handle messages
        if not last_message.from_client:
            # Handle stdout
            if message_type == "stdout":
                await self.input_queue.put(message_text)
        elif message_type == "stdin" and message_text == "\u0003":
            # Stop terminal
            self._working_flow = None
            return

        # Drop message
        last_message.drop()


Plugin = MitmPlugin
