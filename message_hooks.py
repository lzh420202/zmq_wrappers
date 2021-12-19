import zmq
from queue import Queue
import time
import pickle
import math


def sendDataHooks(socket: zmq.Socket, message: dict, progress_bar_info=None):
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


def sendMultipartDataHooks(socket: zmq.Socket, message: dict, progress_bar_info=None):
    message_bytes = pickle.dumps(message)
    split_n = 100
    min_block_size = 1 << 15 # 32kb
    max_block_size = 1 << 20 # 1024kb
    total = len(message_bytes)
    block_size = math.ceil(total / split_n)
    if block_size < min_block_size:
        split_n = math.floor(total / min_block_size)
        block_size = min_block_size
    elif block_size > max_block_size:
        split_n = math.ceil(total / max_block_size)
        block_size = max_block_size

    if progress_bar_info:
        assert isinstance(progress_bar_info, dict)
        progress_bar_info.update(dict(current=0, total=total, used_time=0))
    t = time.time()
    socket.send_string(f'{split_n}')
    _ = socket.recv()
    for i in range(split_n):
        msg = message_bytes[i*block_size:(i+1)*block_size]
        # socket.send(msg, zmq.SNDMORE | 0)
        socket.send(msg)
        if progress_bar_info:
            current = min(block_size * (i + 1), total)
            progress_bar_info.update(dict(current=current, used_time=time.time() - t))
        _ = socket.recv()
    # socket.send(message_bytes[(split_n - 1) * block_size: split_n * block_size])
    if progress_bar_info:
        progress_bar_info.update(dict(current=total, used_time=time.time() - t))
    socket.send_string('done')
    # progress_bar_info.update(dict(current=0, total=0, used_time=0))
    result = socket.recv_string()


def recvMultipartDataHooks(socket: zmq.Socket, output_queue: Queue):
    # while True:
    #     parts = [socket.recv()]
    #     # have first part already, only loop while more to receive
    #     while socket.getsockopt(zmq.RCVMORE):
    #         part = socket.recv()
    #         parts.append(part)
    #     message = pickle.loads(b''.join(parts))
    #     if message:
    #         output_queue.put(message)
    #     socket.send_string('pass')
    while True:
        msg = b'ok'
        parts = []
        n_str = socket.recv_string()
        n = int(n_str)
        socket.send(msg)
        for i in range(n):
            parts.append(socket.recv())
            socket.send(msg)
        _ = socket.recv_string()
        # while True:
        #     part = socket.recv()
        #     parts.append(part)
        message = pickle.loads(b''.join(parts))
        if message:
            output_queue.put(message)
        socket.send_string('pass')