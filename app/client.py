import json
import zmq
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")


def get(key):
    kv = {'_a': 'get', 'key': key}
    kv = json.dumps(kv).encode()
    socket.send(kv)
    m = socket.recv()
    return m


def put(key, value):
    kv = {'_a': 'put', 'key': key, 'value': value}
    kv = json.dumps(kv).encode()
    socket.send(kv)
    m = socket.recv()
    return m


put('kopet', '{"kopet":"mambu"}')
print(get('kopet'))
