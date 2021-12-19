import zmq
import threading
from queue import Queue

class zmq_client_base(threading.Thread):
    def __init__(self, dst_ip: str, port: int, input_queue: Queue, output_queue: Queue, callback):
        threading.Thread.__init__(self)
        if callback is None:
            raise ValueError('callback can not be None.')
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.set(zmq.LINGER, 0)
        self.addr = f"tcp://{dst_ip}:{port}"
        self.callback = callback
        self.input_queue = input_queue
        self.output_queue = output_queue

    def sendMessage(self, message: dict):
        self.socket.connect(self.addr)
        result = self.callback(self.socket, message)
        self.socket.close()
        return result

    def run(self):
        while True:
            message = self.input_queue.get()
            if message:
                result = self.sendMessage(message)
                self.output_queue.put(result)
            else:
                break
        self.context.destroy()


class zmq_server_base(threading.Thread):
    def __init__(self, port: int, output_queue: Queue, callback):
        threading.Thread.__init__(self)
        if callback is None:
            raise ValueError('callback can not be None.')
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind(f"tcp://*:{port}")
        self.callback = callback
        self.output_queue = output_queue

    def close_server(self):
        self.socket.close()
        self.context.destroy()

    def listening(self):
        self.callback(self.socket, self.output_queue)

    def run(self):
        self.listening()