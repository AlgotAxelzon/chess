class Piece(object):
    def __init__(self, color, type, pos):
        self.color = color
        self.type = type
        self.pos = pos
        self.ep = False

    def __str__(self):
        if self.color == "white":
            return self.type.upper()
        return self.type.lower()

    def __repr__(self):
        return str([self.color, self.type, str(self.pos)])
