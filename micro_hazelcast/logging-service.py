import hazelcast, argparse, os
from flask import Flask, request, jsonify
from check import check_container

msg = {}

parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int, required=True)
args = parser.parse_args()

app = Flask(__name__)

containers = ['lab2-node1', 'lab2-node2', 'lab2-node3', 'lab2-management-center']
for c in containers[:-1]:
    if not check_container(c):
        os.system(f'docker start {c}')
        container = c
        break
if not check_container(containers[-1]):
    os.system(f'docker start {containers[-1]}')

hz = hazelcast.HazelcastClient(cluster_name='lab2')

msg = hz.get_map('messages').blocking()

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        id, txt = request.form.get('id'), request.form.get('txt')
        if not (id or txt):
            return jsonify('No id or text'), 400

        msg.put(id, txt)
        print('Message:', txt)
        return jsonify('Message was logged'), 201

    elif request.method == 'GET':
        return [msg.get(key) for key in msg.key_set()]

    else:
        return jsonify('Method not allowed'), 405


app.run(port=args.port)

try:
    while True: pass
except KeyboardInterrupt:
    hz.shutdown()
    os.system(f'Docker stop {container}')