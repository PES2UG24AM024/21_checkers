from board import initial_board, move_piece, SIZE
from rules import legal_moves, captures_from, promote, owner


def fmt(pos):
    return f"({pos[0]},{pos[1]})"


class Checkers:
    def __init__(self):
        self.board = initial_board()
        self.player = "R"
        self.chain = None  # square of the piece that must keep capturing

    def opponent(self):
        return "B" if self.player == "R" else "R"

    def print_board(self):
        print("\n   " + "".join(f"{c:<3}" for c in range(SIZE)))
        for r, row in enumerate(self.board):
            print(f"{r}  " + "".join(f"{p:<3}" for p in row))

    def game_over(self):
        """Print the result and return True if the current player cannot play."""
        if not any(owner(p) == self.player for row in self.board for p in row):
            print(f"{self.player} has no pieces left. {self.opponent()} wins!")
            return True
        if not legal_moves(self.board, self.player):
            print(f"{self.player} has no legal moves. {self.opponent()} wins!")
            return True
        return False

    def parse_move(self, raw):
        """Validate raw input; return (start, end) or None after printing why."""
        if len(raw) != 4:
            print("Enter four coordinates.")
            return None
        try:
            sr, sc, er, ec = map(int, raw)
        except ValueError:
            print("Coordinates must be numbers.")
            return None
        if not all(0 <= x < SIZE for x in (sr, sc, er, ec)):
            print("Outside board.")
            return None
        if owner(self.board[sr][sc]) != self.player:
            print("That is not your piece.")
            return None
        return (sr, sc), (er, ec)

    def apply_move(self, start, end):
        """Make one accepted move and print exactly one result line."""
        captured = move_piece(self.board, start, end)
        promoted = promote(self.board)
        msg = f"{self.player} {'captures' if captured else 'moves'} {fmt(start)} -> {fmt(end)}"
        if captured:
            msg += f" (took {fmt(captured)})"
        if promoted:
            msg += " and is promoted to king"

        self.chain = None
        # Turn continues only after a capture, if not just promoted
        if captured and not promoted and captures_from(self.board, self.player, end):
            self.chain = end
            msg += f". Jump again with {fmt(end)}"
        else:
            self.player = self.opponent()
        print(msg)

    def run(self):
        print("Checkers — move: sr sc er ec   (q to quit)")
        while True:
            self.print_board()
            if self.game_over():
                return
            try:
                raw = input(f"{self.player}> ").strip().lower().split()
            except EOFError:
                return
            if raw == ["q"]:
                return
            parsed = self.parse_move(raw)
            if parsed is None:
                continue
            start, end = parsed

            legal = legal_moves(self.board, self.player, self.chain)
            if (start, end) not in legal:
                if self.chain is not None:
                    print(f"You must continue capturing with {fmt(self.chain)}.")
                elif any(abs(e[0] - s[0]) == 2 for s, e in legal):
                    print("A capture is available; you must capture.")
                else:
                    print("Invalid move.")
                continue
            self.apply_move(start, end)