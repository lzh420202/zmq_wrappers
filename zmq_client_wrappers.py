from zmq_base import zmq_client_base
from queue import Queue
from message_hooks import sendDataHooks, sendMultipartDataHooks


class zmq_data_client(zmq_client_base):
    def __init__(self, dst_ip: str, port: int, input_queue: Queue, output_queue: Queue):
        super(zmq_data_client, self).__init__(dst_ip, port, input_queue, output_queue, sendDataHooks)

class zmq_multipart_data_client(zmq_client_base):
    def __init__(self, dst_ip: str, port: int, input_queue: Queue, output_queue: Queue):
        super(zmq_multipart_data_client, self).__init__(dst_ip, port, input_queue, output_queue, sendMultipartDataHooks)