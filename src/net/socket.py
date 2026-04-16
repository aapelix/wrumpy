import sys
from msg.codec import decode, encode
import msg.messages
import asyncio
import socket


async def run(
    host: str,
    port: int,
    socket_in: asyncio.Queue[msg.messages.Message],
    socket_out: asyncio.Queue[msg.messages.Message],
):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)

    connected = False
    while not connected:
        print(f"connecting to {host}:{port}...")

        if sys.platform == "emscripten":
            try:
                sock.connect((host, port))
                print(f"connected to {host}:{port}")
            except BlockingIOError:
                pass
            except OSError as e:
                if e.errno in (30, 106):
                    print(f"connected to {host}:{port}")
                    connected = True
        else:
            try:
                await asyncio.get_event_loop().sock_connect(sock, (host, port))
                print(f"connected to {host}:{port}")
                connected = True
            except ConnectionRefusedError:
                pass

        await asyncio.sleep(0)

    await asyncio.sleep(0)

    buffer = ""

    while True:
        try:
            data = sock.recv(1024)
            if data:
                buffer += data.decode("utf-8")

                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    if line.strip():
                        await socket_in.put(decode(line))
            else:
                raise Exception("socket closed")

        except BlockingIOError:
            pass

        try:
            msg = socket_out.get_nowait()
            sock.send(encode(msg))

        except asyncio.QueueEmpty:
            pass

        await asyncio.sleep(0)
