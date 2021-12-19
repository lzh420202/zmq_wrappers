import cv2
from zmq_server_wrappers import zmq_data_server, Queue, zmq_multipart_data_server
from threading import Thread
import os

class TestThread(Thread):
    def __init__(self, queue: Queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self) -> None:
        path = 'save'
        os.makedirs(os.path.realpath(path))
        while True:
            data = self.queue.get()
            if data:
                for k, v in data.items():
                    if k != 'image':
                        print(f'{k}: \t{v}')
                # cv2.imwrite(os.path.join(path, data['name']), data['image'])
            else:
                break


if __name__ == '__main__':
    port = 10000
    queue = Queue(10)
    server = zmq_multipart_data_server(port, queue)
    server.start()
    while True:
        data = queue.get()
        if data:
            for k, v in data.items():
                if k != 'image':
                    print(f'{k}: \t{v}')
            print('writing object into file.')
            print(f"Shape: {data['image'].shape}")
            cv2.imwrite(os.path.join('save', data['name']), data['image'])
        else:
            break

    server.join()