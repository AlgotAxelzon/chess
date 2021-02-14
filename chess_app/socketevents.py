from flask_socketio import emit, join_room
from flask import request

from chess_app.app import socketio
from chess_app.match import Match

connections = []

@socketio.on("join")
def handle_join():
    sid = request.sid
    if not sid in connections:
        connections.append(sid)
    else:
        print("Connection " + str(sid) + " already in connections!")

@socketio.on("disconnect")
def handle_disconnect():
    sid = request.sid
    if sid in connections:
        connections.remove(sid)
    else:
        print("Connection " + str(sid) + " not in connections!")

@socketio.on("createMatch")
def handle_createMatch():
    match = Match()
    match_id = match.id
    Match.matches[match_id] = match
    emit("matchCreated", {"match_id": match_id})

@socketio.on("playMatch")
def handle_playMatch(data):
    match_id = data["match_id"]
    if match_id in Match.matches:
        match = Match.matches[match_id]
        # if len(match.players) < 2:
        join_room(match_id)
        match.players.append(request.sid)
        emit("joinedPlay", {"match": match.asjson()})
        # else:
        #     match.spectators.append(request.sid)
        #     emit("toSpectate", {"match_id": match_id})
    else:
        print(str(request.sid) + " tried to play non-existing match " + match_id)

@socketio.on("spectateMatch")
def handle_spectateMatch(data):
    match_id = data["match_id"]
    if match_id in Match.matches:
        join_room(match_id)
        match = Match.matches[match_id]
        match.spectators.append(request.sid)
        emit("joinedSpectate", {"match": match.asjson()})
    else:
        print(str(request.sid) + " tried to spectate non-existing match " + match_id)

@socketio.on("move")
def handle_playMatch(data):
    match_id = data["match_id"]
    move = data["move"]
    if match_id in Match.matches:
        match = Match.matches[match_id]
        # turnIndex = 0 if match.board.turn == "white" else 1
        # if request.sid == match.players[turnIndex]:
        move_ok = match.board.moveInput(move)
        if move_ok:
            match.board.newTurn()
            # emit("updateBoard", {"board": match.board}, room=match_id)
            emit("updateBoard", {"changed": match.board.changed}, room=match_id)
        else:
            print(str(request.sid) + " tried to make invalid move in match " + match_id)
            emit("revertMove")
        # else:
        #     print(str(request.sid) + " tried to make a move on opponents turn in match " + match_id)
        #     emit("revertMove")
    else:
        print(str(request.sid) + " tried to make move in non-existing match " + match_id)
        emit("revertMove")
