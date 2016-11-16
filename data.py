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

filename = 'matchlist_challenger.txt'
csv_file = 'data_challenger.csv'
"""
Create Champion Features

1. Generate List of Champion Names
2. Duplicate list of champion names
3. Append "_1" to Blue team champion name features
4. Append "_2" to Red team champion name features

"""
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
with open('champions.txt', 'w') as f:
    f.write(str(championIds))
"""
championIds = {1: u'Annie', 2: u'Olaf', 3: u'Galio', 4: u'TwistedFate', 5: u'XinZhao', 6: u'Urgot', 7: u'Leblanc', 8: u'Vladimir', 9: u'FiddleSticks', 10: u'Kayle', 11: u'MasterYi', 12: u'Alistar', 13: u'Ryze', 14: u'Sion', 15: u'Sivir', 16: u'Soraka', 17: u'Teemo', 18: u'Tristana', 19: u'Warwick', 20: u'Nunu', 21: u'MissFortune', 22: u'Ashe', 23: u'Tryndamere', 24: u'Jax', 25: u'Morgana', 26: u'Zilean', 27: u'Singed', 28: u'Evelynn', 29: u'Twitch', 30: u'Karthus', 31: u'Chogath', 32: u'Amumu', 33: u'Rammus', 34: u'Anivia', 35: u'Shaco', 36: u'DrMundo', 37: u'Sona', 38: u'Kassadin', 39: u'Irelia', 40: u'Janna', 41: u'Gangplank', 42: u'Corki', 43: u'Karma', 44: u'Taric', 45: u'Veigar', 48: u'Trundle', 50: u'Swain', 51: u'Caitlyn', 53: u'Blitzcrank', 54: u'Malphite', 55: u'Katarina', 56: u'Nocturne', 57: u'Maokai', 58: u'Renekton', 59: u'JarvanIV', 60: u'Elise', 61: u'Orianna', 62: u'MonkeyKing', 63: u'Brand', 64: u'LeeSin', 67: u'Vayne', 68: u'Rumble', 69: u'Cassiopeia', 72: u'Skarner', 74: u'Heimerdinger', 75: u'Nasus', 76: u'Nidalee', 77: u'Udyr', 78: u'Poppy', 79: u'Gragas', 80: u'Pantheon', 81: u'Ezreal', 82: u'Mordekaiser', 83: u'Yorick', 84: u'Akali', 85: u'Kennen', 86: u'Garen', 89: u'Leona', 90: u'Malzahar', 91: u'Talon', 92: u'Riven', 96: u'KogMaw', 98: u'Shen', 99: u'Lux', 101: u'Xerath', 102: u'Shyvana', 103: u'Ahri', 104: u'Graves', 105: u'Fizz', 106: u'Volibear', 107: u'Rengar', 110: u'Varus', 111: u'Nautilus', 112: u'Viktor', 113: u'Sejuani', 114: u'Fiora', 115: u'Ziggs', 117: u'Lulu', 119: u'Draven', 120: u'Hecarim', 121: u'Khazix', 122: u'Darius', 126: u'Jayce', 127: u'Lissandra', 131: u'Diana', 133: u'Quinn', 134: u'Syndra', 136: u'AurelionSol', 143: u'Zyra', 150: u'Gnar', 154: u'Zac', 157: u'Yasuo', 161: u'Velkoz', 163: u'Taliyah', 201: u'Braum', 202: u'Jhin', 203: u'Kindred', 222: u'Jinx', 223: u'TahmKench', 236: u'Lucian', 238: u'Zed', 240: u'Kled', 245: u'Ekko', 254: u'Vi', 266: u'Aatrox', 267: u'Nami', 268: u'Azir', 412: u'Thresh', 420: u'Illaoi', 421: u'RekSai', 427: u'Ivern', 429: u'Kalista', 432: u'Bard'}
champion_names = ['MonkeyKing_1', 'Jax_1', 'Shaco_1', 'Warwick_1', 'Nidalee_1', 'Zyra_1', 'Kled_1', 'Brand_1', 'Rammus_1', 'Illaoi_1', 'Corki_1', 'Braum_1', 'Darius_1', 'Tryndamere_1', 'MissFortune_1', 'Yorick_1', 'Xerath_1', 'Sivir_1', 'Riven_1', 'Orianna_1', 'Gangplank_1', 'Malphite_1', 'Poppy_1', 'Karthus_1', 'Jayce_1', 'Nunu_1', 'Trundle_1', 'Graves_1', 'Morgana_1', 'Gnar_1', 'Lux_1', 'Shyvana_1', 'Renekton_1', 'Fiora_1', 'Jinx_1', 'Kalista_1', 'Fizz_1', 'Kassadin_1', 'Sona_1', 'Irelia_1', 'Viktor_1', 'Kindred_1', 'Cassiopeia_1', 'Maokai_1', 'Thresh_1', 'Kayle_1', 'Hecarim_1', 'Khazix_1', 'Olaf_1', 'Ziggs_1', 'Syndra_1', 'DrMundo_1', 'Karma_1', 'Annie_1', 'Akali_1', 'Volibear_1', 'Yasuo_1', 'Kennen_1', 'Rengar_1', 'Ryze_1', 'Shen_1', 'Zac_1', 'Talon_1', 'Swain_1', 'Bard_1', 'Sion_1', 'Vayne_1', 'Nasus_1', 'TwistedFate_1', 'Chogath_1', 'Udyr_1', 'Lucian_1', 'Ivern_1', 'Leona_1', 'Caitlyn_1', 'Sejuani_1', 'Nocturne_1', 'Zilean_1', 'Azir_1', 'Rumble_1', 'Taliyah_1', 'Teemo_1', 'Urgot_1', 'Amumu_1', 'Galio_1', 'Heimerdinger_1', 'Anivia_1', 'Ashe_1', 'Velkoz_1', 'Singed_1', 'Skarner_1', 'Varus_1', 'Twitch_1', 'Garen_1', 'Blitzcrank_1', 'MasterYi_1', 'Elise_1', 'Alistar_1', 'Katarina_1', 'Ekko_1', 'Mordekaiser_1', 'Lulu_1', 'Aatrox_1', 'Draven_1', 'TahmKench_1', 'FiddleSticks_1', 'Pantheon_1', 'XinZhao_1', 'AurelionSol_1', 'LeeSin_1', 'Taric_1', 'Malzahar_1', 'Lissandra_1', 'Diana_1', 'Tristana_1', 'RekSai_1', 'Vladimir_1', 'JarvanIV_1', 'Nami_1', 'Jhin_1', 'Soraka_1', 'Veigar_1', 'Janna_1', 'Nautilus_1', 'Evelynn_1', 'Gragas_1', 'Zed_1', 'Vi_1', 'KogMaw_1', 'Ahri_1', 'Quinn_1', 'Leblanc_1', 'Ezreal_1', 'MonkeyKing_2', 'Jax_2', 'Shaco_2', 'Warwick_2', 'Nidalee_2', 'Zyra_2', 'Kled_2', 'Brand_2', 'Rammus_2', 'Illaoi_2', 'Corki_2', 'Braum_2', 'Darius_2', 'Tryndamere_2', 'MissFortune_2', 'Yorick_2', 'Xerath_2', 'Sivir_2', 'Riven_2', 'Orianna_2', 'Gangplank_2', 'Malphite_2', 'Poppy_2', 'Karthus_2', 'Jayce_2', 'Nunu_2', 'Trundle_2', 'Graves_2', 'Morgana_2', 'Gnar_2', 'Lux_2', 'Shyvana_2', 'Renekton_2', 'Fiora_2', 'Jinx_2', 'Kalista_2', 'Fizz_2', 'Kassadin_2', 'Sona_2', 'Irelia_2', 'Viktor_2', 'Kindred_2', 'Cassiopeia_2', 'Maokai_2', 'Thresh_2', 'Kayle_2', 'Hecarim_2', 'Khazix_2', 'Olaf_2', 'Ziggs_2', 'Syndra_2', 'DrMundo_2', 'Karma_2', 'Annie_2', 'Akali_2', 'Volibear_2', 'Yasuo_2', 'Kennen_2', 'Rengar_2', 'Ryze_2', 'Shen_2', 'Zac_2', 'Talon_2', 'Swain_2', 'Bard_2', 'Sion_2', 'Vayne_2', 'Nasus_2', 'TwistedFate_2', 'Chogath_2', 'Udyr_2', 'Lucian_2', 'Ivern_2', 'Leona_2', 'Caitlyn_2', 'Sejuani_2', 'Nocturne_2', 'Zilean_2', 'Azir_2', 'Rumble_2', 'Taliyah_2', 'Teemo_2', 'Urgot_2', 'Amumu_2', 'Galio_2', 'Heimerdinger_2', 'Anivia_2', 'Ashe_2', 'Velkoz_2', 'Singed_2', 'Skarner_2', 'Varus_2', 'Twitch_2', 'Garen_2', 'Blitzcrank_2', 'MasterYi_2', 'Elise_2', 'Alistar_2', 'Katarina_2', 'Ekko_2', 'Mordekaiser_2', 'Lulu_2', 'Aatrox_2', 'Draven_2', 'TahmKench_2', 'FiddleSticks_2', 'Pantheon_2', 'XinZhao_2', 'AurelionSol_2', 'LeeSin_2', 'Taric_2', 'Malzahar_2', 'Lissandra_2', 'Diana_2', 'Tristana_2', 'RekSai_2', 'Vladimir_2', 'JarvanIV_2', 'Nami_2', 'Jhin_2', 'Soraka_2', 'Veigar_2', 'Janna_2', 'Nautilus_2', 'Evelynn_2', 'Gragas_2', 'Zed_2', 'Vi_2', 'KogMaw_2', 'Ahri_2', 'Quinn_2', 'Leblanc_2', 'Ezreal_2']
blueteam = ['MonkeyKing_1', 'Jax_1', 'Shaco_1', 'Warwick_1', 'Nidalee_1', 'Zyra_1', 'Kled_1', 'Brand_1', 'Rammus_1', 'Illaoi_1', 'Corki_1', 'Braum_1', 'Darius_1', 'Tryndamere_1', 'MissFortune_1', 'Yorick_1', 'Xerath_1', 'Sivir_1', 'Riven_1', 'Orianna_1', 'Gangplank_1', 'Malphite_1', 'Poppy_1', 'Karthus_1', 'Jayce_1', 'Nunu_1', 'Trundle_1', 'Graves_1', 'Morgana_1', 'Gnar_1', 'Lux_1', 'Shyvana_1', 'Renekton_1', 'Fiora_1', 'Jinx_1', 'Kalista_1', 'Fizz_1', 'Kassadin_1', 'Sona_1', 'Irelia_1', 'Viktor_1', 'Kindred_1', 'Cassiopeia_1', 'Maokai_1', 'Thresh_1', 'Kayle_1', 'Hecarim_1', 'Khazix_1', 'Olaf_1', 'Ziggs_1', 'Syndra_1', 'DrMundo_1', 'Karma_1', 'Annie_1', 'Akali_1', 'Volibear_1', 'Yasuo_1', 'Kennen_1', 'Rengar_1', 'Ryze_1', 'Shen_1', 'Zac_1', 'Talon_1', 'Swain_1', 'Bard_1', 'Sion_1', 'Vayne_1', 'Nasus_1', 'TwistedFate_1', 'Chogath_1', 'Udyr_1', 'Lucian_1', 'Ivern_1', 'Leona_1', 'Caitlyn_1', 'Sejuani_1', 'Nocturne_1', 'Zilean_1', 'Azir_1', 'Rumble_1', 'Taliyah_1', 'Teemo_1', 'Urgot_1', 'Amumu_1', 'Galio_1', 'Heimerdinger_1', 'Anivia_1', 'Ashe_1', 'Velkoz_1', 'Singed_1', 'Skarner_1', 'Varus_1', 'Twitch_1', 'Garen_1', 'Blitzcrank_1', 'MasterYi_1', 'Elise_1', 'Alistar_1', 'Katarina_1', 'Ekko_1', 'Mordekaiser_1', 'Lulu_1', 'Aatrox_1', 'Draven_1', 'TahmKench_1', 'FiddleSticks_1', 'Pantheon_1', 'XinZhao_1', 'AurelionSol_1', 'LeeSin_1', 'Taric_1', 'Malzahar_1', 'Lissandra_1', 'Diana_1', 'Tristana_1', 'RekSai_1', 'Vladimir_1', 'JarvanIV_1', 'Nami_1', 'Jhin_1', 'Soraka_1', 'Veigar_1', 'Janna_1', 'Nautilus_1', 'Evelynn_1', 'Gragas_1', 'Zed_1', 'Vi_1', 'KogMaw_1', 'Ahri_1', 'Quinn_1', 'Leblanc_1', 'Ezreal_1']
redteam = ['MonkeyKing_2', 'Jax_2', 'Shaco_2', 'Warwick_2', 'Nidalee_2', 'Zyra_2', 'Kled_2', 'Brand_2', 'Rammus_2', 'Illaoi_2', 'Corki_2', 'Braum_2', 'Darius_2', 'Tryndamere_2', 'MissFortune_2', 'Yorick_2', 'Xerath_2', 'Sivir_2', 'Riven_2', 'Orianna_2', 'Gangplank_2', 'Malphite_2', 'Poppy_2', 'Karthus_2', 'Jayce_2', 'Nunu_2', 'Trundle_2', 'Graves_2', 'Morgana_2', 'Gnar_2', 'Lux_2', 'Shyvana_2', 'Renekton_2', 'Fiora_2', 'Jinx_2', 'Kalista_2', 'Fizz_2', 'Kassadin_2', 'Sona_2', 'Irelia_2', 'Viktor_2', 'Kindred_2', 'Cassiopeia_2', 'Maokai_2', 'Thresh_2', 'Kayle_2', 'Hecarim_2', 'Khazix_2', 'Olaf_2', 'Ziggs_2', 'Syndra_2', 'DrMundo_2', 'Karma_2', 'Annie_2', 'Akali_2', 'Volibear_2', 'Yasuo_2', 'Kennen_2', 'Rengar_2', 'Ryze_2', 'Shen_2', 'Zac_2', 'Talon_2', 'Swain_2', 'Bard_2', 'Sion_2', 'Vayne_2', 'Nasus_2', 'TwistedFate_2', 'Chogath_2', 'Udyr_2', 'Lucian_2', 'Ivern_2', 'Leona_2', 'Caitlyn_2', 'Sejuani_2', 'Nocturne_2', 'Zilean_2', 'Azir_2', 'Rumble_2', 'Taliyah_2', 'Teemo_2', 'Urgot_2', 'Amumu_2', 'Galio_2', 'Heimerdinger_2', 'Anivia_2', 'Ashe_2', 'Velkoz_2', 'Singed_2', 'Skarner_2', 'Varus_2', 'Twitch_2', 'Garen_2', 'Blitzcrank_2', 'MasterYi_2', 'Elise_2', 'Alistar_2', 'Katarina_2', 'Ekko_2', 'Mordekaiser_2', 'Lulu_2', 'Aatrox_2', 'Draven_2', 'TahmKench_2', 'FiddleSticks_2', 'Pantheon_2', 'XinZhao_2', 'AurelionSol_2', 'LeeSin_2', 'Taric_2', 'Malzahar_2', 'Lissandra_2', 'Diana_2', 'Tristana_2', 'RekSai_2', 'Vladimir_2', 'JarvanIV_2', 'Nami_2', 'Jhin_2', 'Soraka_2', 'Veigar_2', 'Janna_2', 'Nautilus_2', 'Evelynn_2', 'Gragas_2', 'Zed_2', 'Vi_2', 'KogMaw_2', 'Ahri_2', 'Quinn_2', 'Leblanc_2', 'Ezreal_2']
"""
Calculate Average Mastery Score

