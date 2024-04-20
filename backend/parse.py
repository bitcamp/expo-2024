import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy
from scipy import optimize
import itertools
from typing import List, Dict, Tuple, Optional
import random
import json
import random


DRAFT_COLUMN_NAME = 'Project Status'
TEAM_COLUMN_NAME = 'Project Title'
LINK_COLUMN_NAME = 'Submission Url'
IN_PERSON_COLUMN_NAME = 'Will you be in-person to present?'
CHALLENGES_COLUMN_NAME = 'Opt-In Prizes'
TRACK_CHALLENGE_COLUMN_NAME = 'Bitcamp Track Challenge'

hc = []
cap = []
#1 refers to index 0 (bloomberg), 2 refers to index 1 (costar)...
category_names = []
team_names = []
links = []
all_mlh = []
in_person = []

MLH_HACKS = set([
    "Best Domain Name from GoDaddy Registry - MLH",
    "Best DEI Hack sponsored by Fidelity - MLH",
    "Best Use of Taipy - MLH",
    "Best Use of PropelAuth - MLH",
    "Best Use of Kintone - MLH",
    "Best Use of Starknet - MLH",
])

BITCAMP_TRACK_HACKS = set([
    "Best Machine Learning Track Hack - Bitcamp",
    "Best App Dev Track Hack - Bitcamp",
    "Best Cybersecurity Track Hack - Bitcamp",
    "Beginner Quantum Track Hacks - Bitcamp",
    "Best Advanced Quantum Track Hack - Bitcamp"
])

BITCAMP_HACKS = set([
    "Best Hardware Hack - Bitcamp",
    "Best Bitcamp Hack - Bitcamp",
    "Best First Time Hack - Bitcamp",
    "Best UI/UX Hack - Bitcamp",
    "Best Moonshot Hack - Bitcamp",
    "Best Razzle Dazzle Hack - Bitcamp",
    "Best Social Good Hack - Bitcamp",
    "Best Gamification Hack - Bitcamp",
    "People's Choice Hack - Bitcamp",
    "Best Sustainability Hack - Bitcamp"
])

FULL_CHALLENGE_LIST = [
    "Best Hardware Hack - Bitcamp",
    "Best Bitcamp Hack - Bitcamp",
    "Best First Time Hack - Bitcamp",
    "Best UI/UX Hack - Bitcamp",
    "Best Moonshot Hack - Bitcamp",
    "Best Razzle Dazzle Hack - Bitcamp",
    "Best Social Good Hack - Bitcamp",
    "Best Gamification Hack - Bitcamp",
    "People's Choice Hack - Bitcamp",
    "Best Sustainability Hack - Bitcamp",
    
    "Best Hardware Hack - Bitcamp",
    "Best Bitcamp Hack - Bitcamp",
    "Best First Time Hack - Bitcamp",
    "Best UI/UX Hack - Bitcamp",
    "Best Moonshot Hack - Bitcamp",
    "Best Razzle Dazzle Hack - Bitcamp",
    "Best Social Good Hack - Bitcamp",
    "Best Gamification Hack - Bitcamp",
    "People's Choice Hack - Bitcamp",
    "Best Sustainability Hack - Bitcamp"

    "Best use of AI/ML Innovation for the Francis Scott Key Bridge Recovery Efforts - Cloudforce",
    "Most Philanthropic Hack - Bloomberg",
    "Best Digital Forensics Related Hack - Cipher Tech",
    "Best Use of APIs related to Housing/Climate Change - Fannie Mae",
    "Best AI Powered Solution for Defense Contracts - Bloomberg Industry Group",
    "Best Financial Hack - Capital One",
    "University Course Catalog Data Extraction and Query Challenge - Xficient",
]

TRACK_HACK_OPT_OUT_RESPONSE = "I am not signing up for a track"

def get_challenge_maps(full_challenge_list):
    challenge_to_id = {}
    id_to_challenge = {}
    for i, challenge in enumerate(full_challenge_list):
        challenge_to_id[challenge] = i
        id_to_challenge[i] = challenge
    return challenge_to_id, id_to_challenge

# Get mapping
CHALLENGE_TO_ID, ID_TO_CHALLENGE = get_challenge_maps(FULL_CHALLENGE_LIST)

def process_challenges(challenges):
    result = []
    MLH_challenges = []
    for challenge in challenges:
        team_challenges = challenge.split(",")
        current_challenges = []
        current_mlh_challenges = []
        
        for tc in team_challenges:
            tc = tc.strip()
            if tc in MLH_HACKS:
                current_mlh_challenges.append(tc)
            else:
                current_challenges.append(tc)
        result.append(current_challenges)
        MLH_challenges.append(current_mlh_challenges)

    return result, MLH_challenges
            
def process_bitcamp_hacks(track_response, challenges):
    bitcamp_challenges = []
    other_challenges = []
    result = []

    for challenge in challenges:
        if challenge in BITCAMP_HACKS:
            bitcamp_challenges.append(challenge)
        else:
            other_challenges.append(challenge)
    

    if track_response == TRACK_HACK_OPT_OUT_RESPONSE:
        max_challenges = max(3, len(bitcamp_challenges))
        result += (random.sample(bitcamp_challenges, max_challenges))
    else:
        max_challenges = max(2, len(bitcamp_challenges))
        result += (random.sample(bitcamp_challenges, max_challenges))
        result.append(track_response)


