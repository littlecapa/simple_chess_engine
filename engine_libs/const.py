## changing these values seem to trigger strange crashes in checkmating situations. best to keep this the same as what you want this engine for really is the NNUE
###############################################################################
# Global constants
###############################################################################

# Our board is represented as a 120 character string. The padding allows for
# fast detection of moves that don't stay within the board.
A1, H1, A8, H8 = 91, 98, 21, 28

squares = {
    21: "a8", 22: "b8", 23: "c8", 24: "d8", 25: "e8", 26: "f8", 27: "g8", 28: "h8",
    31: "a7", 32: "b7", 33: "c7", 34: "d7", 35: "e7", 36: "f7", 37: "g7", 38: "h7",
    41: "a6", 42: "b6", 43: "c6", 44: "d6", 45: "e6", 46: "f6", 47: "g6", 48: "h6",
    51: "a5", 52: "b5", 53: "c5", 54: "d5", 55: "e5", 56: "f5", 57: "g5", 58: "h5",
    61: "a4", 62: "b4", 63: "c4", 64: "d4", 65: "e4", 66: "f4", 67: "g4", 68: "h4",
    71: "a3", 72: "b3", 73: "c3", 74: "d3", 75: "e3", 76: "f3", 77: "g3", 78: "h3",
    81: "a2", 82: "b2", 83: "c2", 84: "d2", 85: "e2", 86: "f2", 87: "g2", 88: "h2",
    91: "a1", 92: "b1", 93: "c1", 94: "d1", 95: "e1", 96: "f1", 97: "g1", 98: "h1",
    0: "-"
}


initial = (
    '         \n'  #   0 -  9
    '         \n'  #  10 - 19
    ' rnbqkbnr\n'  #  20 - 29
    ' pppppppp\n'  #  30 - 39
    ' ........\n'  #  40 - 49
    ' ........\n'  #  50 - 59
    ' ........\n'  #  60 - 69
    ' ........\n'  #  70 - 79
    ' PPPPPPPP\n'  #  80 - 89
    ' RNBQKBNR\n'  #  90 - 99
    '         \n'  # 100 -109
    '         \n'  # 110 -119
)

# Lists of possible moves for each piece type.
N, E, S, W = -10, 1, 10, -1
directions = {
    'P': (N, N+N, N+W, N+E),
    'N': (N+N+E, E+N+E, E+S+E, S+S+E, S+S+W, W+S+W, W+N+W, N+N+W),
    'B': (N+E, S+E, S+W, N+W),
    'R': (N, E, S, W),
    'Q': (N, E, S, W, N+E, S+E, S+W, N+W),
    'K': (N, E, S, W, N+E, S+E, S+W, N+W)
}


# The table size is the maximum number of elements in the transposition table.
TABLE_SIZE = 1e7

# Constants for tuning search
QS_LIMIT = 213
EVAL_ROUGHNESS = 13
DRAW_TEST = True
