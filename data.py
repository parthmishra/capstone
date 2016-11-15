"""
Generate a dataset of Ranked Games of League of Legends using Riot's API

Author: Parth Mishra
Copyright 2016


Credit:
https://www.dataquest.io/blog/python-json-tutorial/
"""
import json
import requests
import csv
import pandas as pd
import ijson
import urllib
import time
import random

apikey = "RGAPI-ba9c94aa-1b78-412d-920a-02f0c696d7c5" #API key is removed for security purposes

filename = 'champions.json'

"""
with open(filename, 'r') as f:
    objects = ijson.items(f, "matches.item")
    columns = (o for o in objects if o['teamId'] == 100)
    for col in columns:
        col.encode('ascii')
"""

"""
with open(filename, 'r') as f:
    data = ijson.items(f, 'matches.item')
    columns = list(data)
"""

"""
#teams = [col["teams"] for col in columns]
participantIdentities = [col["participantIdentities"] for col in columns]
players = participantIdentities[0]
#players = [col["player"] for col in participantIdentities]
#print players
player = players[0]
#summonerId = player[1]
#print summonerId
player1 = player['player']
summonerId = player1['summonerId']
print summonerId
"""

"""
Create Champion Features

1. Generate List of Champion Names
2. Duplicate list of champion names
3. Append "_1" to Blue team champion name features
4. Append "_2" to Red team champion name features

"""
"""
with open('champions.json') as data_file:
    data = json.load(data_file)

champion_data = data["overview_data"]["data"]
champion_keys = champion_data.keys()
championIds = {}
for champ in champion_keys:
    Id = data["overview_data"]["data"][champ]["id"]
    championIds[champ] = Id

print championIds

blueteam = [str(i)+"_1" for i in champion_keys]
redteam = [str(i)+"_2" for i in champion_keys]
blueteam.extend(redteam)
champion_names = blueteam

print champion_names
"""

"""
Calculate Average Mastery Score

1. Get list of players in the game
2. Get their champion picks
3. Look up each player mastery based on pick
4. Add to players total and divide by 5

"""
def getMastery(summonerId, championId):
    response = requests.get("https://na.api.pvp.net/championmastery/location/NA1/player/"+str(summonerId)+"/champion/"+str(championId)+"?api_key="+str(apikey))
    data = response.json()
    mastery = data["championLevel"]

    return mastery

"""
Generate Match List

Create list of 700 matches seeded by a random participant in each game

100 Bronze
100 Silver
100 Gold
100 Platinum
100 Diamond
100 Master
100 Challenger

"""
matchlist = []
d_seed = 48349059

def getMatch(data):
    for i in range(0,9):
        game_type = data["games"][i]["subType"]
        matchId = data["games"][i]["gameId"]
        if game_type == "RANKED_FLEX_SR" and matchId not in matchlist:
            print "Game Type: ", game_type

            matchlist.append(matchId)
            print "Match ID: ", matchId
            rand = random.randint(0,8)
            seed = data["games"][i]["fellowPlayers"][rand]["summonerId"]
            return seed

    seed = 48349059
    return seed


while len(matchlist) < 100:

    response = requests.get("https://na.api.pvp.net/api/lol/na/v1.3/game/by-summoner/"+str(d_seed)+"/recent?api_key=RGAPI-ba9c94aa-1b78-412d-920a-02f0c696d7c5")
    data = response.json()
    d_seed = getMatch(data)

    print "Matchlist length: ", len(matchlist)
    time.sleep(2)

matchlist_file = open('matchlist.txt', 'w')

for match in matchlist:
    matchlist_file.write("%s\n" % match)


"""
Training Data Sample

2*133 Features are champions with binary 0 (not present) or 1 (present)
2 Features are dedicated to average champion mastery of each respective team
1 Feature indicating patch number (for future extensibility purposes)
1 Class label that has 0 (blue team win) or 1 (red team win)


"""
