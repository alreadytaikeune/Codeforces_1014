#! encoding=utf8
from __future__ import absolute_import, unicode_literals, print_function


n, s, c, h, u = [int(k) for k in raw_input().split(" ")]

tl = "ABCDEFGHIJ"

t = dict(zip("ABCDEFGHIJ", range(10)))

pat = [t[k] for k in raw_input()]
bot = [t[k] for k in raw_input()]
tn = [[] for i in range(10)]

for i in range(n):
    tn[pat[i]] += [i]

nexti = [[] for i in range(10)]

for i in range(10):
    for j in range(len(tn[i])):
        nxt = tn[i][(j+1) % n]
        for k in range(tn[i][j], nxt):
            nexti[i][k] = nxt

z = range(10)


def findnext(wfrom, color):
    wfrom = wfrom % n
    while nexti[color][wfrom] in z:
        wfrom = nexti[color][wfrom]
    return (nexti[color][wfrom]-wfrom) % n


m = [[None for i in range(10)] for j in range(10)]

for i in range(10):
    for col in range(10):
        nxt = findnext(z[i])
        m[i][col] = nxt

mz = max(z)


def margmax(poss=range(10)):
    mx = 0
    res = None
    for i in range(10):
        for j in poss:
            if m[i][j]*(mz+10-z[i]) > mx:
                res = (i, j)
                mx = m[i][j]*(mz+10-z[i])
    return res


rr = []

for i in bot:
    best = margmax([i])
    bg = best[0]
    rr += [best]
    for j in range(10):
        if j != bg and z[j]+(nexti[i][bg]-z[j]) % n == z[bg]:
            m[j][i] = z[bg]
    z[bg] += m[bg][i]
    for col in range(10):
        m[bg][col] = findnext(z[i])
    print(best[0], tl[best[1]])