1. Get list of players in the game
2. Get their champion picks
3. Look up each player mastery based on pick
4. Add to players total and divide by 5

"""


def getMastery(summonerId, championId):

    response = requests.get("https://na.api.pvp.net/championmastery/location/NA1/player/"+str(summonerId)+"/champion/"+str(championId)+"?api_key="+str(apikey))


    if response.status_code == 429:
        print "Unsuccessful Mastery Call: 429"
        for i in range(3):
            time.sleep(10)
            response = requests.get("https://na.api.pvp.net/championmastery/location/NA1/player/"+str(summonerId)+"/champion/"+str(championId)+"?api_key="+str(apikey))
            if response.status_code == 200:
                print "Mastery Call Successfully Recovered"
                print response.headers
                break
            else:
                mastery = 1
                return mastery



    if response.status_code == 500:
        print "Unsuccessful Mastery Call: 500"
        mastery = 1
        return mastery
        new_summonerId = 48349059
        for i in range(5):
            time.sleep(30)
            new_response = requests.get("https://na.api.pvp.net/championmastery/location/NA1/player/"+str(summonerId)+"/champion/"+str(championId)+"?api_key="+str(apikey))
            if response.status_code  == 200:
                print "Mastery Call Successfully Recovered"
                data = new_response.json()


    data = response.json()
    mastery = data["championLevel"]

    time.sleep(1)
    return mastery


"""
Training Data Sample

