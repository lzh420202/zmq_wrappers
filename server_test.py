from zmq_wrappers import custom_server

if __name__ == '__main__':
    server = custom_server(10000)
    # server.getData()