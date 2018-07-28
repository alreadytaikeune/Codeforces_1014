#! encoding=utf8
from __future__ import unicode_literals, print_function, absolute_import
import string
import threading
from Queue import Queue, Full, Empty
from subprocess import Popen, PIPE
import numpy as np
from tabulate import tabulate

N = 100000
S = 10000
C = 10
H = 10
U = 10

LETTERS = list(string.ascii_uppercase)[:H]
ERROR_FLAG = False
LOCK = threading.Lock()


def get_err_flag():
    global LOCK
    global ERROR_FLAG
    with LOCK:
        return ERROR_FLAG


def raise_err_flag():
    global LOCK
    global ERROR_FLAG
    with LOCK:
        ERROR_FLAG = True


def give_me_a_test():
    out = []
    out.append("{} {} {} {} {}".format(N, S, C, H, U))

    stripe = np.random.choice(LETTERS, (N,))
    bottles = np.random.choice(LETTERS, (H+S,))
    out.append("".join(stripe))
    out.append("".join(bottles))
    return "\n".join(out) + "\n"


def get_from_queue(queue):
    while True:
        try:
            return queue.get(timeout=0.1)
        except Empty:
            if get_err_flag():
                raise RuntimeError("Error flag raised")


def put_in_queue(queue, v):
    while True:
        try:
            return queue.put(v, timeout=0.1)
        except Full:
            if get_err_flag():
                raise RuntimeError("Error flag raised")


def run_script_thread(script_name, tests_queue, score_queue):

    def _run_script(script, inp):
        p = Popen(["python", script], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate(input=inp)
        if p.returncode != 0:
            tests_queue.task_done()
            score_queue.put(None)
            raise_err_flag()
            raise RuntimeError(
                "Got error while running script {}: {}".format(script, stderr))
        return stdout

    while True:
        test = get_from_queue(tests_queue)
        if test is None:
            tests_queue.task_done()
            print("No more test... exiting thread")
            return
        try:
            sol = _run_script(script_name, test)
            score = _run_script("evaluation_script.py", test+sol)
            score_queue.put(int(score))
            tests_queue.task_done()
        except Exception as e:
            raise_err_flag()
            raise ValueError("Got unhandled exception {}".format(e))


def run_for_script(script_name):
    WORKERS = 2
    RUN_ON_N = 10
    tests_queue = Queue(100)
    scores_queue = Queue(100)
    threads = []
    print("Starting {} workers..".format(WORKERS))
    for w in range(WORKERS):
        t = threading.Thread(
            target=run_script_thread,
            args=(script_name, tests_queue, scores_queue))
        t.daemon = True
        threads.append(t)
        t.start()
    print("Starting to generate {} tests".format(RUN_ON_N))
    for _ in range(RUN_ON_N):
        put_in_queue(tests_queue, give_me_a_test())
    for _ in range(WORKERS):
        put_in_queue(tests_queue, None)
    if get_err_flag():
        exit(1)
    print("All tests have been sent, waiting for results...")
    for t in threads:
        t.join()
    scores = []
    for i in range(RUN_ON_N):
        scores.append(get_from_queue(scores_queue))
        scores_queue.task_done()

    return np.array(scores)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("scripts", nargs='+')
    args = parser.parse_args()
    scores = []
    for sname in args.scripts:
        print("Running evaluation on script {}".format(sname))
        s = run_for_script(sname)
        best = np.max(s)
        worst = np.min(s)
        avg = np.mean(s)
        std = np.std(s)
        scores.append((sname, best, worst, avg, std))
        print("Best: {}".format(best))
        print("Worst: {}".format(worst))
        print("Std dev: {:.2f}".format(avg))
        print("Average score: {:.2f}".format(std))

    res = tabulate(
        scores, ("Name", "Best", "Worst", "Average", "Std dev"),
        tablefmt="pipe")
    print(res)
    with open("Standings.md", "w") as _:
        _.write(res)
