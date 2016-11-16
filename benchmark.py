"""
benchmark.py

Create the benchmark model and evaluate its performance using accuracy and f1 Score

"""
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score


champion_winrates = {u'MonkeyKing': 51.21, u'Jax': 50.55, u'Shaco': 51.63, u'Warwick': 47.47, u'Nidalee': 42.49, u'Zyra': 53.46, u'Kled': 49.98, u'Brand': 54.05, u'Rammus': 52.11, u'Illaoi': 49.91, u'Corki': 49.71, u'Braum': 50.35, u'Darius': 50.94, u'Tryndamere': 46.29, u'MissFortune': 51, u'Blitzcrank': 51.18, u'Yorick': 51.33, u'Xerath': 53.05, u'Sivir': 49.83, u'Riven': 51.55, u'Orianna': 52.75, u'Gangplank': 51.27, u'Malphite': 45.52, u'Poppy': 51.95, u'Karthus': 53.93, u'Jayce': 53.08, u'Nunu': 52.53, u'Trundle': 49.06, u'Graves': 50.04, u'Lucian': 47.01, u'Gnar': 46.76, u'Lux': 45.66, u'Shyvana': 48.19, u'Renekton': 50.14, u'XinZhao': 49.13, u'Jinx': 51.25, u'Kalista': 43.33, u'Fizz': 48.27, u'Kassadin': 50.29, u'Sona': 52.34, u'Vladimir': 46.06, u'Viktor': 53.2, u'Kindred': 48.47, u'Cassiopeia': 51.11, u'Maokai': 47.61, u'Thresh': 49.21, u'Kayle': 53.94, u'Hecarim': 54.7, u'Khazix': 50.3, u'Olaf': 49.78, u'Ziggs': 55.36, u'Syndra': 52.42, u'DrMundo': 47.32, u'Karma': 50.66, u'Annie': 48.21, u'Akali': 41.75, u'Volibear': 52.32, u'Yasuo': 48.42, u'Kennen': 52.48, u'Rengar': 46.52, u'Ryze': 46.82, u'Shen': 43.51, u'Zac': 52.49, u'Talon': 44.34, u'Swain': 53.98, u'Bard': 48.45, u'Sion': 56.7, u'Vayne': 53.19, u'Nasus': 51.78, u'TwistedFate': 53.99, u'Chogath': 49.75, u'Udyr': 51.7, u'Morgana': 49.58, u'Ivern': 46.12, u'Leona': 51.52, u'Caitlyn': 52.01, u'Sejuani': 52.36, u'Nocturne': 52.32, u'Zilean': 51.26, u'Azir': 44.58, u'Rumble': 49.55, u'Skarner': 53.6, u'Teemo': 51.31, u'Urgot': 51.32, u'Amumu': 51.73, u'Galio': 53.07, u'Heimerdinger': 48.91, u'Anivia': 55.37, u'Ashe': 49.35, u'Velkoz': 52.43, u'Singed': 53.28, u'Taliyah': 50.48, u'Varus': 47.82, u'Twitch': 53.01, u'Garen': 46.98, u'Diana': 52.49, u'MasterYi': 46.88, u'Elise': 49.93, u'Alistar': 47.88, u'Katarina': 41.33, u'Ekko': 52.45, u'Mordekaiser': 48.66, u'Lulu': 49.67, u'Aatrox': 42.1, u'Draven': 50.11, u'TahmKench': 50.06, u'FiddleSticks': 50.9, u'Pantheon': 49.11, u'Fiora': 49.93, u'AurelionSol': 52.78, u'LeeSin': 51.47, u'Taric': 52.32, u'Malzahar': 54.83, u'Lissandra': 50.55, u'Tristana': 50.01, u'RekSai': 50.42, u'Irelia': 51.31, u'JarvanIV': 50.9, u'Nami': 52.5, u'Jhin': 51.88, u'Soraka': 52.63, u'Veigar': 51.7, u'Janna': 55.08, u'Nautilus': 51.15, u'Evelynn': 50.9, u'Gragas': 48.96, u'Zed': 47.47, u'Vi': 53.26, u'KogMaw': 47.23, u'Ahri': 54.8, u'Quinn': 46.72, u'Leblanc': 47.5, u'Ezreal': 49.6}
y_pred = []

filename = 'data.csv'
data = pd.read_csv(filename)
print "Match data read succsesfully!"

columns = list(data.columns[:-3])
target = data.columns[-1]
labels = data['WINNER']

for index,row in data.iterrows():
    blueteam = []
    blueteam_total_winrate = 0
    redteam_total_winrate = 0
    redteam = []
    for champ in columns:
        if row[champ] == 1 and champ[-2:] == "_1":
            blueteam.append(champ[:-2])
        if row[champ] == 1 and champ[-2:] == "_2":
            redteam.append(champ[:-2])
    for i in blueteam:
        winrate = champion_winrates[i]
        blueteam_total_winrate += winrate
    for i in redteam:
        winrate = champion_winrates[i]
        redteam_total_winrate += winrate

    BLUE_AVG_WINRATE = blueteam_total_winrate/5.0
    RED_AVG_WINRATE = redteam_total_winrate/5.0

    if BLUE_AVG_WINRATE > RED_AVG_WINRATE:
        y_pred.append(1)
    else:
        y_pred.append(0)

# Evaluate Performance
print "Number of Predictions: ", len(labels)
print "Benchmark Accuracy: ", accuracy_score(labels, y_pred)
print "Benchmark F1 Score: ", f1_score(labels, y_pred)
