SIZE = 8


def owner(piece):
    """'R', 'B', or None for an empty square (kings 'RK'/'BK' belong to R/B)."""
    return None if piece == "." else piece[0]


def _on_board(r, c):
    return 0 <= r < SIZE and 0 <= c < SIZE


def _directions(piece):
    """Row directions a piece may move in: kings both, men forward only."""
    if piece.endswith("K"):
        return (-1, 1)
    return (-1,) if piece[0] == "R" else (1,)


def simple_move(board, player, start, end):
    sr, sc = start
    er, ec = end
    piece = board[sr][sc]
    return (
        owner(piece) == player
        and _on_board(er, ec)
        and board[er][ec] == "."
        and abs(ec - sc) == 1
        and (er - sr) in _directions(piece)
    )


def capture_move(board, player, start, end):
    """Return the jumped square if start->end is a legal capture, else None."""
    sr, sc = start
    er, ec = end
    piece = board[sr][sc]
    if owner(piece) != player or not _on_board(er, ec) or board[er][ec] != ".":
        return None
    if abs(er - sr) != 2 or abs(ec - sc) != 2:
        return None
    if (er - sr) // 2 not in _directions(piece):
        return None
    mr, mc = (sr + er) // 2, (sc + ec) // 2
    victim = owner(board[mr][mc])
    if victim is None or victim == player:  # must jump an opponent piece
        return None
    return (mr, mc)


def captures_from(board, player, pos):
    """All landing squares for captures available to the piece at pos."""
    r, c = pos
    ends = []
    for d in _directions(board[r][c]):
        for dc in (-2, 2):
            end = (r + 2 * d, c + dc)
            if capture_move(board, player, pos, end):
                ends.append(end)
    return ends


def _simple_moves_from(board, player, pos):
    r, c = pos
    ends = []
    for d in _directions(board[r][c]):
        for dc in (-1, 1):
            end = (r + d, c + dc)
            if simple_move(board, player, pos, end):
                ends.append(end)
    return ends


def legal_moves(board, player, only_from=None):
    """List of (start, end) legal moves.

    Forced capture: if any capture exists, only captures are returned.
    If only_from is given (mid multi-capture), only captures by that piece.
    """
    captures, simples = [], []
    for r in range(SIZE):
        for c in range(SIZE):
            if owner(board[r][c]) != player:
                continue
            if only_from is not None and (r, c) != only_from:
                continue
            captures += [((r, c), e) for e in captures_from(board, player, (r, c))]
            simples += [((r, c), e) for e in _simple_moves_from(board, player, (r, c))]
    if only_from is not None:
        return captures
    return captures or simples


def promote(board):
    """Crown men on the far row. Returns the list of promoted squares."""
    promoted = []
    for c in range(SIZE):
        if board[0][c] == "R":
            board[0][c] = "RK"
            promoted.append((0, c))
        if board[SIZE - 1][c] == "B":
            board[SIZE - 1][c] = "BK"
            promoted.append((SIZE - 1, c))
    return promoted