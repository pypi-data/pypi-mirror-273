import asyncio
import logging
import os
import threading
import websockets
import queue
from relationalai import debugging
import __main__ # to get the users root file path

#------------------------------------------------------------------------------
# Logging Handler
#------------------------------------------------------------------------------

class WebSocketLoggingHandler(logging.Handler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from relationalai.analysis.mechanistic import Mechanism
        self.Mechanism = Mechanism
        self.queue: queue.Queue[str] = queue.Queue()

    def start(self, url: str):
        main_path = getattr(__main__, "__file__", None)
        program_span = debugging.span_start("program",  main=os.path.relpath(main_path) if main_path else "notebook")
        self.thread = threading.Thread(target=self.connect, args=(url, program_span))
        self.thread.start()

    def emit(self, record):
        d = record.msg
        if (isinstance(d, dict) and
            d["event"] == "span_start" and
            "task" in d["span"].attrs and
            "mech" not in d["span"].attrs):
            d["span"].attrs["mech"] = self.Mechanism(d["span"].attrs["task"])
        log_entry = self.format(record)
        self.queue.put_nowait(log_entry)

    def connect(self, url: str, span: debugging.Span):
        print(f"Connecting to {url}...")
        try:
            try:
                loop = asyncio.get_running_loop()
                loop.run_until_complete(self.connect_async(url, span))
            except RuntimeError:
                asyncio.run(self.connect_async(url, span))
        except (ConnectionRefusedError, websockets.WebSocketException, OSError, asyncio.TimeoutError):
            print(f"Failed to connect to {url}. Running with debug sink disabled.")

    async def connect_async(self, url: str, span: debugging.Span):
        async with websockets.connect(url) as ws:
            print("Connected.")
            while True:
                if not threading.main_thread().is_alive():
                    debugging.span_end(span)
                    log_entry = self.queue.get(timeout=1)
                    await ws.send(log_entry)
                    break

                try:
                    log_entry = self.queue.get(timeout=1)
                    await ws.send(log_entry)
                except queue.Empty:
                    pass
                except websockets.ConnectionClosedError:
                    break

#------------------------------------------------------------------------------
# Enable debugging
#------------------------------------------------------------------------------

already_debugging = False
def start_debugger_session(host = "0.0.0.0", port = 8080):
    global already_debugging
    if already_debugging:
        return

    ws_handler = WebSocketLoggingHandler()
    ws_handler.setFormatter(debugging.JsonFormatter())
    debugging.logger.addHandler(ws_handler)
    ws_handler.start(f"ws://{host}:{port}/ws/program")

    already_debugging = True
