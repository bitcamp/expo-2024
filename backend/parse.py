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
from collections import defaultdict

from datetime import datetime, timedelta
import pytz

random.seed(10)

DRAFT_COLUMN_NAME = 'Project Status'
TEAM_COLUMN_NAME = 'Project Title'
LINK_COLUMN_NAME = 'Submission Url'
IN_PERSON_COLUMN_NAME = 'Will You Be Present To Demo In Person On Sunday?'
CHALLENGES_COLUMN_NAME = 'Opt-In Prizes'
TRACK_CHALLENGE_COLUMN_NAME = 'Bitcamp Track Challenge'
TRACK_HACK_OPT_OUT_RESPONSE = "I don't want to submit to a Bitcamp track challenge. I understand that I can still submit to the other Bitcamp sponsored challenges."

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

EXCLUDED_CHALLENGES = set([
    "People's Choice Hack - Bitcamp",
    "Beginner Quantum Track Hacks - Bitcamp"
])

CHALLENGE_JUDGE_GROUPS = [
    3, #"Best Machine Learning Track Hack - Bitcamp", (3+4)
    4, #"Best App Dev Track Hack - Bitcamp", (9+2)
    2, #"Best Cybersecurity Track Hack - Bitcamp", (3+2)
    0, #"Beginner Quantum Track Hacks - Bitcamp", (4+2)
    3, #"Best Advanced Quantum Track Hack - Bitcamp", (4+2)

    2, #"Best Hardware Hack - Bitcamp",
    2, #"Best Bitcamp Hack - Bitcamp",
    2, #"Best First Time Hack - Bitcamp",
    2, #"Best UI/UX Hack - Bitcamp",
    2, #"Best Moonshot Hack - Bitcamp",
    2, #"Best Razzle Dazzle Hack - Bitcamp",
    2, #"Best Social Good Hack - Bitcamp",
    2, #"Best Gamification Hack - Bitcamp",
    2, #"People's Choice Hack - Bitcamp",
    2, #"Best Sustainability Hack - Bitcamp",

    2, #"Best use of AI/ML Innovation for the Francis Scott Key Bridge Recovery Efforts - Cloudforce",
    2, #"Most Philanthropic Hack - Bloomberg",
    1, #"Best Digital Forensics Related Hack - Cipher Tech",
    2, #"Best Use of APIs related to Housing/Climate Change - Fannie Mae",
    2, #"Best AI Powered Solution for Defense Contracts - Bloomberg Industry Group", 
    2, #"Best Financial Hack - Capital One",
    2 #"University Course Catalog Data Extraction and Query Challenge - Xficient",
]

TABLES = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8', 'J1', 'J2', 'J3', 'J4', 'J5', 'J6', 'J7', 'J8', 'K1', 'K2', 'K5', 'K6', 'K7', 'K8', 'L1', 'L2', 'L5', 'L6', 'L7', 'L8', 'M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'N7', 'N8', 'O1', 'O2', 'O3', 'O4', 'O5', 'O6', 'O7', 'O8', 'P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8']
random.shuffle(TABLES)

FULL_CHALLENGE_LIST = [
    "Best Machine Learning Track Hack - Bitcamp",
    "Best App Dev Track Hack - Bitcamp",
    "Best Cybersecurity Track Hack - Bitcamp",
    "Beginner Quantum Track Hacks - Bitcamp",
    "Best Advanced Quantum Track Hack - Bitcamp",
    
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

    "Best use of AI/ML Innovation for the Francis Scott Key Bridge Recovery Efforts - Cloudforce",
    "Most Philanthropic Hack - Bloomberg",
    "Best Digital Forensics Related Hack - Cipher Tech",
    "Best Use of APIs related to Housing/Climate Change - Fannie Mae",
    "Best AI Powered Solution for Defense Contracts - Bloomberg Industry Group",
    "Best Financial Hack - Capital One",
    "University Course Catalog Data Extraction and Query Challenge - Xficient",
    
#     "Best use of AI/ML Innovation for the Francis Scott Key Bridge Recovery Efforts - Cloudforce",
# "Best Digital Forensics Related Hack - Cipher Tech",
# "Best Use of APIs related to Housing/Climate Change - Fannie Mae",
# "Best AI Powered Solution for Defense Contracts - Bloomberg Industry Group",
# "Best Bitcamp Hack - Bitcamp",
# "Best UI/UX Hack - Bitcamp",
# "Best Social Good Hack - Bitcamp",
# "Best Financial Hack - Capital One",
# "Beginner Quantum Track Hacks - Bitcamp",
# "Best use of AI/ML Innovation for the Francis Scott Key Bridge Recovery Efforts - Cloudforce",
# "Best Digital Forensics Related Hack - Cipher Tech",
# "Best Use of APIs related to Housing/Climate Change - Fannie Mae",
# "Best AI Powered Solution for Defense Contracts - Bloomberg Industry Group",
# "Best Bitcamp Hack - Bitcamp",
# "Best UI/UX Hack - Bitcamp",
# "Best Financial Hack - Capital One",
# "Best use of AI/ML Innovation for the Francis Scott Key Bridge Recovery Efforts - Cloudforce",
# "Best AI Powered Solution for Defense Contracts - Bloomberg Industry Group",
# "Best UI/UX Hack - Bitcamp",
# "Beginner Quantum Track Hacks - Bitcamp"
]

