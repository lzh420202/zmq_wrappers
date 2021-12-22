import zmq
from queue import Queue
import time
import pickle
import math


def sendDataHooks(socket: zmq.Socket, message: dict, progress_bar_info=None):
    t = time.time()
    socket.send_pyobj(message)
    result = socket.recv_pyobj()
    return result


def recvDataHooks(socket: zmq.Socket, callback):
    while True:
        message = socket.recv_pyobj()
        if message:
            reply = callback(message)
        else:
            reply = None
        socket.send_pyobj(reply)


def sendMultipartDataHooks(socket: zmq.Socket, message: dict, progress_bar_info=None):
    if message.get('TEST') is not None:
        socket.send_string('START')
        _ = socket.recv()
        socket.send_string('1')
        _ = socket.recv()
        return dict(TEST='SUCCESS')
    else:
        message_bytes = pickle.dumps(message)
        split_n = 100
        min_block_size = 1 << 15 # 32kb
        max_block_size = 1 << 20 # 1024kb
        total = len(message_bytes)
        block_size = math.ceil(total / split_n)
        if block_size < min_block_size:
            split_n = max(1, math.floor(total / min_block_size))
            block_size = math.ceil(total / split_n)
        elif block_size > max_block_size:
            split_n = math.ceil(total / max_block_size)
            block_size = math.ceil(total / split_n)

        if progress_bar_info:
            assert isinstance(progress_bar_info, dict)
            progress_bar_info.update(dict(current=0, total=total, used_time=0))
        t = time.time()
        socket.send_string('START')
        _ = socket.recv()
        socket.send_string(f'{split_n}')
        _ = socket.recv()
        for i in range(split_n):
            msg = message_bytes[i*block_size:(i+1)*block_size]
            socket.send(msg)
            if progress_bar_info:
                current = min(block_size * (i + 1), total)
                progress_bar_info.update(dict(current=current, used_time=time.time() - t))
            _ = socket.recv()
        if progress_bar_info:
            progress_bar_info.update(dict(current=total, used_time=time.time() - t))
        socket.send_string('done')
        result = socket.recv_pyobj()
        return result


def recvMultipartDataHooks(socket: zmq.Socket, callback):
    renew = False
    while True:
        msg = b'ok'
        parts = []
        if renew:
            renew = False
        else:
            assert socket.recv_string() == 'START'
            socket.send(msg)

        n_str = socket.recv_string()
        n = int(n_str)
        socket.send(msg)
        for i in range(n):
            msg_recv = socket.recv()
            if len(msg_recv) == 5:
                if msg_recv == b'START':
                    renew = True
                    socket.send(msg)
                    break
            parts.append(msg_recv)
            socket.send(msg)
        if renew:
            continue
        _ = socket.recv_string()
        message = pickle.loads(b''.join(parts))
        if message:
            reply = callback(message)
        else:
            reply = None

        socket.send_pyobj(reply)