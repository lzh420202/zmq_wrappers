import queue
from ..wrappers.zmq_client_wrappers import zmq_multipart_data_client, monitorThread

class custom_client():
    def __init__(self, ip, port, with_monitor=False):
        self.input_queue = queue.Queue(10)
        if with_monitor:
            self.process_info = dict(current=0, total=0, used_time=0)
        else:
            self.process_info = None
        self.client = zmq_multipart_data_client(ip, port, self.input_queue, self.process_info)
        self.client.start()
        if with_monitor:
            self.monitor = monitorThread(self.process_info, 0.1)
            self.monitor.start()
        else:
            self.monitor = None

    def sendData(self, data):
        self.input_queue.put(data)

    def testServer(self):
        self.input_queue.put(dict(TEST=True))