2*133 Features are champions with binary 0 (not present) or 1 (present)
2 Features are dedicated to average champion mastery of each respective team
1 Feature indicating patch number (for future extensibility purposes)
1 Class label that has 0 (blue team win) or 1 (red team win)


"""
#filename = 'test_matches.txt' # for debugging with just 2 matches


with open(filename) as f:
    matchlist = f.readlines()
    matchlist = [int(x) for x in matchlist]

remaining_features = ['BLUE_AVG_MASTERY','RED_AVG_MASTERY','WINNER']
features = champion_names
features.extend(remaining_features)
data = []

counter = 0
start_time = time.time()
for matchId in matchlist:
    participantIds = []
    championPicks = []
    playerIds = []
    data_sample = [0]*269
    start_sample_time = time.time()

    response = requests.get("https://na.api.pvp.net/api/lol/na/v2.2/match/"+str(matchId)+"?api_key="+str(apikey))

    if response.status_code == 429:
        print "Unsuccessful Match Call: 429"
        for i in range(3):
            time.sleep(15)
            response = requests.get("https://na.api.pvp.net/api/lol/na/v2.2/match/"+str(matchId)+"?api_key="+str(apikey))
            if response.status_code == 200:
                print "Match Call Successfully Recovered"
                break

    if response.status_code == 500:
        print "Unsuccessful Match Call: 500"
        matchId = 2346376881
        time.sleep(10)
        response = requests.get("https://na.api.pvp.net/api/lol/na/v2.2/match/"+str(matchId)+"?api_key="+str(apikey))

    match_data = response.json()
    #print match_data

    for i in range(0,10):
        participantIds.append(match_data["participantIdentities"][i]["player"]["summonerId"])
        playerIds.append(match_data["participants"][i]["participantId"])
        championPicks.append(match_data["participants"][i]["championId"])
        #print championPicks

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
    red_champs = []
    for i in range(5,10):
        red_champs.append(championIds[championPicks[i]]+"_2")

    for j in range(132):
        for i in range(0,5):
            if  red_champs[i] == redteam[j]:
                data_sample[j+133] = 1
            elif data_sample[j+133] == 1:
                data_sample[j+133] = 1
            else:
                data_sample[j+133] = 0

    #print "Red Team: ", red_champs


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

    #data_file = 'data_gold.txt'
    temp_data = { matchId : data_sample }

    counter += 1
    print str(counter) + " samples added. Latest matchId: " + str(matchId)
    finish_sample_time = (time.time() - start_sample_time)
    print "Elapsed Time for Sample: " + str(finish_sample_time) + " seconds"

df = pd.DataFrame(data, columns=features)
df.to_csv(csv_file)
finish_time = (time.time() - start_time)
print "Finished in: " + str(finish_time) + " seconds"
