import time

from .zmq_base import zmq_client_base
from queue import Queue
from .message_hooks import sendDataHooks, sendMultipartDataHooks
from .client_function import client_payload
from threading import Thread
import copy


class zmq_data_client(zmq_client_base):
    def __init__(self, dst_ip: str, port: int, input_queue: Queue):
        super(zmq_data_client, self).__init__(dst_ip, port, input_queue, sendDataHooks, client_payload)


class zmq_multipart_data_client(zmq_client_base):
    def __init__(self, dst_ip: str, port: int, input_queue: Queue, progressbar=None):
        super(zmq_multipart_data_client, self).__init__(dst_ip, port, input_queue, sendMultipartDataHooks, client_payload)
        self.progressbar = progressbar

class zmq_client(zmq_client_base):
    def __init__(self, dst_ip: str, port: int, input_queue: Queue, message_callback=None, function_callback=None, progressbar=None):
        if message_callback is None:
            message_callback = sendMultipartDataHooks
        if function_callback is None:
            function_callback = client_payload
        super(zmq_client, self).__init__(dst_ip, port, input_queue, message_callback, function_callback)
        self.progressbar = progressbar


class monitorThread(Thread):
    def __init__(self, variate, interval_time=0.1):
        Thread.__init__(self)
        self.variate = variate
        self.interval_time = interval_time
        self.bar_width = 50

    def run(self) -> None:
        space = '\033[42m{}\033[0m'
        while True:
            if self.variate:
                if self.variate['total'] > 0:
                    stat_copy = copy.deepcopy(self.variate)
                    if stat_copy['used_time'] == 0:
                        continue
                    rate = stat_copy['current'] / stat_copy['total']
                    bar_length = min(self.bar_width, round(rate * self.bar_width))
                    process = space.format(''.ljust(bar_length))
                    # if bar_length < self.bar_width:
                    process = process.ljust(self.bar_width + 9)
                    speed = stat_copy['current'] / ((1 << 20) * stat_copy['used_time'])
                    bar = "\r" + f"{rate: 5.0%} {process} " \
                                 f"{stat_copy['current']/(1<<20):.1f}/{stat_copy['total']/(1<<20):.1f}MB " \
                                 f"{speed: 5.2f}MB/s " \
                                 f"{stat_copy['used_time']: .1f}s"
                    print(bar, end='', flush=True)
                    if stat_copy['current'] == stat_copy['total']:
                        self.variate.update(dict(current=0, total=0, used_time=0))
                        print('')
            time.sleep(self.interval_time)

