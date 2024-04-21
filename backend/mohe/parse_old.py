# open csv and parse it
# return a list of dictionaries

# parse with pandas
import pandas as pd
import csv

def parse_old(file):
    with open(file, 'r') as f:
        data = list(csv.DictReader(f))
        datapa
    return data


parse_old('data.csv')