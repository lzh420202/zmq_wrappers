from ..wrappers.zmq_server_wrappers import zmq_multipart_data_server

class custom_server():
    def __init__(self, port):
        self.server = zmq_multipart_data_server(port)
        self.server.start()