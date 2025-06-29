from flask import Flask, request, jsonify
import socket, requests, uuid, random, hazelcast


log_ports = [8881, 8882, 8883]
msg_ports = [8884, 8885]
msg_srv = 'http://localhost:8884/'

hz = hazelcast.HazelcastClient(cluster_name='lab4')
msg_queue = hz.get_queue("queue").blocking()
print(hz)
response = []

app = Flask(__name__)

def is_open(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    check_port = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    return True if check_port == 0 else False

def choose_port(ports):
    open_ports = ports.copy()
    while open_ports:
        port = random.choice(open_ports)
        if not is_open(port):
            print(f"Port {port} is closed")
            open_ports.remove(port)
        else:
            print(f"Port {port} is open")
            return port
    raise ValueError("No available open ports")

@app.route('/', methods=['POST', 'GET'])
def home():
    logging_port = choose_port(log_ports)
    print(f'logging port: {logging_port}')

    if request.method == 'POST':
        txt = request.form.get('txt')
        if not txt:
            return jsonify('No message'), 400
        id = str(uuid.uuid4())
        msg = {'id': id, 'txt': txt}
        action = requests.post(f'http://localhost:{logging_port}/', data=msg)
        msg_queue.put(txt)
        return jsonify(msg), 200

    elif request.method == 'GET':

        messages_port = choose_port(msg_ports)
        print(f'messages port: {messages_port}')
        log_response, msg_response = requests.get(f'http://localhost:{logging_port}/'), requests.get(
            f'http://localhost:{messages_port}/')

        for i in msg_response.json():
            if i not in response:
                response.append(i)

        return [f'logging-service: {log_response.json()}'[:-1], f'message-service: {response}'], 200

    else:
        return jsonify('Method not allowed'), 405



if __name__ == '__main__':
    app.run(port=8880)