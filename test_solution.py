#! encoding=utf8
from __future__ import unicode_literals, print_function, absolute_import
import sys
import string
import threading
from Queue import Queue, Full, Empty
from subprocess import Popen, PIPE
import numpy as np

N = 100000
S = 10000
C = 10
H = 10
U = 10

LETTERS = list(string.ascii_uppercase)[:H]
ERROR_FLAG = False
LOCK = threading.LOCK


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
    return "\n".join(out)


def get_from_queue(queue):
    while True:
        try:
            return queue.get(timeout=0.1)
        except Empty:
            if get_err_flag():
                raise RuntimeError("Error flag raised")


def put_from_queue(queue, v):
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
                "Got error while running script {}".format(stderr))
        return stdout

    while True:
        test = get_from_queue(tests_queue)
        if test is None:
            tests_queue.task_done()
            return
        try:
            sol = _run_script(script_name, test)
            score = _run_script("evaluate_solution.py", test+sol)
            score_queue.put(int(score))
            tests_queue.task_done()
        except Exception as e:
            raise_err_flag()
            raise ValueError("Got unhandled exception {}".format(e))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./test_script.py script")
    script_name = sys.argv[2]
    WORKERS = 2
    RUN_ON_N = 10
    tests_queue = Queue(100)
    scores_queue = Queue(100)
    threads = []
    for w in range(WORKERS):
        t = threading.Thread(
            run_script_thread, args=(script_name, tests_queue, scores_queue))
        t.daemon = True
        threads.append(t)
        t.start()
    for _ in range(RUN_ON_N):
        tests_queue.put(give_me_a_test())

    for _ in range(WORKERS):
        tests_queue.put(None)
    for t in threads:
        t.join()
    scores = []
    for i in range(RUN_ON_N):
        scores.append(scores_queue.get())
        scores_queue.task_done()

    scores = np.array(scores)
    print("Run results for {}. Based on {} values".format(
        script_name, RUN_ON_N))
    print("Average score: {:.2f}".format(np.mean(scores)))
    print("Best: {}".format(np.max(scores)))
    print("Worst: {}".format(np.min(scores)))
    print("Std dev: {:.2f}".format(np.stddev(scores)))
