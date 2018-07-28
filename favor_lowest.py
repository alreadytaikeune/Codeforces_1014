#! encoding=utf8
from __future__ import absolute_import, unicode_literals, print_function
from collections import Counter
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
idx_in_bottles = H


def findnext(pos, color):
    while stripe[pos] != color and pos not in positions:
        pos += 1
    return pos


for s in range(S):
    min_pos = positions[0]
    idx = 0
    for i, p in enumerate(positions):
        if p < min_pos:
            min_pos = p
            idx = i
    max_pos = min_pos
    best_c = None
    for b in bottles_in_hand:
        if bottles_in_hand[b] > 0:
            v = findnext(min_pos+1, b)
            if v > max_pos:
                max_pos = v
                best_c = b
    assert best_c is not None
    positions[idx] = max_pos
    bottles_in_hand[best_c] -= 1
    bottles_in_hand[bottles[idx_in_bottles]] += 1
    idx_in_bottles += 1
    print("{} {}".format(idx, best_c))
