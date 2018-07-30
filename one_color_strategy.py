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


def findnext(pos, color):
    while stripe[pos % N] != color or pos in positions:
        pos += 1
    return pos % N


for s in range(H+S):
    color = bottles[s]
    u = lti[color]
    p = positions[u]
    np = findnext(p, color)
    positions[u] = np

    print("{} {}".format(u, color))
