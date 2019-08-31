import rocksdb
import json
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

# apk add py-zmq

opts = rocksdb.Options()
opts.create_if_missing = True
opts.db_log_dir = '/tmp/logs'
opts.max_log_file_size = 0
opts.max_open_files = 300000
opts.write_buffer_size = 67108864
opts.max_write_buffer_number = 300
opts.target_file_size_base = 67108864

opts.table_factory = rocksdb.BlockBasedTableFactory(
    filter_policy=rocksdb.BloomFilterPolicy(10),
    block_cache=rocksdb.LRUCache(2 * (1024 ** 3)),
    block_cache_compressed=rocksdb.LRUCache(500 * (1024 ** 2)))

db = rocksdb.DB("/tmp/rocksdb-caching", opts)

while True:
    msg = socket.recv()
    msg = json.loads(msg)
    key = msg['key'].encode()
    if msg['_a'] == 'put':
        value = msg['value'].encode()
        # put
        db.put(key, value)
        print('put:' + str(key.decode()))
        socket.send(b'1')

    elif msg['_a'] == 'iter':
        # iterasi
        it = db.iterkeys()
        it.seek(key)
        at = []
        for t in it:
            at.append(t.decode())
        keys = str(json.dumps(at)).encode()
        print('iter:' + str(key))
        socket.send(keys)

    else:
        print('get:' + str(key.decode()))
        gt = db.get(key)
        if gt == None:
            gt = str('0').encode()
        socket.send(gt)
