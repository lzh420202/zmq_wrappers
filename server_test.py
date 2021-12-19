import cv2
from zmq_server_wrappers import zmq_data_server, Queue, zmq_multipart_data_server
import os

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