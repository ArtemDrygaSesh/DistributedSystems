from flask import Flask, request, jsonify
import requests, uuid

log_srv = 'http://localhost:8881/logging'
msg_srv = 'http://localhost:8882/messages'

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        txt = request.form.get('txt')
        if not txt:
            return jsonify('No message'), 400
        id = str(uuid.uuid4())
        msg = {'id': id, 'txt': txt}
        action = requests.post(log_srv, data=msg)
        return jsonify(msg), 200

    elif request.method == 'GET':
        log, msg = requests.get(log_srv), requests.get(msg_srv)
        return [f'logging-service: {log.text}'[:-1], f'message-service: {msg.text}'], 200

    else:
        return jsonify('Method not allowed'), 405


if __name__ == '__main__':
    app.run(port=8880)