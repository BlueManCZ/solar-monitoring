from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from time import sleep
from signal import signal, SIGINT
import threading
from my_parser import parse

ADDRESS = '0.0.0.0'
PORT = 5000

app = Flask(__name__)
app.secret_key = 'secret'
sio = SocketIO(app)
connections = 0
running = True


@sio.on('connect')
def connect():
    global connections
    connections += 1


@sio.on('disconnect')
def disconnect():
    global connections
    connections -= 1


class SolarSystem:
    panels = []
    batteries = []


class Panel:
    voltage = 0
    current = 0

    def power(self):
        return self.voltage * self.current


class Battery:
    voltage = 0
    current = 0
    capacity = 0


def auto_refresh():
    while running:
        if connections > 0:
            data = parse()
            if not data:
                continue
            sio.emit('refresh', data, namespace='/')
        sleep(2)


def quit_handler(signal_received, frame):
    global running
    running = False
    quit()


@app.route('/')
def hello_world():

    return render_template('index.html')


if __name__ == '__main__':

    signal(SIGINT, quit_handler)

    y = threading.Thread(target=auto_refresh)
    y.start()

    sio.run(app, host=ADDRESS, port=PORT, debug=True)
