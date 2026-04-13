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
        try:
            sock.connect((host, port))
        except BlockingIOError:
            pass
        except OSError as e:
            if e.errno in (30, 106):
                print(f"connected to {host}:{port}")
                connected = True

        await asyncio.sleep(0)

    await asyncio.sleep(0)

    while True:
        try:
            data = sock.recv(1024)
            if data:
                await socket_in.put(decode(data))
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
