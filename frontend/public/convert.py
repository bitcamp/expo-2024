import json

challenges = [
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

        "Best Domain Name from GoDaddy Registry - MLH",
        "Best DEI Hack sponsored by Fidelity - MLH",
        "Best Use of Taipy - MLH",
        "Best Use of PropelAuth - MLH",
        "Best Use of Kintone - MLH",
        "Best Use of Starknet - MLH"
]

data = []

for i, challenge in enumerate(challenges):
    data.append({
        "id": i,
        "prize_category": challenge,
    })

with open("expo_algorithm_challenges.json", "w") as f:
    json.dump(data, f, indent=4)