from flask import Flask, jsonify
import socket

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello, World! Your VPS is up and running."

@app.route('/server-info')
def server_info():
    # Gather server details
    server_details = {
        "hostname": socket.gethostname(),
        "ip_address": socket.gethostbyname(socket.gethostname())
    }
    return jsonify(server_details)

if __name__ == '__main__':
    # Listen on all interfaces (0.0.0.0) and port 5000
    app.run(host='0.0.0.0', port=5000)
