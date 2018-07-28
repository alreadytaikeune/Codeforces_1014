#! encoding=utf8
from __future__ import absolute_import, unicode_literals, print_function
from collections import Counter
N = 100000
S = 10000
C = 10
H = 10
U = 10

constants = raw_input()

# Start reading test
stripe = raw_input()
bottles = raw_input()

# start reading solution
actions = []
for _ in range(S):
    actions.append([int(x) for x in raw_input().strip().split()])


# compute the score

chameleons = range(C)
bottles_in_hand = Counter(bottles[:H])
idx_bottles = H
for u, c in actions:
    if Counter[c] == 0:
        raise ValueError("Trying to use a bottle not in hand")
    Counter[c] -= 1
    Counter[idx_bottles] += 1
    idx_bottles += 1
    idx_cham = chameleons[u]
    new_pos_stripe = idx_cham + 1
    while stripe[new_pos_stripe] != c and \
            new_pos_stripe not in chameleons.values():
        new_pos_stripe += 1
    chameleons[u] = new_pos_stripe

print(min(chameleons))
