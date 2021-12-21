import cv2
from client_wrapper import custom_client

if __name__ == '__main__':
    client = custom_client('192.168.2.38', 10000, True)
    image = cv2.imread(r'E:\TEST_IMAGES\sar_plane\GF3\GF3_KAS_SL_005811_W95.1_N16.4_20170917_L1A_HH_L10002605023_0.020.tiff', cv2.IMREAD_UNCHANGED)
    data = dict(image=image, name='s27.png')
    client.sendData(data)
    # client.testServer()

