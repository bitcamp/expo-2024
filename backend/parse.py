import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy
from scipy import optimize
import itertools
from typing import List, Dict, Tuple, Optional
import random

hc = []
cap = []
#1 refers to index 0 (bloomberg), 2 refers to index 1 (costar)...
category_names = []

def process(csv_file):
    global category_names
    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        #for every each category row in the csv, split by commas to get each category
        for row in reader:
            categories = row[9].split(',')
            append = []
            for category in categories:
                if category.strip():
                    #for every category, ignore MLH
                    if not category.strip().endswith("Major League Hacking"):
                        #append it to the array for that hack
                        append.append(category.strip())
                        #if it isn't in the cap array, add it
                        if category.strip() not in cap:
                            cap.append(category.strip())
            hc.append(append)
        category_names = cap.copy()
        #assume one judging group for each category
        for i in range(0, len(cap)):
            cap[i] = 1

        #check if group signed up for more than three bitcamp categories. if true, remove bitcamp categories until = 3
        for sub_arr in hc:
            bitcamp_count = sum(1 for s in sub_arr if s.endswith('Bitcamp'))
            if bitcamp_count > 3:
                bitcamp_indices = [i for i, s in enumerate(sub_arr) if s.endswith('Bitcamp')]
                indices_to_remove = random.sample(bitcamp_indices, bitcamp_count - 3)
                sub_arr[:] = [s for i, s in enumerate(sub_arr) if i not in indices_to_remove]

        #change hc to index numbering
        for i in range(0, len(hc)):
            for j in range(0, len(hc[i])):
                hc[i][j] = category_names.index(hc[i][j])


csv_file = "backend/bitcamp-2023-projects.csv"
process(csv_file)
print(hc)
# print(cap)
print()

def abstract_expo_alg(hc: List[List[int]], cap: List[int], t_max: int):
    # extracting sizes
    M = len(hc)
    N = len(cap)
    
    # bookkeeping for valid (h, j) pairs
    valid_hj = set()
    for h, req_cat in enumerate(hc):
        for j in req_cat:
            valid_hj.add((h, j))
    hj_to_i_base = dict(map(tuple, map(lambda t: t[::-1], list(enumerate(valid_hj)))))

    def solve_expo(T: int):
        # index bookkeeping
        num_var = len(valid_hj) * T
        def hjt_to_i(h: int, j: int, t: int) -> int:
            return len(valid_hj) * (t-1) + hj_to_i_base[(h, j)]

        # first condition
        A1 = np.zeros((len(valid_hj), num_var))
        for x, (h, j) in enumerate(valid_hj):
            for t in range(T):
                A1[x, hjt_to_i(h, j, t)] = 1
        b1= np.ones(len(valid_hj))

        # second condition
        A2 = np.zeros((N*T, num_var))
        for x, (j, t) in enumerate(itertools.product(range(N), range(T))):
            for h in range(M):
                if (h, j) not in valid_hj:
                    continue
                A2[x, hjt_to_i(h, j, t)] = 1
        b2 = np.repeat(cap, T)

        # third condition
        A3 = np.zeros((M*T, num_var))
        for x, (h, t) in enumerate(itertools.product(range(M), range(T))):
            for j in range(N):
                if (h, j) not in valid_hj:
                    continue
                A3[x, hjt_to_i(h, j, t)] = 1
        b3 = np.ones(M*T)

        # solve linear program
        x = scipy.optimize.milp(
            c=-np.ones(num_var),
            constraints=[
                scipy.optimize.LinearConstraint(A1, 0, b1),
                scipy.optimize.LinearConstraint(A2, 0, b2),
                scipy.optimize.LinearConstraint(A3, 0, b3)
            ],
            bounds=scipy.optimize.Bounds(lb=0, ub=1),
            integrality=1
        ).x
        if int(sum(x)) < len(valid_hj):
            return None

        # interpret solution
        H = [list() for _ in range(M)]
        J = [list() for _ in range(N)]
        for j in range(N):
            J[j] = [list() for _ in range(T)]
            for h in range(M):
                if (h, j) not in valid_hj:
                    continue
                for t in range(T):
                    if x[hjt_to_i(h, j, t)] == 1.0:
                        H[h].append((j, t))
                        J[j][t].append(h)
        return (H, J)

    # return solve_expo(t_max)
    # binary search:
    a, b = 1, t_max
    while a < b-1:
        m = int(np.ceil((a+b)/2))
        soln = solve_expo(m)
        if soln is None: # failure
            a = m+1
        else: # success
            b = m

    # check when 2 left
    if a == b:
        t = a
    else:
        if solve_expo(a) is None:
            t = b
        else:
            t = a

    # return optimal solution
    H, J = solve_expo(t)
    return (t, H, J)

t, H, J = abstract_expo_alg(hc, cap, 50)
print(t)
print()
print(H)
print()
print(J)

for i in range(len(H)):
    for j in range(len(H[i])):
        H[i][j] = (category_names[H[i][j][0]], j)

print(H)