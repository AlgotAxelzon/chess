from board import Board



if __name__=="__main__":
    board = Board()
    while True:
        board.draw("white")
        move = board.moveInput()
        # board.move(move)
        board.newTurn()
