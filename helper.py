"""
helper.py
Author: Parth Mishra
Copyright 2016

Helper functions for use in classify.py

DO NOT MODIFY

Functions are mostly taken from previous Udacity projects
"""
import numpy as np
import pandas as pd
import json


json_data = open('champion_data.json')

champ_data = json.load(json_data)
champion_winrates = {}

for i in range(199):
     champName = champ_data["matches"][i]['key']
     winPercent = champ_data["matches"][i]['general']['winPercent']
     champion_winrates[champName] = winPercent


with open('champions.txt', 'w') as f:
    f.write(str(champion_winrates))
