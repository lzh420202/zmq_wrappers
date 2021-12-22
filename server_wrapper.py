from queue import Queue
from zmq_wrappers.zmq_server_wrappers import zmq_multipart_data_server
import cv2
import os

class custom_server():
    def __init__(self, port):
        # self.output_queue = Queue(10)
        self.server = zmq_multipart_data_server(port)
        self.server.start()

    # def getData(self):
    #     while True:
    #         data = self.output_queue.get()
    #         if data:
    #             for k, v in data.items():
    #                 if k != 'image':
    #                     print(f'{k}: \t{v}')
    #             print('writing object into file.')
    #             print(f"Shape: {data['image'].shape}")
    #             cv2.imwrite(os.path.join('save', data['name']), data['image'])
    #         else:
    #             break