def get_challenge_maps(full_challenge_list):
    challenge_to_id = {}
    id_to_challenge = {}
    for i, challenge in enumerate(full_challenge_list):
        challenge_to_id[challenge] = i
        id_to_challenge[i] = challenge
    return challenge_to_id, id_to_challenge

# Get mapping
CHALLENGE_TO_ID, ID_TO_CHALLENGE = get_challenge_maps(FULL_CHALLENGE_LIST)

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
            elif len(tc) > 0 and (tc not in EXCLUDED_CHALLENGES):
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
    # print(bitcamp_challenges)
    # print(other_challenges)

    if track_response in BITCAMP_TRACK_HACKS:
        max_challenges = min(2, len(bitcamp_challenges))
        result = (random.sample(bitcamp_challenges, max_challenges))
        result.append(track_response)
    else:
        max_challenges = min(3, len(bitcamp_challenges))
        result = (random.sample(bitcamp_challenges, max_challenges))

    result += other_challenges

    return result

def process(csv_file):
    types = defaultdict(lambda: str)
    projects = pd.read_csv(csv_file, keep_default_na=False, dtype=types)

    # Only grab submitted projects
    submitted_projects = projects[projects[DRAFT_COLUMN_NAME] != 'Draft']

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
        nc = process_bitcamp_hacks(track, temp_challenges[i])
        # print(nc)
        challenges.append(nc)

    hc = []
    for ind_challenges in challenges:
        ind_hc = []
        for challenge in ind_challenges:
            ind_hc.append(CHALLENGE_TO_ID[challenge])
        hc.append(ind_hc)
    
    return team_names, links, in_person, challenges, MLH_challenges, hc


def parse_challenge_name(challenge_name):
    return challenge_name.split(" - ")

def expo_output_to_json(t, H, team_names, links, in_person_list, MLH_challenges):
    eastern = pytz.timezone('US/Eastern')

    EXPO_START_TIME = "2024-04-21 11:00:00"
    EXPO_START = eastern.localize(datetime.strptime(EXPO_START_TIME, "%Y-%m-%d %H:%M:%S"))

    HACK_TIME = 5
    judgetime_seen = defaultdict(lambda: 1)

    result = []
    for id, team in enumerate(H):
        team_json = {
            "id": id,
            "team_name": team_names[id],
            "table": TABLES.pop() if in_person_list[id] else "virtual",
            "in_person": in_person_list[id],
            "link": links[id],
        }

        challenges = []

        for timeslot in team:
            challenge_id, start_slot = timeslot
            challenge = ID_TO_CHALLENGE[challenge_id]

            start_time = str(EXPO_START + timedelta(minutes=HACK_TIME*start_slot))

            challenge_name, company = parse_challenge_name(challenge)
            
            judge_id = challenge + str(start_slot)
            judge_group = judgetime_seen[judge_id]
            judgetime_seen[judge_id] += 1

            challenge_json = {
                "is_mlh": False,
                "challenge_name": challenge_name,
                "company": company,
                "judge": f"Judge {judge_group}",
                "start_time": start_time,
            }
            challenges.append(challenge_json)

        challenges.sort(key=lambda x: x["start_time"])
        
        for challenge in MLH_challenges[id]:
            challenge_name, company = parse_challenge_name(challenge)

            challenge_json = {
                "is_mlh": True,
                "challenge_name": challenge_name,
                "company": company,
                "judge": "Judge",
                "start_time": "",
            }
            challenges.append(challenge_json)
        
        team_json["challenges"] = challenges
        result.append(team_json)
                
    return result


def main():
    # csv_file = "./projects-2024-teammates.csv"
    csv_file = "./final10am.csv"
    team_names, links, in_person, challenges, MLH_challenges, hc = process(csv_file)

    # cap = [5, 2, 5, 4, 4, 4, 4, 4, 4, 4, 2, 4, 4, 2, 4, 4, 4, 1]
    cap = [2, 2, 2, 1, 1, 2, 2, 2,           4, 4, 4, 4, 4, 4, 4, 4, 4, 4,  1,1,1,1,1,1,1,1,1]

    # print(len(cap))
    # print(len(FULL_CHALLENGE_LIST))
    # print(len(CHALLENGE_TO_ID))
    # print(len(ID_TO_CHALLENGE))
    # for challenge_name, id in CHALLENGE_TO_ID.items():
    #     print(f'{challenge_name} - {cap[id]}')

    # print(len(cap))

    # print(hc)

    t, H, J = abstract_expo_alg(hc, cap, 69)

    print(t)
    print(150 // t)
    print(H)

    expo_output = expo_output_to_json(t, H, team_names, links, in_person, MLH_challenges)

    output_path = '../frontend/public/expo_algorithm_results.json'

    with open(output_path, 'w') as f:
        json.dump(expo_output, f, indent=4)

    print(f"Output written to {output_path}")


if __name__ == "__main__":
    main()
