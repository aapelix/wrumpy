import asyncio
from msg.messages import Message
from asyncio import Queue
import net.socket

send: Queue[Message]
socket_in: Queue[Message]


def run(host, port):
    global send, socket_in

    socket_in = Queue()
    send = Queue()

    asyncio.create_task(net.socket.run(host, port, socket_in, send))
