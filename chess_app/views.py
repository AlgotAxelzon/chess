from flask import render_template, abort

from chess_app.app import app
from chess_app.match import Match

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/play/<string:match_id>")
def play(match_id):
    if match_id in Match.matches:
        return render_template("match.html", match_id=match_id)
    abort(400)

@app.route("/spectate/<string:match_id>")
def spectate(match_id):
    if match_id in Match.matches:
        return render_template("spectate.html", match_id=match_id)
    abort(400)

# TODO: Implement practice mode
# @app.route("/practice")
# def practice():
#     return
