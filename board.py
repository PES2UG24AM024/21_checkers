SIZE = 8


def initial_board():
    board = [["."] * SIZE for _ in range(SIZE)]
    for r in range(3):
        for c in range(SIZE):
            if (r + c) % 2 == 1:
                board[r][c] = "B"
    for r in range(5, 8):
        for c in range(SIZE):
            if (r + c) % 2 == 1:
                board[r][c] = "R"
    return board


def move_piece(board, start, end):
    """Move a piece. If it was a jump, remove the jumped piece.

    Returns the square of the captured piece, or None for a plain move.
    """
    sr, sc = start
    er, ec = end
    captured = None
    if abs(er - sr) == 2:  # a jump: the jumped square is the midpoint
        captured = ((sr + er) // 2, (sc + ec) // 2)
        board[captured[0]][captured[1]] = "."
    board[er][ec] = board[sr][sc]
    board[sr][sc] = "."
    return captured 