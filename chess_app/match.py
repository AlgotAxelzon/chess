from uuid import uuid4
import json

from chess_app.board import Board


class Match(object):
    matches = dict()
    def __init__(self, type="match"):
        self.type = type
        self.id = str(uuid4())
        self.board = Board()
        self.players = []
        self.spectators = []

    def asjson(self):
        return json.dumps({
            "type": self.type,
            "id": self.id,
            "board": self.board.asdict(),
            "players": self.players,
            "spectators": self.spectators
        })

# if __name__=="__main__":
#     board = Board()
#     while True:
#         board.draw("white")
#         move = board.moveInput()
#         # board.move(move)
#         board.newTurn()
