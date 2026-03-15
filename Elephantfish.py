#!/usr/bin/env pypy
# -*- coding: utf-8 -

from __future__ import print_function
import re, sys, time
from itertools import count
from collections import namedtuple

piece = { 'P': 44, 'N': 108, 'B': 23, 'R': 233, 'A': 23, 'C': 101, 'K': 2500}

# 子力价值表参考"象眼"

pst = {
    "P": (
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  9,  9,  9, 11, 13, 11,  9,  9,  9,  0,  0,  0,  0,
      0,  0,  0, 19, 24, 34, 42, 44, 42, 34, 24, 19,  0,  0,  0,  0,
      0,  0,  0, 19, 24, 32, 37, 37, 37, 32, 24, 19,  0,  0,  0,  0,
      0,  0,  0, 19, 23, 27, 29, 30, 29, 27, 23, 19,  0,  0,  0,  0,
      0,  0,  0, 14, 18, 20, 27, 29, 27, 20, 18, 14,  0,  0,  0,  0,
      0,  0,  0,  7,  0, 13,  0, 16,  0, 13,  0,  7,  0,  0,  0,  0,
      0,  0,  0,  7,  0,  7,  0, 15,  0,  7,  0,  7,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  1,  1,  1,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  2,  2,  2,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0, 11, 15, 11,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0
    ),
    "B":(
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0, 40,  0,  0,  0, 40,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0, 38,  0,  0, 40, 43, 40,  0,  0, 38,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0, 43,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0, 40, 40,  0, 40, 40,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0
    ),
    "N": (
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0, 90, 90, 90, 96, 90, 96, 90, 90, 90,  0,  0,  0,  0,
      0,  0,  0, 90, 96,103, 97, 94, 97,103, 96, 90,  0,  0,  0,  0,
      0,  0,  0, 92, 98, 99,103, 99,103, 99, 98, 92,  0,  0,  0,  0,
      0,  0,  0, 93,108,100,107,100,107,100,108, 93,  0,  0,  0,  0,
      0,  0,  0, 90,100, 99,103,104,103, 99,100, 90,  0,  0,  0,  0,
      0,  0,  0, 90, 98,101,102,103,102,101, 98, 90,  0,  0,  0,  0,
      0,  0,  0, 92, 94, 98, 95, 98, 95, 98, 94, 92,  0,  0,  0,  0,
      0,  0,  0, 93, 92, 94, 95, 92, 95, 94, 92, 93,  0,  0,  0,  0,
      0,  0,  0, 85, 90, 92, 93, 78, 93, 92, 90, 85,  0,  0,  0,  0,
      0,  0,  0, 88, 85, 90, 88, 90, 88, 90, 85, 88,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0
    ),
    "R": (
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,206,208,207,213,214,213,207,208,206,  0,  0,  0,  0,
      0,  0,  0,206,212,209,216,233,216,209,212,206,  0,  0,  0,  0,
      0,  0,  0,206,208,207,214,216,214,207,208,206,  0,  0,  0,  0,
      0,  0,  0,206,213,213,216,216,216,213,213,206,  0,  0,  0,  0,
      0,  0,  0,208,211,211,214,215,214,211,211,208,  0,  0,  0,  0,
      0,  0,  0,208,212,212,214,215,214,212,212,208,  0,  0,  0,  0,
      0,  0,  0,204,209,204,212,214,212,204,209,204,  0,  0,  0,  0,
      0,  0,  0,198,208,204,212,212,212,204,208,198,  0,  0,  0,  0,
      0,  0,  0,200,208,206,212,200,212,206,208,200,  0,  0,  0,  0,
      0,  0,  0,194,206,204,212,200,212,204,206,194,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0
    ),
    "C": (
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,100,100, 96, 91, 90, 91, 96,100,100,  0,  0,  0,  0,
      0,  0,  0, 98, 98, 96, 92, 89, 92, 96, 98, 98,  0,  0,  0,  0,
      0,  0,  0, 97, 97, 96, 91, 92, 91, 96, 97, 97,  0,  0,  0,  0,
      0,  0,  0, 96, 99, 99, 98,100, 98, 99, 99, 96,  0,  0,  0,  0,
      0,  0,  0, 96, 96, 96, 96,100, 96, 96, 96, 96,  0,  0,  0,  0,
      0,  0,  0, 95, 96, 99, 96,100, 96, 99, 96, 95,  0,  0,  0,  0,
      0,  0,  0, 96, 96, 96, 96, 96, 96, 96, 96, 96,  0,  0,  0,  0,
      0,  0,  0, 97, 96,100, 99,101, 99,100, 96, 97,  0,  0,  0,  0,
      0,  0,  0, 96, 97, 98, 98, 98, 98, 98, 97, 96,  0,  0,  0,  0,
      0,  0,  0, 96, 96, 97, 99, 99, 99, 97, 96, 96,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0
    )
}

