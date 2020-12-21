class Pos(object):
    lanes = ["a", "b", "c", "d", "e", "f", "g", "h"]
    def __init__(self, lane=0, rank=0):
        self.lane = lane
        self.rank = rank

    def __str__(self):
        return Pos.lanes[self.lane-1] + str(self.rank)

    def __repr__(self):
        return Pos.lanes[self.lane-1] + str(self.rank)

    def asdict(self):
        return {
            "lane": self.lane,
            "rank": self.rank
        }

    @staticmethod
    def strToInt(pos_str):
        if len(pos_str) > 2:
            raise UserWarning("pos has more than 2 characters")
        if not pos_str[0] in Pos.lanes:
            raise UserWarning("invalid lane")
        if not (1 <= int(pos_str[1]) <= 8):
            raise UserWarning("rank not in range")
        lane = Pos.lanes.index(pos_str[0]) + 1
        rank = int(pos_str[1])
        return lane, rank
