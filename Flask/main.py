from flask import Flask, request, render_template, send_file, redirect, session, g, make_response
from flask_socketio import SocketIO
import os
import socket
from threading import Thread
from time import sleep
import sys

dir = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(dir)
sys.path.append(parent)

from server_commands import cmd


app = Flask(__name__)
app.secret_key = os.urandom(24)

socketio = SocketIO(app)

server_ip = "0.0.0.0"
server_port = 5000


remote_server_ip = "127.0.0.1"
remote_server_port = 45000
BUF_SIZE = 2048
CONN_FLAG = True
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    soc.connect((remote_server_ip, remote_server_port))
    soc.settimeout(1)
except Exception as e:
    CONN_FLAG = False

# print("soc connected")
def remote_server_handler():
    sleep(3)
    while True:
        # soc.send(cmd.UPDATE.value.encode("utf-8"))

        try:
            msg = soc.recv(BUF_SIZE)
            msg = msg.decode()
            print(f"kg server> {msg}")
        except socket.timeout as e:
            msg = None

        socketio.emit("hello", {"msg": msg})

        # if msg:
        #     print(msg)
        #     socketio.emit("hello", {"msg": "OLA"})

        # if msg:
        #     print(msg)
        #     socketio.emit("hello", {"msg": msg[0]})
        #     print("EMIT")

        sleep(1)
        if msg == cmd.SHUTDOWN:
            break
    soc.close()


if CONN_FLAG:
    th = Thread(target=remote_server_handler)
    th.start()


@socketio.on("client-connect")
def client_connect(args):
    print(args)
    socketio.emit("hello", {"msg": "HELLO"})

@app.route('/')
def index():
    return render_template('index.html')


socketio.run(app.run(server_ip, server_port, debug=True))
