from flask import Flask, request, render_template, send_file, redirect, session, g, make_response
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

server_ip = "0.0.0.0"
server_port = 5000


@app.route('/')
def index():
    return render_template('index.html')



app.run(server_ip, server_port, debug=True)
