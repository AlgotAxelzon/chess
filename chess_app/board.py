from copy import deepcopy

from chess_app.constants import CASTLE_BLACK, CASTLE_WHITE, EP_RANK_BLACK, EP_RANK_WHITE, START_PIECES
from chess_app.pos import Pos
from chess_app.moves import moveNotBlocked, validPattern, validCastle

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

    def positionsDict(self):
        res = deepcopy(self.positions)
        for key in res:
            res[key] = res[key].asdict()
        return res

    def asdict(self):
        return {
            "pieces": [p.asdict() for p in self.pieces],
            "turn": self.turn,
            "positions": self.positionsDict()
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

    def posType(self, pos_str):
        if pos_str in self.positions:
            return self.positions[pos_str].type
        return ""

    def kingPos(self, color):
        for p in self.pieces:
            if p.type == "K" and p.color == color:
                return str(p.pos)
        print("could not find king")

    def copy(self):
        return Board(self.pieces, self.turn)

    def isCastle(self, move_str):
        if self.turn == "white":
            return move_str in CASTLE_WHITE
        else:
            return move_str in CASTLE_BLACK

    def inCheck(self, color):
        posKing = self.kingPos(color)
        opponent_pieces = [piece for piece in self.pieces if piece.color != color]
        for piece in opponent_pieces:
            move_from = str(piece.pos)
            valid = validPattern(move_from, posKing, piece.type)
            if not valid:
                continue
            valid, _, _ = moveNotBlocked(self, move_from, posKing)
            if valid:
                return True
        return False
    
    def makesSelfCheck(self, move_from, move_to, takes, color, takeEP):
        board_copy = deepcopy(self)

        if takeEP:
            if color == "white":
                posTake = move_to[0] + str(EP_RANK_BLACK)
            else:
                posTake = move_to[0] + str(EP_RANK_WHITE)
            piece_taken = board_copy.positions[posTake]
            index_taken = board_copy.pieces.index(piece_taken)
            board_copy.pieces.pop(index_taken)
        
        if takes:
            piece_taken = board_copy.positions[move_to]
            index_taken = board_copy.pieces.index(piece_taken)
            board_copy.pieces.pop(index_taken)

        piece_move = board_copy.positions[move_from]
        index = board_copy.pieces.index(piece_move)
        board_copy.pieces[index].pos = Pos(Pos.lanes.index(move_to[0])+1, int(move_to[1]))
        board_copy.updatePos()

        return board_copy.inCheck(color)

    def moveInput(self, move=""):
        if move == "":
            move_str = input(self.turn + "s move:").lower()
        else:
            move_str = move
        if len(move_str) == 4 and move_str[:2] in self.positions:
            move_from = move_str[:2]
            move_to = move_str[2:]

            takes = False
            color_to = self.posColor(move_to)
            if color_to != self.turn and color_to != "":
                takes = True

            castle, rook_from, rook_to = False, False, False
            if self.isCastle(move_str):
                castle, rook_from, rook_to = validCastle(self, move_str)

            if self.posColor == self.turn:
                print("cannot take own piece!")
                return False

            # Not allowed to move opponents piece
            if self.posColor(move_from) != self.turn:
                print("cannot move opponents piece!")
                return False

            # Test for move following basic piece-rules
            pieceType = self.posType(move_from)
            valid = validPattern(move_from, move_to, pieceType, self.turn)
            if not valid and not castle:
                print("invalid move")
                return False
            
            # Test for move blocked by other pieces
            valid, takeEP, moveEP = moveNotBlocked(self, move_from, move_to)
            if valid or castle:

                # Test for move resulting in self-check
                if self.makesSelfCheck(move_from, move_to, takes, self.turn, takeEP):
                    print("move puts you in check!")
                    return False

                # Piece gets taken
                if takeEP or takes:
                    if takes:
                        posTaken = move_to
                    else:
                        if self.turn == "white":
                            posTaken = move_to[0] + str(EP_RANK_BLACK)
                        else:
                            posTaken = move_to[0] + str(EP_RANK_WHITE)

                    piece_taken = self.positions[posTaken]
                    index_taken = self.pieces.index(piece_taken)
                    self.pieces.pop(index_taken)

                # If castle, move rook
                if castle:
                    if rook_from == False or rook_to == False:
                        print("rook_from or rook_to is False when castle is True") 
                    piece_move = self.positions[rook_from]
                    index = self.pieces.index(piece_move)
                    self.pieces[index].pos = Pos(Pos.lanes.index(rook_to[0])+1, int(rook_to[1]))
                    # Piece has moved
                    self.pieces[index].hasMoved = True

                piece_move = self.positions[move_from]
                index = self.pieces.index(piece_move)
                self.pieces[index].pos = Pos(Pos.lanes.index(move_to[0])+1, int(move_to[1]))
                
                # Piece can be captured en passant
                if moveEP:
                    self.pieces[index].ep = True
                else:
                    self.pieces[index].ep = False
                
                # Piece has moved
                self.pieces[index].hasMoved = True

                self.updatePos()
                return True
        print("invalid move.")
        return False
