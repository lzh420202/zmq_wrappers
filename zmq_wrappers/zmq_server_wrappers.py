from .zmq_base import zmq_server_base
from .message_hooks import recvDataHooks, recvMultipartDataHooks
from queue import Queue


class zmq_data_server(zmq_server_base):
    def __init__(self, port: int, output_queue: Queue):
        super(zmq_data_server, self).__init__(port, output_queue, recvDataHooks)


class zmq_multipart_data_server(zmq_server_base):
    def __init__(self, port: int, output_queue: Queue):
        super(zmq_multipart_data_server, self).__init__(port, output_queue, recvMultipartDataHooks)