# coding=utf-8

import asyncio
import json
from typing import List, Dict

import websockets
from websockets import WebSocketClientProtocol


class InforeWss:

    def __init__(self, url: str) -> None:
        self.ws: WebSocketClientProtocol
        self.url = url

    async def __aenter__(self):
        await self.connect_to_server()
        return self

    async def __aexit__(self):
        await self.close()

    async def send_and_recv(self, data: dict):
        if not self.ws:
            raise ValueError("ws连接断开")
        await self.ws.send(json.dumps(data))
        msg_list: List[Dict] = []
        while True:
            try:
                response = await asyncio.wait_for(self.ws.recv(), timeout=1)
                msg = json.loads(response)
                msg_list.append(msg)
            except asyncio.TimeoutError:
                break
        return msg_list

    async def connect_to_server(self):
        try:
            self.ws = await websockets.connect(self.url)
        except Exception as e:
            raise ConnectionError(f"连接服务失败：{e}")

    async def close(self):
        if self.ws:
            await self.ws.close()
            self.ws = None


async def main():
    url = ""
    data = {}
    ws = InforeWss(url)
    await ws.connect_to_server()
    await ws.send_and_recv(data)


if __name__ == "__main__":
    asyncio.run(main())