def process(csv_file):
    projects = pd.read_csv(csv_file)

    # Only grab submitted projects
    submitted_projects = projects[projects[DRAFT_COLUMN_NAME] == 'Submitted']

    team_names = submitted_projects[TEAM_COLUMN_NAME].tolist()
    links = submitted_projects[LINK_COLUMN_NAME].tolist()
    in_person = (submitted_projects[IN_PERSON_COLUMN_NAME] == 'Yes').tolist()
    challenge_fields = submitted_projects[CHALLENGES_COLUMN_NAME].tolist()

    # Separate MLH and other challenges
    
    temp_challenges, MLH_challenges = process_challenges(challenge_fields)

    # Get track challenge and limit bitcamp challenges to MAX 3
    track_response = submitted_projects[TRACK_CHALLENGE_COLUMN_NAME].tolist()

    challenges = []
    for i, track in enumerate(track_response):
        challenges.append(process_bitcamp_hacks(track, temp_challenges[i]))

    hc = []
    for ind_challenges in challenges:
        ind_hc = []
        for challenge in ind_challenges:
            ind_hc.append(CHALLENGE_TO_ID[challenge])
        hc.append(ind_hc)
    
    return team_names, links, in_person, challenges, MLH_challenges, hc
                    

csv_file = "./bitcamp-2023-projects.csv"
team_names, links, in_person, challenges, MLH_challenges, hc = process(csv_file)


# cap = [5, 2, 5, 4, 4, 4, 4, 4, 4, 4, 2, 4, 4, 2, 4, 4, 4, 1]
cap = [2, 2, 2, 1, 1, 2, 2, 2,           4, 4, 4, 4, 4, 4, 4, 4, 4, 4]

for challenge_name, id in CHALLENGE_TO_ID:
    print(f'{challenge_name} - {cap[id]}')

# print(len(cap))

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

t, H, J = abstract_expo_alg(hc, cap, 69)
# print(t)
# print()
# print(H)
# print()
# print(J)

# for i in range(len(H)):
#     for j in range(len(H[i])):
#         H[i][j] = (category_names[H[i][j][0]], H[i][j][1])

# # print(H)

# final_cat_names = []

# # print(category_names)

# for val in category_names:
#     if (val[val.index("- ") + 2: ] != "Bitcamp"):
#         final_cat_names.append(val[val.index("- ") + 2: ] + " - " + val[0:val.index(" -")])
#     else:
#         final_cat_names.append(val)
        
# mlh_challenges = list(set([item for sublist in all_mlh for item in sublist]))
# final_cat_names = final_cat_names + mlh_challenges

# combined = []

# tables = []
# for i in range(20):
#     letter = chr(ord('A') + i)
#     if letter == 'K' or letter == 'L':
#         tables.extend([letter + str(j) for j in range(1, 13) if j not in (3, 4, 5)])
#     else:
#         tables.extend([letter + str(j) for j in range(1, 13)])

# judge = "Judge"
# max = 0

# tableCounter = 0
# in_person_count = 0
# for i in range(0, len(in_person)):
#     if in_person[i] == "Yes":
#         in_person_count += 1
# in_person_arr = random.sample(range(in_person_count), in_person_count)

# for i in range(len(team_names)):
#     H_new = []
#     if (H[i] != []):
#         for j in range(len(H[i])):
#             if (H[i][j][0][H[i][j][0].index("- ") + 2: ] == "Bitcamp"):
#                 H_new.append([H[i][j][0][0:H[i][j][0].index(" -")], H[i][j][0][H[i][j][0].index("- ") + 2: ], judge, H[i][j][1]])
#             else:
#                 H_new.append([H[i][j][0][H[i][j][0].index("- ") + 2: ], H[i][j][0][0:H[i][j][0].index(" -")], judge, H[i][j][1]])
            
#             if H[i][j][1] > max:
#                 max = H[i][j][1]
    
#     H_new.sort(key=lambda x: x[-1])

#     for category in all_mlh[i]:
#         append = []
#         append.append(category.split(" - "))
#         H_new.append(append[0])


#     if in_person[i] == "Yes":
#         data = [
#             ["Yes", tables[in_person_arr[tableCounter]]],
#             team_names[i],
#             H_new,
#         ]
#         tableCounter += 1
#     else:
#         data = [
#             ["No"],
#             team_names[i],
#             H_new,
#         ]
#     combined.append(data)

# names_links = []
# for i in range(len(team_names)):
#     names_links.append([team_names[i], links[i]])
    
# repeats = {}    

# for value in combined:
#     if value != []:
#         for challenge in value[2]:
#             if challenge[1] != "Major League Hacking":
#                 challenge_key = str(challenge[0]) + " - " + str(challenge[1])
#                 if challenge_key not in repeats:
#                     repeats[challenge_key] = [[challenge[3]]]
#                 else:
#                     repeats[challenge_key].append([challenge[3]])

# for key, lists in repeats.items():
#     repeats[key] = sorted(lists, key=lambda x: x[0])

# for key in repeats:
#     curr = final_cat_names.index(key)
#     judgeCount = cap[curr]
#     inc = 0
#     for lst in repeats[key]:
#         lst.append((inc % judgeCount) + 1)
#         inc+=1

# for value in combined:
#     if value != []:
#         for challenge in value[2]:
#             if challenge[1] != "Major League Hacking":
#                 challenge_key = str(challenge[0]) + " - " + str(challenge[1])
#                 for idx, inner_list in enumerate(repeats[challenge_key]):
#                     if inner_list[0] == challenge[3]:
#                         challenge[2] = challenge[2] + " " + str(inner_list[1])
#                         del repeats[challenge_key][idx]
#                         break
                    
# for value in combined:
#     if value != []:
#         name = value[1]
#         for lst in names_links:
#             if name == lst[0]:
#                 value.append(lst[1])

# data = {
#     "category_names": final_cat_names,
#     "team_names": names_links,
#     "combined_values": combined,
#     "total_times" : max
# }
