from constants import EP_RANK_BLACK, EP_RANK_WHITE
from pos import Pos
from helpfunctions import sign

def rookPattern(move_from, move_to):
    from_lane, from_rank = Pos.strToInt(move_from)
    to_lane, to_rank = Pos.strToInt(move_to)

    if (from_lane == to_lane) or (from_rank == to_rank):
        return True

    return False

def bishopPattern(move_from, move_to):
    from_lane, from_rank = Pos.strToInt(move_from)
    to_lane, to_rank = Pos.strToInt(move_to)

    if abs(to_lane - from_lane) == abs(to_rank - from_rank):
        return True

    return False

def queenPattern(move_from, move_to):

    if rookPattern(move_from, move_to) or bishopPattern(move_from, move_to):
        return True
    
    return False

def kingPattern(move_from, move_to):
    from_lane, from_rank = Pos.strToInt(move_from)
    to_lane, to_rank = Pos.strToInt(move_to)
    
    if abs(to_lane - from_lane) == 1 or abs(to_rank - from_rank) == 1:
        return True

    return False

def knightPattern(move_from, move_to):
    from_lane, from_rank = Pos.strToInt(move_from)
    to_lane, to_rank = Pos.strToInt(move_to)

    if abs(to_lane - from_lane) == 1 and abs(to_rank - from_rank) == 2:
        return True
    elif abs(to_lane - from_lane) == 2 and abs(to_rank - from_rank) == 1:
        return True

    return False

def pawnPattern(move_from, move_to, color=""):
    from_lane, from_rank = Pos.strToInt(move_from)
    to_lane, to_rank = Pos.strToInt(move_to)

    lane_diff = to_lane - from_lane
    rank_diff = to_rank - from_rank

    # Can only move to the next 3 squares
    if not (-1 <= lane_diff <= 1):
        return False

    if (color == "white") or color == "":
        if rank_diff == 1:
            return True
        if rank_diff == 2 and from_rank == 2 and lane_diff == 0:
            return True

    if (color == "black") or color == "":
        if rank_diff == -1:
            return True
        if rank_diff == -2 and from_rank == 7 and lane_diff == 0:
            return True

    return False

def validPattern(move_from, move_to, pieceType, color=""):
    if pieceType == "R":
        return rookPattern(move_from, move_to)
    elif pieceType == "B":
        return bishopPattern(move_from, move_to)
    elif pieceType == "Q":
        return queenPattern(move_from, move_to)
    elif pieceType == "K":
        return kingPattern(move_from, move_to)
    elif pieceType == "N":
        return knightPattern(move_from, move_to)
    elif pieceType == "P":
        return pawnPattern(move_from, move_to, color)
    return False

def moveNotBlocked(board, move_from, move_to):
    if not move_from in board.positions:
        raise UserWarning("moveNotBlocked: move_from not in positions")
    
    pieceType = board.positions[move_from].type
    pieceColor = board.positions[move_from].color

    from_lane, from_rank = Pos.strToInt(move_from)
    to_lane, to_rank = Pos.strToInt(move_to)

    lane_diff = to_lane - from_lane
    rank_diff = to_rank - from_rank

    takeEP = False
    moveEP = False

    if pieceType == "R" or pieceType == "B" or pieceType == "Q":
        if validPattern(move_from, move_to, pieceType):
            lane_dir = sign(lane_diff)
            rank_dir = sign(rank_diff)
            for i in range(1, max(abs(lane_diff), abs(rank_diff))):
                pos_str = str(Pos(from_lane+lane_dir*i, from_rank+rank_dir*i))
                if pos_str in board.positions:
                    return False, takeEP, moveEP
            return True, takeEP, moveEP
        return False, takeEP, moveEP
        
    elif pieceType == "K" or pieceType == "N":
        return True, takeEP, moveEP
        
    elif pieceType == "P":
        lane_dir = sign(lane_diff)
        rank_dir = sign(rank_diff)
        # Move straight
        if lane_diff == 0:
            if abs(rank_diff) == 2:
                moveEP = True
            for i in range(1, max(abs(lane_diff), abs(rank_diff))+1):
                pos_str = str(Pos(from_lane+lane_dir*i, from_rank+rank_dir*i))
                if pos_str in board.positions:
                    return False, takeEP, moveEP
            return True, takeEP, moveEP
        # Move diagonal, take
        else:
            # Normal take
            if move_to in board.positions:
                return True, takeEP, moveEP
            # En passant take
            if pieceColor == "white" and to_rank == 6:
                posTake = move_to[0] + str(EP_RANK_BLACK)
                if posTake in board.positions:
                    if board.positions[posTake].ep == True:
                        takeEP = True
                        return True, takeEP, moveEP
            if pieceColor == "black" and to_rank == 3:
                posTake = move_to[0] + str(EP_RANK_WHITE)
                if posTake in board.positions:
                    if board.positions[posTake].ep == True:
                        takeEP = True
                        return True, takeEP, moveEP
            return False, takeEP, moveEP

    raise UserWarning("unexpected piece pieceType")
