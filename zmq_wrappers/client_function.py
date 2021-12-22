def client_payload(result: dict):
    if result:
        if result.get('TEST') == 'SUCCESS':
            print('ZeroMQ Server is Running!')
            return
        else:
            print('Get results.')
    else:
        print('ZeroMQ Server is crashed!')
