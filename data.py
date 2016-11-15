"""
Generate a dataset of Ranked Games of League of Legends using Riot's API

Author: Parth Mishra
Copyright 2016
"""
import json
import requests
import csv
import pandas as pd
import ijson
import urllib
import time
import random
import numpy as np
from sklearn import preprocessing

apikey = "4bf388db-f2aa-4d18-9d76-b70b3186a3b9" #API key is removed for security purposes



"""
Create Champion Features

1. Generate List of Champion Names
2. Duplicate list of champion names
3. Append "_1" to Blue team champion name features
4. Append "_2" to Red team champion name features

"""
filename = 'champions.json'

with open(filename) as data_file:
    data = json.load(data_file)

champion_data = data["overview_data"]["data"]
champion_keys = champion_data.keys()
championIds = {}
for champ in champion_keys:
    Id = data["overview_data"]["data"][champ]["id"]
    championIds[Id] = champ

blueteam = [str(i)+"_1" for i in champion_keys]
redteam = [str(i)+"_2" for i in champion_keys]
blueteam.extend(redteam)
champion_names = blueteam


"""
Calculate Average Mastery Score

1. Get list of players in the game
2. Get their champion picks
3. Look up each player mastery based on pick
4. Add to players total and divide by 5

"""
def getMastery(summonerId, championId):

    response = requests.get("https://na.api.pvp.net/championmastery/location/NA1/player/"+str(summonerId)+"/champion/"+str(championId)+"?api_key="+str(apikey))
    print "Mastery Status Code: ", response.status_code
    print response.headers


    data = response.json()
    mastery = data["championLevel"]

    time.sleep(5)
    return mastery


"""
Training Data Sample

2*133 Features are champions with binary 0 (not present) or 1 (present)
2 Features are dedicated to average champion mastery of each respective team
1 Feature indicating patch number (for future extensibility purposes)
1 Class label that has 0 (blue team win) or 1 (red team win)


"""

with open('matchlist_silver.txt') as f:
    matchlist = f.readlines()
    matchlist = [int(x) for x in matchlist]

remaining_features = ['BLUE_AVG_MASTERY','RED_AVG_MASTERY','WINNER']
features = champion_names
features.extend(remaining_features)
data = []

counter = 0
for matchId in matchlist:
    participantIds = []
    championPicks = []
    playerIds = []
    data_sample = [0]*269

    try:
        response = requests.get("https://na.api.pvp.net/api/lol/na/v2.2/match/"+str(matchId)+"?api_key="+str(apikey))
        print "Match Status Code: ", response.status_code
        print "Match Header: ", response.headers
    except:
        print response.status_code

    if response.status_code == 200:
        print "Successful call"
    else:
        print "Unsuccessful Call: ", response.status_code
        time.sleep(30)

    match_data = response.json()
    #print match_data

    for i in range(0,10):
        participantIds.append(match_data["participantIdentities"][i]["player"]["summonerId"])
        playerIds.append(match_data["participants"][i]["participantId"])
        championPicks.append(match_data["participants"][i]["championId"])

    """ FILL OUT CHAMPION PICKS """


    # Blue side
    all_champs = []
    for i in range(0,5):
        all_champs.append(championIds[championPicks[i]]+"_1")

    for j in range(132):
        for i in range(0,5):
            if  all_champs[i] == blueteam[j]:
                data_sample[j] = 1
            elif data_sample[j] == 1:
                data_sample[j] = 1
            else:
                data_sample[j] = 0

    #print "Blue Team: ", all_champs



    # Red Side
    all_champs = []
    for i in range(5,10):
        all_champs.append(championIds[championPicks[i]]+"_2")

    for j in range(132):
        for i in range(0,5):
            if  all_champs[i] == redteam[j]:
                data_sample[j] = 1
            elif data_sample[j] == 1:
                data_sample[j] = 1
            else:
                data_sample[j] = 0

    #print "Red Team: ", all_champs


    """ CALCULATE AVERAGE MASTERY """

    BLUE_AVG_MASTERY = 0
    RED_AVG_MASTERY = 0


    for i in range(0,5):
        mastery = getMastery(participantIds[i],championPicks[i])
        BLUE_AVG_MASTERY += mastery

    for i in range(5,10):
        mastery = getMastery(participantIds[i],championPicks[i])
        RED_AVG_MASTERY += mastery

    BLUE_AVG_MASTERY = BLUE_AVG_MASTERY/5.0
    BLUE_AVG_MASTERY = (2*BLUE_AVG_MASTERY - 7)/(7) # normalize continuous features
    RED_AVG_MASTERY = RED_AVG_MASTERY/5.0
    RED_AVG_MASTERY = (2*RED_AVG_MASTERY - 7)/(7)

    data_sample[266]= BLUE_AVG_MASTERY
    data_sample[267]= RED_AVG_MASTERY

    """ ADD WINNER """
    winner = match_data["participants"][0]["stats"]["winner"]
    if winner == True:
        data_sample[268] = 1
    else:
        data_sample[268] = 0

    #print "Data Sample: ", data_sample
    data.append(data_sample)

    counter += 1
    print str(counter) + " samples added"


df = pd.DataFrame(data, columns=features)
df.to_csv('data_silver.csv')
