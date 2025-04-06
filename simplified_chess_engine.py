from copy import deepcopy


def moveGenerator(board, row, col, piece):
    n = len(board)
    directions = {
        "knight": [
            (-2, -1),
            (-2, 1),
            (-1, -2),
            (-1, 2),
            (1, -2),
            (1, 2),
            (2, -1),
            (2, 1),
        ],
        "Bishop": [(-1, +1), (+1, -1), (-1, -1), (+1, +1)],
        "Rook": [(+1, 0), (-1, 0), (0, +1), (0, -1)],
        "Queen": [
            (-1, +1),
            (+1, -1),
            (-1, -1),
            (+1, +1),
            (+1, 0),
            (-1, 0),
            (0, +1),
            (0, -1),
        ],
    }

    valid_moves = []

    if piece == "knight":
        for dr, dc in directions["knight"]:
            r, c = row + dr, col + dc
            if (
                0 <= r < n
                and 0 <= c < n
                and (board[r][c] == " " or board[r][c][0] == "B")
            ):
                valid_moves.append((r, c))

    else:
        for dr, dc in directions[piece]:
            r, c = row + dr, col + dc
            while 0 <= r < n and 0 <= c < n:
                if board[r][c] == " " or board[r][c][0] == "B":
                    valid_moves.append((r, c))
                if board[r][c] != " ":
                    break
                r += dr
                c += dc

    return valid_moves


def canWin(board, m, black_queen_pos):
    """Check if white can capture the black queen in m moves or fewer."""
    if m <= 0:
        return False

    # Find all white pieces
    white_pieces = []
    for r in range(4):
        for c in range(4):
            if board[r][c].startswith("W"):
                piece_type = (
                    "Queen"
                    if board[r][c][1] == "Q"
                    else (
                        "Rook"
                        if board[r][c][1] == "R"
                        else ("Bishop" if board[r][c][1] == "B" else "knight")
                    )
                )
                white_pieces.append((r, c, piece_type))

    # Try each white piece's moves
    for row, col, piece_type in white_pieces:
        valid_moves = moveGenerator(board, row, col, piece_type)

        # Check if we can directly capture the queen
        if black_queen_pos in valid_moves:
            return True

        # Try each possible move and check if it leads to a win
        for new_row, new_col in valid_moves:
            new_board = deepcopy(board)
            # Move the piece
            new_board[new_row][new_col] = new_board[row][col]
            new_board[row][col] = " "

            # Recursively check if we can win in m-1 moves
            if canWin(new_board, m - 1, black_queen_pos):
                return True

    return False


def simplified_chess_engine(whites, blacks, m):
    board = [[" "] * 4 for _ in range(4)]

    for piece in whites:
        piece_type = piece[0]
        col = ord(piece[-2]) - ord("A")
        row = int(piece[-1]) - 1
        board[row][col] = "W" + piece_type

    for piece in blacks:
        piece_type = piece[0]
        col = ord(piece[-2]) - ord("A")
        row = int(piece[-1]) - 1
        board[row][col] = "B" + piece_type

        # Find the black queen position
        if piece_type == "Q":
            black_queen_pos = (row, col)

    if "black_queen_pos" not in locals():
        return False
    # Check if white can win
    return canWin(board, m, black_queen_pos)


if __name__ == "__main__":
    whites = ["RB2"]
    blacks = ["QD3"]
    m = 2
    print(simplified_chess_engine(whites, blacks, m))  # ✅ Output: True
