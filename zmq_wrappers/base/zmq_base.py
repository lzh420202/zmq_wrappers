import zmq
from threading import Thread
from queue import Queue

class zmq_client_base(Thread):
    def __init__(self, dst_ip: str, port: int, input_queue: Queue, message_callback, function_callback):
        Thread.__init__(self)
        if message_callback is None:
            raise ValueError('message callback can not be None.')
        if function_callback is None:
            raise ValueError('function callback can not be None.')
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.set(zmq.LINGER, 0)
        self.addr = f"tcp://{dst_ip}:{port}"
        self.message_callback = message_callback
        self.function_callback = function_callback
        self.input_queue = input_queue
        self.progressbar = None

    def sendMessage(self, message: dict):
        self.socket.connect(self.addr)
        result = self.message_callback(self.socket, message, self.progressbar)
        self.socket.disconnect(self.addr)
        return result

    def run(self):
        while True:
            message = self.input_queue.get()
            if message:
                result = self.sendMessage(message)
                self.function_callback(result)
                # self.output_queue.put(result)
            else:
                break
        self.context.destroy()


class zmq_server_base(Thread):
    def __init__(self, port: int, message_callback, function_callback):
        Thread.__init__(self)
        if message_callback is None:
            raise ValueError('message callback can not be None.')
        if function_callback is None:
            raise ValueError('function callback can not be None.')
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind(f"tcp://*:{port}")
        self.message_callback = message_callback
        self.function_callback = function_callback

    def close_server(self):
        self.socket.close()
        self.context.destroy()

    def listening(self):
        self.message_callback(self.socket, self.function_callback)

    def run(self):
        self.listening()