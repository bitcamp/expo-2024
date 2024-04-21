# this takes 2023 data and replaces the old names with the new names in the current

import pandas as pd
import csv

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
    "Best Machine Learning Hack - Bitcamp": SAME,
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
    "Advanced Quantum Track - Bitcamp": SAME,
    "People's Choice Hack - Bitcamp": SAME,
    "Best Hardware Hack - Bitcamp": SAME,
    "Best Gamification Hack - Bitcamp": SAME,
    "Cipher Tech - Best Digital Forensics Hack": "Best Digital Forensics Hack - Cipher Tech",
    "Best Bitcamp Hack - Bitcamp": SAME,
    "Best Accessibility Hack sponsored by Fidelity - Major League Hacking": SAME,
}


def parse_old(file):
    with open(file, "r") as f:
        data = list(csv.DictReader(f))

        # find and print all unique entries in the list represented as a string in column J of the CSV
        # uniques = set()
        # for row in data:
        #     item_string = row["Opt-In Prizes"]
        #     items = item_string.split(",")
        #     for item in items:
        #         item = item.strip()
        #         uniques.add(item)
        # print(uniques)

        # replace all old names with new names
        for row in data:
            item_string = row["Opt-In Prizes"]
            items = item_string.split(",")
            for i, item in enumerate(items):
                item = item.strip()
                if item in LOOKUP:
                    items[i] = LOOKUP[item]
            row["Opt-In Prizes"] = ", ".join(items)

        # save the new data to a new file
        with open("2023 bitcamp new.csv", "w") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)


parse_old("2023 bitcamp.csv")
