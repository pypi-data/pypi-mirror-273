import asyncio
import json
from pathlib import Path
from typing import Any, Callable, Coroutine, Protocol

import aiohttp
import websockets
from aiohttp import web

import relationalai

PROJECT_ROOT = Path(relationalai.__file__).resolve().parent.parent.parent
HTTP_DIST_DIR = PROJECT_ROOT / "frontend" / "debugger" / "dist"

#------------------------------------------------------------------------------
# Program Connections
#------------------------------------------------------------------------------

connected_program = None

async def handle_program(req: web.Request):
    ws = web.WebSocketResponse()
    await ws.prepare(req)

    global connected_program
    if connected_program:
        print("Refusing to connect to new program until previous one finishes.")
        await ws.close()

    connected_program = ws
    buffered_broadcasts.clear()
    print("Program connected")
    try:
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                await broadcast(msg.data)
            elif msg.type == aiohttp.WSMsgType.ERROR:
                err = ws.exception()
                if err:
                    raise err
            else:
                raise Exception("Unknown message type", msg.type)
    finally:
        print("Program disconnected")
        connected_program = None

    return ws

#------------------------------------------------------------------------------
# Browser Client Connections
#------------------------------------------------------------------------------

connected_clients: set[web.WebSocketResponse] = set()

async def handle_client_message(msg: Any, ws: web.WebSocketResponse):
    try:
        parsed = json.loads(msg)
    except json.JSONDecodeError as e:
        print("Got invalid json from client:", e)
        return

    action = client_actions.get(parsed["type"])
    if not action:
        print("Got action request from client for non-existent action of type", parsed["type"])
        return

    kwargs = {k: v for k, v in parsed.items() if k != 'type'}
    res = action(ws, **kwargs)
    if res:
        if asyncio.iscoroutine(res):
            res = await res

        await ws.send_json(res)

async def handle_client(req: web.Request):
    ws = web.WebSocketResponse()
    await ws.prepare(req)
    connected_clients.add(ws)
    try:
        for msg in buffered_broadcasts:
            await ws.send_str(msg)

        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                await handle_client_message(msg.data, ws)
            elif msg.type == aiohttp.WSMsgType.ERROR:
                err = ws.exception()
                if err:
                    raise err
            else:
                raise Exception("Unknown message type", msg.type)

    except websockets.exceptions.ConnectionClosed as e:
        print(f"Client disconnected with reason: {e}")
    finally:
        connected_clients.remove(ws)

    return ws

#------------------------------------------------------------------------------
# Browser Client Actions
#------------------------------------------------------------------------------

ClientActionReturn = Coroutine[Any, Any, dict|None]|dict|None

class ClientAction(Protocol):
    def __call__(self, ws: web.WebSocketResponse, **kwargs: Any) -> ClientActionReturn:
        ...

client_actions: dict[str, ClientAction] = {}

def client_action(name: str|None = None):
    def decorator(fn: Callable[..., ClientActionReturn]):
        client_actions[name or fn.__name__] = fn

    return decorator

@client_action()
def ping(_):
    print("Pinged!")
    return {"type": "pong"}

#------------------------------------------------------------------------------
# Event Log
#------------------------------------------------------------------------------

buffered_broadcasts = []

async def broadcast(message):
    buffered_broadcasts.append(message)
    if connected_clients:
        tasks = [asyncio.create_task(client.send_str(message)) for client in connected_clients]
        await asyncio.wait(tasks)

#------------------------------------------------------------------------------
# Server
#------------------------------------------------------------------------------

async def serve_index(_):
    return web.FileResponse(HTTP_DIST_DIR / "index.html")

runner: web.AppRunner|None = None
async def run_server(host: str, port: int):
    global runner
    if runner:
        await runner.shutdown()

    app = web.Application()
    app.router.add_get("/ws/program", handle_program)
    app.router.add_get("/ws/client", handle_client)
    app.router.add_get("/", serve_index)
    app.router.add_static("/", HTTP_DIST_DIR, show_index=False)  # Serving static files from DIR
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host, port)
    await site.start()

    print(f"Server started at http://{host}:{port}")

    return runner

def start_server(host: str, port: int):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_server(host, port))
    loop.run_forever()


def stop_server():
    global runner
    if not runner:
        return

    loop = asyncio.get_running_loop()
    loop.run_until_complete(broadcast(json.dumps({"event": "debug_server_closed"})))
    loop.run_until_complete(runner.shutdown())
    runner = None
