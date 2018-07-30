#! encoding=utf8
from __future__ import absolute_import, unicode_literals, print_function
from collections import Counter
import random
import itertools
import copy

N = 100000
S = 10000
C = 10
H = 10
U = 10
_ = raw_input()
stripe = raw_input()
bottles = raw_input()
actions = []
positions = range(10)
bottles_in_hand = Counter(bottles[:H])


def findnext(pos, color):
    while stripe[pos%N] != color or pos in positions:
        pos += 1
    return pos


def get_lowest_update(positions, bottles_in_hand):
    idx = 0
    col = None
    next_pos = None
    min_pos = positions[0]
    for i, p in enumerate(positions):
        if p < min_pos:
            min_pos = p
            idx = i
    next_pos = min_pos
    for b in bottles_in_hand:
        if bottles_in_hand[b] > 0:
            v = findnext(min_pos+1, b)
            if v > next_pos:
                next_pos = v
                col = b
    return idx, next_pos, col


def get_greedy_update(positions, bottles_in_hand):
    # greedy
    tmp = 0
    for u in range(U):
        pos = positions[u]
        for b in bottles_in_hand:
            if bottles_in_hand[b] > 0:
                v = findnext(pos+1, b) - pos
                if v > tmp:
                    tmp = v
                    next_pos = v + pos
                    col = b
                    idx = u
    return idx, next_pos, col


def get_greedy_update2(positions, bottles_in_hand):
    bottles = list(bottles_in_hand.elements())
    random.shuffle(bottles)
    bottles = bottles[:5]
    perms = list(itertools.permutations(bottles))
    p_done = set()
    best_score = 0
    for p in perms:
        pe = ''.join(p)
        if pe in p_done:
            continue
        assgn = {}
        for b_i, b in enumerate(p):
            tmp = 0
            best_u = None
            new_pos = None
            u_done = set()
            for u in range(U):
                if u in u_done:
                    continue
                pos = positions[u]
                v = findnext(pos+1, b) - pos
                if v > tmp:
                    tmp = v
                    best_u = u
                    new_pos = v+pos
                u_done.add(u)
            assgn[b_i] = (best_u, new_pos)
        new_p = copy.deepcopy(positions)
        for b_i, b in enumerate(p):
            new_p[assgn[b_i][0]] = assgn[b_i][1]

        score = min(new_p)
        if score > best_score:
            best_perm = p
            best_assgn = assgn

        p_done.add(pe)

    updates = []
    for b_i, b in enumerate(best_perm):
        updates.append((best_assgn[b_i][0], best_assgn[b_i][1], b))
    return updates


idx_in_bottles = H
while idx_in_bottles < S:

    # idx1, next_pos1, col1 = get_lowest_update(positions, bottles_in_hand)
    idx2, next_pos2, col2 = get_greedy_update(positions, bottles_in_hand)

    # incr1 = (next_pos1 - positions[idx1])
    # incr2 = (next_pos2 - positions[idx2])/3.
    # # print(incr1, incr2)

    # p1 = float(incr1)/(incr1 + incr2)
    # eps = random.random()
    # if eps < p1:
    #     idx, next_pos, col = idx1, next_pos1, col1
    # else:
    #     idx, next_pos, col = idx2, next_pos2, col2
    sol = get_greedy_update2(positions, bottles_in_hand)
    for idx, next_pos, col in sol:
        assert col is not None
        assert next_pos is not None
        assert bottles_in_hand[col] > 0

        positions[idx] = next_pos
        bottles_in_hand[col] -= 1
        bottles_in_hand[bottles[idx_in_bottles + H]] += 1
        # print("{} {}".format(idx, col))
        idx_in_bottles += 1
print(positions)
