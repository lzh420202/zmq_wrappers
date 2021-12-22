from .zmq_base import zmq_server_base
from .message_hooks import recvDataHooks, recvMultipartDataHooks
from .server_function import server_payload


class zmq_data_server(zmq_server_base):
    def __init__(self, port: int):
        super(zmq_data_server, self).__init__(port, recvDataHooks, server_payload)


class zmq_multipart_data_server(zmq_server_base):
    def __init__(self, port: int):
        super(zmq_multipart_data_server, self).__init__(port, recvMultipartDataHooks, server_payload)


class zmq_server(zmq_server_base):
    def __init__(self, port: int, message_hooks=None, payload_hooks=None):
        if message_hooks is None:
            message_hooks = recvMultipartDataHooks
        if payload_hooks is None:
            payload_hooks = server_payload
        super(zmq_server, self).__init__(port, message_hooks, payload_hooks)