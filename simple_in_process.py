#!/usr/bin/env python3

import heapq
import math
import string
import time

ALPHABETH = string.ascii_lowercase + ' .!'
TIMEIT_TIMES = 1000000
CANDIDATES_PER_ROUND = 10

time_fun = getattr(time, 'perf_counter_ns', time.time)


def vault(key):
    return key == 'this is the key to the vault. well done!'


def create_stmt(key_to_try):
    return lambda: vault(key_to_try)


def iter_candidates(prefix=''):
    for a in ALPHABETH:
        yield prefix + a


def min_timeit(func, number=1):
    result = math.inf
    for _ in range(number):
        start = time_fun()
        func()
        stop = time_fun()
        elapsed = stop - start
        if elapsed < result:
            result = elapsed
    return result


def create_measurement(key):
    return (-min_timeit(create_stmt(key), number=TIMEIT_TIMES), key)


def find_length():
    return [create_measurement(i * '.') for i in range(50)]


def main():
    print(find_length())
    
    tried = set()
    q = []
    processed_candidates = []

    for x in iter_candidates():
        tried.add(x)
        heapq.heappush(q, create_measurement(x))

    for _ in range(100):
        candidates = [heapq.heappop(q) for _ in range(CANDIDATES_PER_ROUND)]
        print(candidates)
        for candidate in candidates:
            heapq.heappush(processed_candidates, candidate)
            for x in iter_candidates(candidate[1]):
                if x not in tried:
                    tried.add(x)
                    heapq.heappush(q, create_measurement(x))
    
    print(min(q[0], processed_candidates[0]))


if __name__ == '__main__':
    main()
