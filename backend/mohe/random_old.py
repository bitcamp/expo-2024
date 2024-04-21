# this takes 2023 data and replaces the old names with the new names in the current

import pandas as pd
import csv
import random

NEW = [
    "Best Public Sector Hack - Bloomberg Industry Group",
    "Best Use of Real Estate Data - CoStar Group",
    "Best Financial Hack - Capital One",
    "Best Moonshot Hack - Bitcamp",
    "People's Choice Hack - Bitcamp",
    "Best Machine Learning Hack - Bitcamp",
    "Best First Time Hack - Bitcamp",
    "Best UI/UX Hack - Bitcamp",
    "Best Social Good Hack - Bitcamp",
    "Best Gamification Hack - Bitcamp",
    "Best Use of CockroachDB Serverless - Cockroach Labs",
    "Best Bitcamp Hack - Bitcamp",
    "Most Philanthropic Hack - Bloomberg",
    "Don\u2019t Put All Your Eggs in One Basket - Fannie Mae",
    "Best Razzle Dazzle Hack - Bitcamp",
    "Best Hardware Hack - Bitcamp",
    "Best Digital Forensics Hack - Cipher Tech",
    "Advanced Quantum Track - Bitcamp",
    "Best Accessibility Hack sponsored by Fidelity - Major League Hacking",
    "Best Use of MongoDB Atlas - Major League Hacking",
    "Best Domain Name from Domain.com - Major League Hacking",
    "Most Creative Use of Twilio - Major League Hacking",
    "Best Blockchain Project Using Hedera - Major League Hacking",
    "Best Use of Microsoft Cloud for Your Community - Major League Hacking",
]

OLD = [
    "",
    "Fannie Mae - Don’t Put All Your Eggs in One Basket",
    "Best Use of Microsoft Cloud for Your Community - Major League Hacking",
    "Best Domain Name from Domain.com - Major League Hacking",
    "Best Razzle Dazzle Hack - Bitcamp",
    "Bloomberg - Most Philanthropic Hack",
    "Most Creative Use of Twilio - Major League Hacking",
    "Best Machine Learning Hack - Bitcamp",
    "Bloomberg Industry Group - Best Public Sector Hack",
    "Capital One - Best Financial Hack",
    "Cockroach Labs - Best Use of CockroachDB Serverless",
    "Best Moonshot Hack - Bitcamp",
    "Best UI/UX Hack - Bitcamp",
    "CoStar Group - Best Use of Real Estate Data",
    "Best First Time Hack - Bitcamp",
    "Best Use of MongoDB Atlas - Major League Hacking",
    "Best Social Good Hack - Bitcamp",
    "Best Blockchain Project Using Hedera - Major League Hacking",
    "Advanced Quantum Track - Bitcamp",
    "People's Choice Hack - Bitcamp",
    "Best Hardware Hack - Bitcamp",
    "Best Gamification Hack - Bitcamp",
    "Cipher Tech - Best Digital Forensics Hack",
    "Best Bitcamp Hack - Bitcamp",
    "Best Accessibility Hack sponsored by Fidelity - Major League Hacking",
]

SAME = "Same"

