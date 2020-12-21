from copy import deepcopy

from constants import START_PIECES
from pos import Pos
from moves import moveNotBlocked, validPattern

class Board(object):
    def __init__(self, pieces=START_PIECES, turn="white"):
        self.pieces = pieces
        self.turn = turn
        self.positions = self.updatePos()

    def updatePos(self):
        positions = dict()
        for p in self.pieces:
            key = str(p.pos)
            positions[key] = p
        self.positions = positions
        return positions

    def asdict(self):
        return {
            "pieces": self.pieces,
            "turn": self.turn
        }

    @staticmethod
    def keys_row(row, color):
        poss = []
        order = range(1, 9) if color=="white" else reversed(range(1, 9))
        for i in order:
            poss.append(str(Pos(i, row)))
        return poss

    def newTurn(self):
        if self.turn == "white":
            self.turn = "black"
        else:
            self.turn = "white"

    def draw(self, color):
        if color == "white":
            ranks = "    ┃ a ┃ b ┃ c ┃ d ┃ e ┃ f ┃ g ┃ h ┃"
            order = list(reversed(range(1,9)))
        else:
            ranks = "    ┃ h ┃ g ┃ f ┃ e ┃ d ┃ c ┃ b ┃ a ┃"
            order = list(range(1,9))
        print("┏━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┓")
        for i in order:
            keys = Board.keys_row(i, color)
            row_str = "┃ " + str(i) + " ┃"  
            for key in keys:
                if key in self.positions:
                    row_str += (" " + str(self.positions[key]) + " ┃")
                else:
                    row_str += ("   ┃")
            print(row_str)
            
            if i == order[-1]:
                print("┗━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━┫")
            else:
                print("┣━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━┫")
        print(ranks)
        print("    ┗━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┛")

    def posColor(self, pos_str):
        if pos_str in self.positions:
            return self.positions[pos_str].color
        return ""
        raise UserWarning("no piece on pos")

    # def posEmpty(self, pos_str):
    #     for _ in self.positions[pos_str]:
    #         return False
    #     return True

    def posType(self, pos_str):
        if pos_str in self.positions:
            return self.positions[pos_str].type
        return ""

    def kingPos(self, color):
        for p in self.pieces:
            if p.type == "K" and p.color == color:
                return str(p.pos)
        raise UserWarning("could not find king")

    def copy(self):
        return Board(self.pieces, self.turn)

    def inCheck(self, color):
        posKing = self.kingPos(color)
        opponent_pieces = [piece for piece in self.pieces if piece.color != color]
        for piece in opponent_pieces:
            move_from = str(piece.pos)
            valid = validPattern(move_from, posKing, piece.type, True)
            valid = valid and moveNotBlocked(self, move_from, posKing)
            if valid:
                return True
        return False
    
    def makesSelfCheck(self, move_from, move_to, takes, color):
        board_copy = deepcopy(self)

        if takes:
            piece_taken = board_copy.positions[move_to]
            index_taken = board_copy.pieces.index(piece_taken)
            board_copy.pieces.pop(index_taken)

        piece_move = board_copy.positions[move_from]
        index = board_copy.pieces.index(piece_move)
        board_copy.pieces[index].pos = Pos(Pos.lanes.index(move_to[0])+1, int(move_to[1]))
        board_copy.updatePos()

        return board_copy.inCheck(color)

        


    def moveInput(self):
        while True:
            move_str = input(self.turn + "s move:").lower()
            if len(move_str) == 4 and move_str[:2] in self.positions:
                move_from = move_str[:2]
                move_to = move_str[2:]

                takes = False
                color_to = self.posColor(move_to)
                if color_to != self.turn and color_to != "":
                    takes = True

                if self.posColor == self.turn:
                    print("cannot take own piece!")
                    continue

                # Not allowed to move opponents piece
                if self.posColor(move_from) != self.turn:
                    print("cannot move opponents piece!")
                    continue

                pieceType = self.posType(move_from)
                valid = validPattern(move_from, move_to, pieceType, takes)
                valid = valid and moveNotBlocked(self, move_from, move_to)
                if valid:

                    # Does the move result in self-check?
                    if self.makesSelfCheck(move_from, move_to, takes, self.turn):
                        print("move puts you in check!")
                        continue

                    if takes:
                        piece_taken = self.positions[move_to]
                        # TODO: Save piece_taken to "captured list"/add points
                        print(self.pieces)
                        index_taken = self.pieces.index(piece_taken)
                        self.pieces.pop(index_taken)

                    piece_move = self.positions[move_from]
                    index = self.pieces.index(piece_move)
                    self.pieces[index].pos = Pos(Pos.lanes.index(move_to[0])+1, int(move_to[1]))
                    self.updatePos()
                    break

            print("invalid move.")
        return move_str

    # def move(self, move_str):
    #     move_from = move_str[:2]
    #     move_to = move_str[2:]

    #     pieceType = self.posType(move_from)
    #     if validPattern(move_from, move_to, pieceType):
    #         piece_move = self.positions[move_from]
    #         index = self.pieces.index(piece_move)
    #         self.pieces[index].pos = Pos(Pos.lanes.index(move_to[0])+1, int(move_to[1]))
    #         self.updatePos()
    