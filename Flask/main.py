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

from server_commands import cmd, string_delim, obj


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
    soc.send(cmd.INIT.value.encode("utf-8"))
    print("Sending init")
    while True:
        # soc.send(cmd.UPDATE.value.encode("utf-8"))

        try:
            msg = soc.recv(BUF_SIZE)
            msg = msg.decode()
        except socket.timeout as e:
            msg = None

        if msg:
            print(f"server> {msg}")

            cmd_type, msg = msg.split(string_delim.COMMAND_TYPE.value)
            obj_type, msg = msg.split(string_delim.OBJECT_TYPE.value)
            data, str_score = msg.split(string_delim.DATA_DEL.value)

            if obj_type == obj.NODE.value:
                id, type, label = data[1:-1].split(",")
                print(id, type, label)

                socketio.emit("add-node", {
                    "id": id,
                    "type": type,
                    "label": label
                })


            # print(cmd_type)
            # print(obj_type)
            # print(data)
            # print(str_score)

            # socketio.emit("hello", {"msg": msg})

        sleep(1)
        if msg == cmd.SHUTDOWN:
            break
    soc.close()


if CONN_FLAG:
    th = Thread(target=remote_server_handler)
    th.start()
    CONN_FLAG = False


@socketio.on("client-connect")
def client_connect(args):
    soc.send(cmd.INIT.value.encode("utf-8"))
    socketio.emit("hello", {"msg": "HELLO"})

@app.route('/')
def index():
    return render_template('index.html')


socketio.run(app.run(server_ip, server_port))