pst["A"] = pst["B"]
pst["K"] = pst["P"]
pst["K"] = [i + piece["K"] if i > 0 else 0 for i in pst["K"]]

A0, I0, A9, I9 = 12 * 16 + 3,12 * 16 + 11, 3 * 16 + 3,  3 * 16 + 11

initial = (
    '               \n'  #   0 -  9
    '               \n'  #  10 - 19
    '               \n'  #  10 - 19
    '   rnbakabnr   \n'  #  20 - 29
    '   .........   \n'  #  40 - 49
    '   .c.....c.   \n'  #  40 - 49
    '   p.p.p.p.p   \n'  #  30 - 39
    '   .........   \n'  #  50 - 59
    '   .........   \n'  #  70 - 79
    '   P.P.P.P.P   \n'  #  80 - 89
    '   .C.....C.   \n'  #  70 - 79
    '   .........   \n'  #  70 - 79
    '   RNBAKABNR   \n'  #  90 - 99
    '               \n'  # 100 -109
    '               \n'  # 100 -109
    '               \n'  # 110 -119
)

N, E, S, W = -16, 1, 16, -1
directions = {
    'P': (N, W, E),
    'N': (N+N+E, E+N+E, E+S+E, S+S+E, S+S+W, W+S+W, W+N+W, N+N+W),
    'B': (2 * N + 2 * E, 2 * S + 2 * E, 2 * S + 2 * W, 2 * N + 2 * W),
    'R': (N, E, S, W),
    'C': (N, E, S, W),
    'A': (N+E, S+E, S+W, N+W),
    'K': (N, E, S, W)
}

MATE_LOWER = piece['K'] - (2*piece['R'] + 2*piece['N'] + 2*piece['B'] + 2*piece['A'] + 2*piece['C'] + 5*piece['P'])
MATE_UPPER = piece['K'] + (2*piece['R'] + 2*piece['N'] + 2*piece['B'] + 2*piece['A'] + 2*piece['C'] + 5*piece['P'])

TABLE_SIZE = 1e7
QS_LIMIT = 219
EVAL_ROUGHNESS = 13
DRAW_TEST = True
THINK_TIME = 5

