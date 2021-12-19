import cv2
import zmq
from queue import Queue
import time
import pickle
import math


def sendDataHooks(socket: zmq.Socket, message: dict):
    t = time.time()
    socket.send_pyobj(message)
    result = socket.recv_string()
    print(result)
    print(f'{time.time() - t: .2f} s')


def recvDataHooks(socket: zmq.Socket, output_queue: Queue):
    while True:
        message = socket.recv_pyobj()
        if message:
            output_queue.put(message)
        socket.send_string('pass')


def sendMultipartDataHooks(socket: zmq.Socket, message: dict):
    t = time.time()
    message_bytes = pickle.dumps(message)
    split_n = 100
    min_block_size = 1 << 15
    max_block_size = 1 << 20
    block_size = math.ceil(len(message_bytes) / split_n)
    split_message = [message_bytes[i*block_size:(i+1)*block_size] for i in range(split_n)]

    for msg in split_message[:-1]:
        socket.send(msg, zmq.SNDMORE | 0)
    socket.send(split_message[-1], 0)

    result = socket.recv_string()
    print(result)
    print(f'{time.time() - t: .2f} s')


def recvMultipartDataHooks(socket: zmq.Socket, output_queue: Queue):
    while True:
        parts = [socket.recv()]
        # have first part already, only loop while more to receive
        while socket.getsockopt(zmq.RCVMORE):
            part = socket.recv()
            parts.append(part)
        message = pickle.loads(b''.join(parts))
        if message:
            output_queue.put(message)
        socket.send_string('pass')