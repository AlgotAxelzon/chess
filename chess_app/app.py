from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__, static_url_path='/static')
socketio = SocketIO(app)

import chess_app.socketevents

if __name__ == "__main__":
    socketio.run(app)
