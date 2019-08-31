from sanic import Sanic
from sanic import response

import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://0.0.0.0:5555")
app = Sanic()

# rocksdb get


def get(key):
    key = str(key)
    kv = {'_a': 'get', 'key': key}
    kv = json.dumps(kv).encode()
    socket.send(kv)
    m = socket.recv()
    return m

# rocksdb put


def put(key, value):
    kv = {'_a': 'put', 'key': str(key), 'value': str(value)}
    kv = json.dumps(kv).encode()
    socket.send(kv)
    m = socket.recv()
    return m

# rocksdb iter


def iter(key):
    key = str(key)
    kv = {'_a': 'iter', 'key': key}
    kv = json.dumps(kv).encode()
    socket.send(kv)
    m = socket.recv()
    return m


@app.route('/')
async def test(request):
    return response.text('ok')


@app.route('/favicon.ico')
async def test(request):
    return response.text('ok')


@app.route('/keys/<key>')
async def get_handler(request, key):
    t = iter(key).decode()
    return response.text(t)


@app.route('/get/<key>')
async def get_handler(request, key):
    t = get(key).decode()
    return response.text(t)


@app.route('/set/<key>/<value>')
async def set_handler(request, key, value):
    t = put(key, value).decode()
    return response.text(t)


@app.route("/set/<key>", methods=["POST"])
async def handler(request, key):
    key = str(key)
    value = str(json.dumps(request.json))
    c = put(key, value).decode()
    print(key, value)
    return response.text(c)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
