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

def pawnPattern(move_from, move_to, takes, color=""):
    from_lane, from_rank = Pos.strToInt(move_from)
    to_lane, to_rank = Pos.strToInt(move_to)

    # Can only take diagonally
    if takes and (to_lane - from_lane) == 0:
        return False
    if (not takes) and abs(to_lane - from_lane) == 1:
        return False

    # Can only move to the next 3 squares
    if not (-1 <= (to_lane - from_lane) <= 1):
        return False

    if (color == "white") or color == "":
        if (to_rank - from_rank) == 1:
            return True
        if (to_rank - from_rank) == 2 and from_rank == 2 and not takes:
            return True

    if (color == "black") or color == "":
        if (to_rank - from_rank) == -1:
            return True
        if (to_rank - from_rank) == -2 and from_rank == 7 and not takes:
            return True

    return False

def validPattern(move_from, move_to, type, takes):
    if type == "R":
        return rookPattern(move_from, move_to)
    elif type == "B":
        return bishopPattern(move_from, move_to)
    elif type == "Q":
        return queenPattern(move_from, move_to)
    elif type == "K":
        return kingPattern(move_from, move_to)
    elif type == "N":
        return knightPattern(move_from, move_to)
    elif type == "P":
        return pawnPattern(move_from, move_to, takes)
    return False

def moveNotBlocked(board, move_from, move_to):
    if not move_from in board.positions:
        raise UserWarning("moveNotBlocked: move_from not in positions")
    
    type = board.positions[move_from].type

    from_lane, from_rank = Pos.strToInt(move_from)
    to_lane, to_rank = Pos.strToInt(move_to)

    lane_diff = to_lane - from_lane
    rank_diff = to_rank - from_rank

    if type == "R" or type == "B" or type == "Q":
        lane_dir = sign(lane_diff)
        rank_dir = sign(rank_diff)
        for i in range(1, max(lane_diff, rank_diff)):
            pos_str = str(Pos(from_lane+lane_dir*i, from_rank+rank_dir*i))
            if pos_str in board.positions:
                return False
        return True
        
    elif type == "K" or type == "N":
        return True
        
    elif type == "P":
        lane_dir = sign(lane_diff)
        rank_dir = sign(rank_diff)
        if lane_diff == 0:
            for i in range(1, max(lane_diff, rank_diff)+1):
                pos_str = str(Pos(from_lane+lane_dir*i, from_rank+rank_diff*i))
                if pos_str in board.positions:
                    return False
        return True

    raise UserWarning("unexpected piece type")
