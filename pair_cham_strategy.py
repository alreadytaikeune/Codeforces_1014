#! encoding=utf8
from __future__ import absolute_import, unicode_literals, print_function
from collections import Counter
import string

N = 100000
S = 10000
C = 10
H = 10
U = 10

letters = list(string.ascii_uppercase)[:H]
lti = dict(zip(letters, range(10)))

_ = raw_input()
stripe = raw_input()
bottles = raw_input()
actions = []
positions = range(10)
bottles_in_hand = Counter(bottles[:H])
idx_in_bottles = H

pairs = {}
# idx = {}
for i, c in enumerate(letters):
    pairs[c] = (i, (i+1) % 10)
    # idx[c] = 0


def findnext(pos, color):
    while stripe[pos % N] != color or pos in positions:
        pos += 1
    return pos % N


for s in range(H+S):
    color = bottles[s]
    u1, u2 = pairs[color]
    p1 = positions[u1]
    p2 = positions[u2]
    if p1 < p2:
        p = p1
        u = u1
    else:
        p = p2
        u = u2
    np = findnext(p, color)
    positions[u] = np

    print("{} {}".format(u, color))