class Position(namedtuple('Position', 'board score')):
    def gen_moves(self):
        for i, p in enumerate(self.board):
            if p == 'K':
                for scanpos in range(i - 16,A9,-16):
                    if self.board[scanpos] == 'k':
                        yield (i,scanpos)
                    elif self.board[scanpos] != '.':
                        break
            if not p.isupper(): continue
            if p == 'C':
                for d in directions[p]:
                    cfoot = 0
                    for j in count(i+d, d):
                        q = self.board[j]
                        if q.isspace():break
                        if cfoot == 0 and q == '.':yield (i,j)
                        elif cfoot == 0 and q != '.':cfoot += 1
                        elif cfoot == 1 and q.islower(): yield (i,j);break
                        elif cfoot == 1 and q.isupper(): break;
                continue
            for d in directions[p]:
                for j in count(i+d, d):
                    q = self.board[j]
                    if q.isspace() or q.isupper(): break
                    if p == 'P' and d in (E, W) and i > 128: break
                    elif p in ('A','K') and (j < 160 or j & 15 > 8 or j & 15 < 6): break
                    elif p == 'B' and j < 128: break
                    elif p == 'N':
                        n_diff_x = (j - i) & 15
                        if n_diff_x == 14 or n_diff_x == 2:
                            if self.board[i + (1 if n_diff_x == 2 else -1)] != '.': break
                        else:
                            if j > i and self.board[i + 16] != '.': break
                            elif j < i and self.board[i - 16] != '.': break
                    elif p == 'B' and self.board[i + d // 2] != '.':break
                    yield (i, j)
                    if p in 'PNBAK' or q.islower(): break

    def rotate(self):
        return Position(self.board[-2::-1].swapcase() + " ", -self.score)

    def nullmove(self):
        return self.rotate()

    def move(self, move):
        i, j = move
        put = lambda board, i, p: board[:i] + p + board[i+1:]
        board = self.board
        score = self.score + self.value(move)
        board = put(board, j, board[i])
        board = put(board, i, '.')
        return Position(board, score).rotate()

    def value(self, move):
        i, j = move
        p, q = self.board[i], self.board[j]
        score = pst[p][j] - pst[p][i]
        if q.islower():
            score += pst[q.upper()][255-j-1]
        return score

Entry = namedtuple('Entry', 'lower upper')

class Searcher:
    def __init__(self):
        self.tp_score = {}
        self.tp_move = {}
        self.history = set()
        self.nodes = 0

    def bound(self, pos, gamma, depth, root=True):
        self.nodes += 1
        depth = max(depth, 0)
        if pos.score <= -MATE_LOWER:
            return -MATE_UPPER
        if DRAW_TEST:
            if not root and pos in self.history:
                return 0
        entry = self.tp_score.get((pos, depth, root), Entry(-MATE_UPPER, MATE_UPPER))
        if entry.lower >= gamma and (not root or self.tp_move.get(pos) is not None):
            return entry.lower
        if entry.upper < gamma:
            return entry.upper
        def moves():
            if depth > 0 and not root and any(c in pos.board for c in 'RNC'):
                yield None, -self.bound(pos.nullmove(), 1-gamma, depth-3, root=False)
            if depth == 0:
                yield None, pos.score
            killer = self.tp_move.get(pos)
            if killer and (depth > 0 or pos.value(killer) >= QS_LIMIT):
                yield killer, -self.bound(pos.move(killer), 1-gamma, depth-1, root=False)
            for move in sorted(pos.gen_moves(), key=pos.value, reverse=True):
                if depth > 0 or pos.value(move) >= QS_LIMIT:
                    yield move, -self.bound(pos.move(move), 1-gamma, depth-1, root=False)
        best = -MATE_UPPER
        for move, score in moves():
            best = max(best, score)
            if best >= gamma:
                if len(self.tp_move) > TABLE_SIZE: self.tp_move.clear()
                self.tp_move[pos] = move
                break
        if best < gamma and best < 0 and depth > 0:
            is_dead = lambda pos: any(pos.value(m) >= MATE_LOWER for m in pos.gen_moves())
            if all(is_dead(pos.move(m)) for m in pos.gen_moves()):
                in_check = is_dead(pos.nullmove())
                best = -MATE_UPPER if in_check else 0
        if len(self.tp_score) > TABLE_SIZE: self.tp_score.clear()
        if best >= gamma:
            self.tp_score[pos, depth, root] = Entry(best, entry.upper)
        if best < gamma:
            self.tp_score[pos, depth, root] = Entry(entry.lower, best)
        return best

    def search(self, pos, history=()):
        self.nodes = 0
        if DRAW_TEST:
            self.history = set(history)
            self.tp_score.clear()
        for depth in range(1, 1000):
            lower, upper = -MATE_UPPER, MATE_UPPER
            while lower < upper - EVAL_ROUGHNESS:
                gamma = (lower+upper+1)//2
                score = self.bound(pos, gamma, depth)
                if score >= gamma:
                    lower = score
                if score < gamma:
                    upper = score
            self.bound(pos, lower, depth)
            yield depth, self.tp_move.get(pos), self.tp_score.get((pos, depth, True),Entry(-MATE_UPPER, MATE_UPPER)).lower

if sys.version_info[0] == 2:
    input = raw_input

def parse(c):
    fil, rank = ord(c[0]) - ord('a'), int(c[1])
    return A0 + fil - 16*rank

def render(i):
    rank, fil = divmod(i - A0, 16)
    return chr(fil + ord('a')) + str(-rank)

def print_pos(pos):
    print()
    uni_pieces = {'R':'车', 'N':'马', 'B':'相', 'A':'仕', 'K':'帅', 'P':'兵', 'C':'炮',
                  'r':'俥', 'n':'傌', 'b':'象', 'a':'士', 'k':'将', 'p':'卒', 'c':'砲', '.':'．'}
    for i, row in enumerate(pos.board.split()):
        print(' ', 9-i, ''.join(uni_pieces.get(p, p) for p in row))
    print('    ａｂｃｄｅｆｇｈｉ\n\n')

def main():
    hist = [Position(initial, 0)]
    searcher = Searcher()
    while True:
        print_pos(hist[-1])
        if hist[-1].score <= -MATE_LOWER:
            print("You lost")
            break
        move = None
        while move not in hist[-1].gen_moves():
            match = re.match('([a-i][0-9])'*2, input('Your move: '))
            if match:
                move = parse(match.group(1)), parse(match.group(2))
            else:
                print("Please enter a move like h2e2")
        hist.append(hist[-1].move(move))
        print_pos(hist[-1].rotate())
        if hist[-1].score <= -MATE_LOWER:
            print("You won")
            break
        start = time.time()
        for _depth, move, score in searcher.search(hist[-1], hist):
            if time.time() - start > THINK_TIME:
                break
        if score == MATE_UPPER:
            print("Checkmate!")
        print("Think depth: {} My move: {}".format(_depth, render(255-move[0] - 1) + render(255-move[1]-1)))
        hist.append(hist[-1].move(move))

if __name__ == '__main__':
    main()