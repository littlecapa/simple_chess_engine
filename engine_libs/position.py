from collections import namedtuple
from const import directions, N, S, W, E, A1, H1, A8, H8, squares
from itertools import count
from eval import Eval as e
from values import Values as v

import pdb

class Position(namedtuple('Position', 'board score wc bc ep kp')):
    """ A state of a chess game
    board -- a 120 char representation of the board
    score -- the board evaluation
    wc -- the castling rights, [west/queen side, east/king side]
    bc -- the opponent castling rights, [west/king side, east/queen side]
    ep - the en passant square
    kp - the king passant square
    """
    # side_to_move = 1

    def __init__(self, board, score, wc, bc, ep, kp):
        super().__init__(board = board, score = score, wc = wc, bc = bc, ep = ep, kp = kp)
        self.evaluator = e()
        self.values = v()

    def gen_moves(self):
        # For each of our pieces, iterate through each possible 'ray' of moves,
        # as defined in the 'directions' map. The rays are broken e.g. by
        # captures or immediately in case of pieces such as knights.
        for i, p in enumerate(self.board):
            if not p.isupper(): continue
            for d in directions[p]:
                for j in count(i+d, d):
                    q = self.board[j]
                    # Stay inside the board, and off friendly pieces
                    if q.isspace() or q.isupper(): break
                    # Pawn move, double move and capture
                    if p == 'P' and d in (N, N+N) and q != '.': break
                    if p == 'P' and d == N+N and (i < A1+N or self.board[i+N] != '.'): break
                    if p == 'P' and d in (N+W, N+E) and q == '.' \
                            and j not in (self.ep, self.kp, self.kp-1, self.kp+1): break
                    # Move it
                    yield (i, j)
                    # Stop crawlers from sliding, and sliding after captures
                    if p in 'PNK' or q.islower(): break
                    # Castling, by sliding the rook next to the king
                    if i == A1 and self.board[j+E] == 'K' and self.wc[0]: yield (j+E, j+W)
                    if i == H1 and self.board[j+W] == 'K' and self.wc[1]: yield (j+W, j+E)

    def rotate(self):
        ''' Rotates the board, preserving enpassant '''
        # self.side_to_move = 2
        return Position(
            self.board[::-1].swapcase(), -self.score, self.bc, self.wc,
            119-self.ep if self.ep else 0,
            119-self.kp if self.kp else 0)

    def nullmove(self):
        ''' Like rotate, but clears ep and kp '''
        return Position(
            self.board[::-1].swapcase(), -self.score,
            self.bc, self.wc, 0, 0)

    def move(self, move):
        i, j = move
        p, q = self.board[i], self.board[j]
        
        score = self.score + self.value(move)

        board, ep, wc, bc, kp = self.set_board(self.board, i, j, p, q)

        # We rotate the returned position, so it's ready for the next player
        return Position(board, score, wc, bc, ep, kp).rotate()

    def set_start_board(self, board):
        return board, self.ep, self.wc, self.bc

    def set_board(self, board, i, j, p, q):
        put = lambda board, i, p: board[:i] + p + board[i+1:]
        end_board = board
        end_wc, end_bc, end_ep, end_kp = self.wc, self.bc, 0, 0
        # continue preparing end fen
        # board post move
        end_board = put(end_board, j, end_board[i])
        end_board = put(end_board, i, '.')

        # continue preparing end fen
        # Castling rights, we move the rook or capture the opponent's
        if i == A1: end_wc = (False, end_wc[1])
        if i == H1: end_wc = (end_wc[0], False)
        if j == A8: end_bc = (end_bc[0], False)
        if j == H8: end_bc = (False, end_bc[1])

        # continue preparing end fen
        # Castling
        if p == 'K':
            end_wc = (False, False)
            if abs(j-i) == 2:
                end_kp = (i+j)//2
                end_board = put(end_board, A1 if j < i else H1, '.')
                end_board = put(end_board, end_kp, 'R')

        # final stretch of end fen
        # Pawn promotion, double move and en passant capture
        if p == 'P':
            if A8 <= j <= H8:
                end_board = put(end_board, j, 'Q')
            if j - i == 2*N:
                end_ep = i + N
            if j == self.ep:
                end_board = put(end_board, j+S, '.')

        return end_board, end_ep, end_wc, end_bc, end_kp

    def handcrafted_value(self, i, j, p, q):
        # hce value eval
        hce_score = self.values.pst[p][j] - self.values.pst[p][i]

        if q.islower():
            hce_score += self.values.pst[q.upper()][119-j]

        # hce - Castling check detection
        if abs(j-self.kp) < 2:
            hce_score+= self.values.pst['K'][119-j]
        # hce - Castling
        if p == 'K' and abs(i-j) == 2:
            hce_score+= self.values.pst['R'][(i+j)//2]
            hce_score-= self.values.pst['R'][A1 if j < i else H1]
        # hce - Special pawn stuff
        if p == 'P':
            if A8 <= j <= H8:
                hce_score+= self.values.pst['Q'][j] - self.values.pst['P'][j]
            if j == self.ep:
                hce_score+= self.values.pst['P'][119-(j+S)]

        return hce_score

    def value(self, move):
        i, j = move
        p, q = self.board[i], self.board[j]
        
        # intiialize boards for fen generation
        start_board, start_ep, start_wc, start_bc = self.set_start_board(self.board)
        end_board, end_ep, end_wc, end_bc, _ = self.set_board(self.board, i, j, p, q)

        hce_score = self.handcrafted_value(i, j, p, q)

        # ensure that the game is not over by checking if the kings are still there
        # default to hce_score in a checkmate situation because NNUE doesn't have material value for the king
        if "K" in end_board and "k" in end_board and (hce_score < self.values.MATE_LOWER and hce_score > -self.values.MATE_LOWER):

            start_fen = self.fen(start_board, start_ep, start_wc, start_bc, white=True)
            end_fen = self.fen(end_board, end_ep, end_wc, end_bc, white=False)

            start_score = self.evaluator.get_score(start_fen)/2.08
            end_score = self.evaluator.get_score(end_fen)/-2.08
            
            #start_score = nnue.nnue_evaluate_fen(bytes(start_fen, encoding='utf-8'))/2.08
            #end_score = nnue.nnue_evaluate_fen(bytes(end_fen, encoding='utf-8'))/-2.08

            score = end_score - start_score
        else:
            score = hce_score

        return score

    def fen(self, board, ep, wc, bc, white=False):
        pieces = "rnbqkpRNBQKP"
        sq = 0
        fen = ""
        free_sq = 0
        last_char = ""

        for char in board:
            if sq % 8 == 0:
                free_sq = 0
            if char != " " and char != "\n":
                if char == ".":
                    last_char = char
                    sq += 1
                    free_sq += 1
                    if sq == 64:
                        fen += f"{free_sq}"
                if char in pieces:
                    if last_char == ".":
                        fen += f"{free_sq}"
                        free_sq = 0
                    last_char = char
                    fen += char
                    sq += 1
                if sq % 8 == 0:
                    if sq != 64:
                      if last_char == ".":
                          fen += f"{free_sq}"
                      fen += "/"
                      last_char = "/"

        if white:
            fen += " w "
        else:
            fen += " b "

        if wc[0] == False and wc[1] == False and bc[0] == False and bc[1] == False:
            fen += "-"
        if wc[0] == True:
            fen += "K"
        if wc[1] == True:
            fen += "Q"
        if bc[0] == True:
            fen += "k"
        if bc[1] == True:
            fen += "q"

        en_pass = squares[int(ep)]

        fen += f' {en_pass}'
        fen += ' - -'

        return fen
