from flask import Flask, request, render_template, send_file, redirect, session, g, make_response
from flask_socketio import SocketIO
import os
import socket
from threading import Thread
from time import sleep
import sys
import re

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
CONN_FLAG = False
RUNNING = True
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Server handler function
# Connects to the KG server and start receiving updates on the graph
def remote_server_handler():
    global CONN_FLAG
    while not CONN_FLAG:
        try:
            soc.connect((remote_server_ip, remote_server_port))
            soc.settimeout(1)
            CONN_FLAG = True
        except Exception as e:
            pass

    while RUNNING:
        try:
            msg = soc.recv(BUF_SIZE)
            msg = msg.decode()
        except socket.timeout as e:
            msg = None

        if msg == cmd.SHUTDOWN:
            print(f"server> {msg}")
            break

        if msg:
            print(f"server> {msg}")

            cmd_type, obj_type, data = match_command(msg)

            if cmd_type == cmd.ADD.value:
                if obj_type == obj.NODE.value:
                    node_json = match_node(data)
                    print(f"node json> {node_json}")

                    socketio.emit("add-node", node_json)
                elif obj_type == obj.EDGE.value:
                    edge_json = match_edge(data)
                    print(f"edge json> {edge_json}")

                    socketio.emit("add-edge", edge_json)



            elif cmd_type == cmd.REMOVE.value:
                pass
            elif cmd_type == cmd.UPDATE.value:
                # socketio.emit("update", )
                id, str_score = data[1:-1].split(",")
                print(obj_type, id, str_score)



        # sleep(1)

    soc.send(cmd.SHUTDOWN.value.encode("utf-8"))
    soc.close()
    print("Disconnected!")


def match_command(string: str):
    cmd_type, string = string.split(string_delim.COMMAND_TYPE.value)
    obj_type, data = string.split(string_delim.OBJECT_TYPE.value)
    return cmd_type, obj_type, data


def match_node(string: str):
    id, type, label, str_score = string[1:-1].split(",")

    return {"id": id,
            "type": type,
            "label": label,
            "str_score": str_score,}


def match_edge(string: str):
    match = re.match(r"\(id:(.*?),source:(.*?),target:(.*?),str_score:(.*?)\)", string)

    id = match.group(1)
    source = match.group(2)
    target = match.group(3)
    str_score = match.group(4)
    return {"id": id,
            "source": match_node(source),
            "target": match_node(target),
            "str_score": str_score,}


# Flask server functions
@socketio.on("client-connect")
def client_connect(args):
    print(f"client connected (CONN_FLAG {CONN_FLAG})")
    if CONN_FLAG:
        print("sending init")
        soc.send(cmd.INIT.value.encode("utf-8"))
    socketio.emit("hello", {"msg": "HELLO"})


@socketio.on("add-test-edge")
def test(args):
    socketio.emit("add-test-edge", args)


@app.route('/')
def index():
    return render_template('index.html')


th = Thread(target=remote_server_handler)
th.start()

socketio.run(app.run(server_ip, server_port))