LOOKUP = {
    "Fannie Mae - Don’t Put All Your Eggs in One Basket": SAME,
    "Best Use of Microsoft Cloud for Your Community - Major League Hacking": SAME,
    "Best Domain Name from Domain.com - Major League Hacking": SAME,
    "Best Razzle Dazzle Hack - Bitcamp": SAME,
    "Bloomberg - Most Philanthropic Hack": "Most Philanthropic Hack - Bloomberg",
    "Most Creative Use of Twilio - Major League Hacking": SAME,
    "Bloomberg Industry Group - Best Public Sector Hack": "Best Public Sector Hack - Bloomberg Industry Group",
    "Capital One - Best Financial Hack": "Best Financial Hack - Capital One",
    "Cockroach Labs - Best Use of CockroachDB Serverless": "Best Use of CockroachDB Serverless - Cockroach Labs",
    "Best Moonshot Hack - Bitcamp": SAME,
    "Best UI/UX Hack - Bitcamp": SAME,
    "CoStar Group - Best Use of Real Estate Data": "Best Use of Real Estate Data - CoStar Group",
    "Best First Time Hack - Bitcamp": SAME,
    "Best Use of MongoDB Atlas - Major League Hacking": SAME,
    "Best Social Good Hack - Bitcamp": SAME,
    "Best Blockchain Project Using Hedera - Major League Hacking": SAME,
    "People's Choice Hack - Bitcamp": SAME,
    "Best Hardware Hack - Bitcamp": SAME,
    "Best Gamification Hack - Bitcamp": SAME,
    "Cipher Tech - Best Digital Forensics Hack": "Best Digital Forensics Hack - Cipher Tech",
    "Best Bitcamp Hack - Bitcamp": SAME,
    "Best Accessibility Hack sponsored by Fidelity - Major League Hacking": SAME,
    "Best Machine Learning Hack - Bitcamp": SAME,
    "Advanced Quantum Track - Bitcamp": "Best Advanced Quantum Track Hack",
}


def print_cats(file):
    with open(file, "r") as f:
        data = list(csv.DictReader(f))

        # find and print all unique entries in the list represented as a string in column J of the CSV
        uniques = set()
        for row in data:
            item_string = row["Opt-In Prizes"]
            items = item_string.split(",")
            for item in items:
                item = item.strip()
                uniques.add(item)
        print(uniques)


OLD_TRACKS = [
    "Best Machine Learning Hack - Bitcamp",
    "Best Advanced Quantum Track Hack",
]


def rename_old_cats(file, out):
    for item in LOOKUP:
        if LOOKUP[item] == SAME:
            LOOKUP[item] = item

    with open(file, "r") as f:
        data = list(csv.DictReader(f))

        # replace all old names with new names
        for row in data:
            print(row["Opt-In Prizes"])
            item_string = row["Opt-In Prizes"]

            for item in LOOKUP:
                if item in item_string:
                    item_string = item_string.replace(item, LOOKUP[item])

            items = item_string.split(",")

            new_items = items.copy()
            for item in enumerate(new_items):
                item = item.strip()
                if item in OLD_TRACKS:
                    row["Bitcamp Track Challenge"] = item
                    # remove the track from the list of items
                    print("removing", item)
                    new_items.remove(item)

            # update the row with the new names
            update = ", ".join(items)
            # match anything in item_string that matches OLD_TRACKS and put it in "Bitcamp Track Challenge"
            # for track in OLD_TRACKS:
            #     if track in item_string:
            #         row["Bitcamp Track Challenge"] = track
            #         update = update.replace(track + ", ", "")

            row["Opt-In Prizes"] = update

        # save the new data to a new file
        with open(out, "w") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)


TRACKS = [
    # "Best Machine Learning Track Hack - Bitcamp",
    "Best Cybersecurity Track Hack - Bitcamp",
    "Best App Dev Track Hack - Bitcamp",
    "Beginner Quantum Track Hacks - Bitcamp",
    # "Best Advanced Quantum Track Hack",
]


def randomize_old_cats(file, out):
    with open(file, "r") as f:
        data = list(csv.DictReader(f))

        # if empty, pick a randomized category
        for row in data:
            item_string = row["Bitcamp Track Challenge"]
            if item_string == "":
                # generate random number between 0 and 5
                random_index = random.randint(0, 100)
                # PARAMS: 20, 40, 60, 80
                if random_index < 20:
                    row["Bitcamp Track Challenge"] = TRACKS[0]
                elif random_index < 40:
                    row["Bitcamp Track Challenge"] = TRACKS[1]
                elif random_index < 60:
                    row["Bitcamp Track Challenge"] = TRACKS[2]
                else:
                    row["Bitcamp Track Challenge"] = ""

        # save the new data to a new file
        with open(out, "w") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)


rename_old_cats("2023 bitcamp.csv", "2023 bitcamp filtered.csv")
randomize_old_cats("2023 bitcamp filtered.csv", "2023 bitcamp FINAL.csv")
