from piece import Piece
from pos import Pos

WHITE_START_PIECES = [Piece("white", "R", Pos(1,1)), Piece("white", "N", Pos(2,1)), Piece("white", "B", Pos(3,1)), Piece("white", "Q", Pos(4,1)), Piece("white", "K", Pos(5,1)), Piece("white", "B", Pos(6,1)), Piece("white", "N", Pos(7,1)), Piece("white", "R", Pos(8,1)), 
                      Piece("white", "P", Pos(1,2)), Piece("white", "P", Pos(2,2)), Piece("white", "P", Pos(3,2)), Piece("white", "P", Pos(4,2)), Piece("white", "P", Pos(5,2)), Piece("white", "P", Pos(6,2)), Piece("white", "P", Pos(7,2)), Piece("white", "P", Pos(8,2))]

BLACK_START_PIECES = [Piece("black", "R", Pos(1,8)), Piece("black", "N", Pos(2,8)), Piece("black", "B", Pos(3,8)), Piece("black", "Q", Pos(4,8)), Piece("black", "K", Pos(5,8)), Piece("black", "B", Pos(6,8)), Piece("black", "N", Pos(7,8)), Piece("black", "R", Pos(8,8)), 
                      Piece("black", "P", Pos(1,7)), Piece("black", "P", Pos(2,7)), Piece("black", "P", Pos(3,7)), Piece("black", "P", Pos(4,7)), Piece("black", "P", Pos(5,7)), Piece("black", "P", Pos(6,7)), Piece("black", "P", Pos(7,7)), Piece("black", "P", Pos(8,7))]

START_PIECES = WHITE_START_PIECES + BLACK_START_PIECES

EP_RANK_BLACK = 5
EP_RANK_WHITE = 4

CASTLE_WHITE = ["e1g1", "e1c1"]
CASTLE_BLACK = ["e8g8", "e8c8"]
# [[king, rook, kingMove1/rookMove/emptySq, kingMove2/emptySq, emptySq],]
CASTLE_WHITE_SQUARES = [["e1", "h1", "f1", "g1", "g1"], ["e1", "a1", "d1", "c1", "b1"]]
CASTLE_BLACK_SQUARES = [["e8", "h8", "f8", "g8", "g8"], ["e8", "a8", "d8", "c8", "b8"]]
