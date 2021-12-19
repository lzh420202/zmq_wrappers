from zmq_wrappers.zmq_client_wrappers import Queue, zmq_multipart_data_client, monitorThread
import cv2

if __name__ == '__main__':
    ip = '192.168.2.38'
    port = 10000
    input_queue = Queue(10)
    output_queue = Queue(10)
    process_info = dict(current=0, total=0, used_time=0)
    client = zmq_multipart_data_client(ip, port, input_queue, output_queue, process_info)
    client.start()
    monitor = monitorThread(process_info, 0.05)
    monitor.start()
    image = cv2.imread(r'E:\TEST_IMAGES\sar_plane\GF3\GF3_KAS_SL_005811_W95.1_N16.4_20170917_L1A_HH_L10002605023_0.020.tiff', cv2.IMREAD_UNCHANGED)
    input_queue.put(dict(image=image, name='s27.png'))



    client.join()

