from msg.codec import decode
import asyncio
import threading
from websockify import WebSocketProxy
from lobby.loop import game_loop, handle_msg

HOST = "127.0.0.1"
PORT = 5555


async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    addr, port = writer.get_extra_info("peername")

    while True:
        data = await reader.read(1024)

        if not data:
            break

        msg = decode(data)
        print(f"got from {addr}:{port}: {msg}")

        handle_msg(writer, msg)

    writer.close()
    await writer.wait_closed()


def ws_front(port, host: str = "localhost", offset: int = 20000):
    import signal
    from types import FrameType
    from typing import Callable, Union

    def signal_signal(
        sig: int, proc: Union[Callable[[int, FrameType], None], int, None]
    ) -> Union[Callable[[int, FrameType], None], int, None]:
        print(f"STUB signal.signal({sig},{proc})")
        return proc

    signal.signal = signal_signal  # ty:ignore[invalid-assignment]

    proxy = WebSocketProxy(
        listen_port=port + offset,
        target_host=host,
        target_port=port,
        verbose=True,
        run_once=False,
        daemon=False,
    )
    print(f"Starting ws frontend on {host=}:{port=}+{offset=}={port + offset}")
    proxy.start_server()


ws_thread = threading.Thread(target=ws_front, args=(PORT,))
ws_thread.daemon = True
ws_thread.start()


async def main():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    print("Starting server...")

    asyncio.create_task(game_loop())

    async with server:
        print(f"Server started on {HOST}:{PORT}")
        await server.serve_forever()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
