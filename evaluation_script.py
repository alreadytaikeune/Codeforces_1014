#! encoding=utf8
from __future__ import absolute_import, unicode_literals, print_function
import sys
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

assert len(stripe) == N
assert len(bottles) == H+S
# start reading solution
actions = []
for _ in range(S):
    actions.append(raw_input().split())


# compute the score


chameleons = range(C)
bottles_in_hand = Counter(bottles[:H])
idx_bottles = H
for i, (u, c) in enumerate(actions):
    u = int(u)
    if bottles_in_hand[c] == 0:
        sys.stderr.write(str(c) + "\n")
        sys.stderr.write(str(bottles_in_hand) + "\n")
        raise ValueError(
            "Error executing action {}. Trying to use a bottle not in hand".format(i))
    bottles_in_hand[c] -= 1
    bottles_in_hand[bottles[idx_bottles]] += 1
    idx_bottles += 1
    idx_cham = chameleons[u]
    new_pos_stripe = idx_cham + 1
    while stripe[new_pos_stripe % N] != c or \
            new_pos_stripe in chameleons:
        new_pos_stripe += 1
    chameleons[u] = new_pos_stripe

print(min(chameleons))
print()
