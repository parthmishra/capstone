"""
classify.py

Creates several linear classifiers to predict winners in matches of Leauge of Legends

Author: Parth Mishra
Copyright 2016

"""

from time import time
import numpy as np
import pandas as pd


from sklearn.model_selection import train_test_split
from sklearn.datasets import fetch_lfw_people
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier


################################################################################
"""
Step 1: Gather input data

Data is taken from premade csv files available in the project folder.

"""

filename = 'data.csv'
data = pd.read_csv(filename)

print "Match data read succsesfully!"


################################################################################
"""
Step 2: Data Exploration

A series of descriptive statistics and visualizations of the data

"""


winner_counts = data['WINNER'].value_counts()
blue_mastery = data['BLUE_AVG_MASTERY'].mean()
red_mastery = data['RED_AVG_MASTERY'].mean()
champion_counts = data['Sona_1'].value_counts()
#print "Counts: ", counts

num_blue_wins = winner_counts[1]
num_red_wins = winner_counts[0]
avg_mastery = ( blue_mastery + red_mastery ) / 2
champion_names = ['MonkeyKing_1', 'Jax_1', 'Shaco_1', 'Warwick_1', 'Nidalee_1', 'Zyra_1', 'Kled_1', 'Brand_1', 'Rammus_1', 'Illaoi_1', 'Corki_1', 'Braum_1', 'Darius_1', 'Tryndamere_1', 'MissFortune_1', 'Yorick_1', 'Xerath_1', 'Sivir_1', 'Riven_1', 'Orianna_1', 'Gangplank_1', 'Malphite_1', 'Poppy_1', 'Karthus_1', 'Jayce_1', 'Nunu_1', 'Trundle_1', 'Graves_1', 'Morgana_1', 'Gnar_1', 'Lux_1', 'Shyvana_1', 'Renekton_1', 'Fiora_1', 'Jinx_1', 'Kalista_1', 'Fizz_1', 'Kassadin_1', 'Sona_1', 'Irelia_1', 'Viktor_1', 'Kindred_1', 'Cassiopeia_1', 'Maokai_1', 'Thresh_1', 'Kayle_1', 'Hecarim_1', 'Khazix_1', 'Olaf_1', 'Ziggs_1', 'Syndra_1', 'DrMundo_1', 'Karma_1', 'Annie_1', 'Akali_1', 'Volibear_1', 'Yasuo_1', 'Kennen_1', 'Rengar_1', 'Ryze_1', 'Shen_1', 'Zac_1', 'Talon_1', 'Swain_1', 'Bard_1', 'Sion_1', 'Vayne_1', 'Nasus_1', 'TwistedFate_1', 'Chogath_1', 'Udyr_1', 'Lucian_1', 'Ivern_1', 'Leona_1', 'Caitlyn_1', 'Sejuani_1', 'Nocturne_1', 'Zilean_1', 'Azir_1', 'Rumble_1', 'Taliyah_1', 'Teemo_1', 'Urgot_1', 'Amumu_1', 'Galio_1', 'Heimerdinger_1', 'Anivia_1', 'Ashe_1', 'Velkoz_1', 'Singed_1', 'Skarner_1', 'Varus_1', 'Twitch_1', 'Garen_1', 'Blitzcrank_1', 'MasterYi_1', 'Elise_1', 'Alistar_1', 'Katarina_1', 'Ekko_1', 'Mordekaiser_1', 'Lulu_1', 'Aatrox_1', 'Draven_1', 'TahmKench_1', 'FiddleSticks_1', 'Pantheon_1', 'XinZhao_1', 'AurelionSol_1', 'LeeSin_1', 'Taric_1', 'Malzahar_1', 'Lissandra_1', 'Diana_1', 'Tristana_1', 'RekSai_1', 'Vladimir_1', 'JarvanIV_1', 'Nami_1', 'Jhin_1', 'Soraka_1', 'Veigar_1', 'Janna_1', 'Nautilus_1', 'Evelynn_1', 'Gragas_1', 'Zed_1', 'Vi_1', 'KogMaw_1', 'Ahri_1', 'Quinn_1', 'Leblanc_1', 'Ezreal_1', 'MonkeyKing_2', 'Jax_2', 'Shaco_2', 'Warwick_2', 'Nidalee_2', 'Zyra_2', 'Kled_2', 'Brand_2', 'Rammus_2', 'Illaoi_2', 'Corki_2', 'Braum_2', 'Darius_2', 'Tryndamere_2', 'MissFortune_2', 'Yorick_2', 'Xerath_2', 'Sivir_2', 'Riven_2', 'Orianna_2', 'Gangplank_2', 'Malphite_2', 'Poppy_2', 'Karthus_2', 'Jayce_2', 'Nunu_2', 'Trundle_2', 'Graves_2', 'Morgana_2', 'Gnar_2', 'Lux_2', 'Shyvana_2', 'Renekton_2', 'Fiora_2', 'Jinx_2', 'Kalista_2', 'Fizz_2', 'Kassadin_2', 'Sona_2', 'Irelia_2', 'Viktor_2', 'Kindred_2', 'Cassiopeia_2', 'Maokai_2', 'Thresh_2', 'Kayle_2', 'Hecarim_2', 'Khazix_2', 'Olaf_2', 'Ziggs_2', 'Syndra_2', 'DrMundo_2', 'Karma_2', 'Annie_2', 'Akali_2', 'Volibear_2', 'Yasuo_2', 'Kennen_2', 'Rengar_2', 'Ryze_2', 'Shen_2', 'Zac_2', 'Talon_2', 'Swain_2', 'Bard_2', 'Sion_2', 'Vayne_2', 'Nasus_2', 'TwistedFate_2', 'Chogath_2', 'Udyr_2', 'Lucian_2', 'Ivern_2', 'Leona_2', 'Caitlyn_2', 'Sejuani_2', 'Nocturne_2', 'Zilean_2', 'Azir_2', 'Rumble_2', 'Taliyah_2', 'Teemo_2', 'Urgot_2', 'Amumu_2', 'Galio_2', 'Heimerdinger_2', 'Anivia_2', 'Ashe_2', 'Velkoz_2', 'Singed_2', 'Skarner_2', 'Varus_2', 'Twitch_2', 'Garen_2', 'Blitzcrank_2', 'MasterYi_2', 'Elise_2', 'Alistar_2', 'Katarina_2', 'Ekko_2', 'Mordekaiser_2', 'Lulu_2', 'Aatrox_2', 'Draven_2', 'TahmKench_2', 'FiddleSticks_2', 'Pantheon_2', 'XinZhao_2', 'AurelionSol_2', 'LeeSin_2', 'Taric_2', 'Malzahar_2', 'Lissandra_2', 'Diana_2', 'Tristana_2', 'RekSai_2', 'Vladimir_2', 'JarvanIV_2', 'Nami_2', 'Jhin_2', 'Soraka_2', 'Veigar_2', 'Janna_2', 'Nautilus_2', 'Evelynn_2', 'Gragas_2', 'Zed_2', 'Vi_2', 'KogMaw_2', 'Ahri_2', 'Quinn_2', 'Leblanc_2', 'Ezreal_2']
champion_winrates = {u'MonkeyKing': 51.21, u'Jax': 50.55, u'Shaco': 51.63, u'Warwick': 47.47, u'Nidalee': 42.49, u'Kled': 49.98, u'Rammus': 52.11, u'Illaoi': 49.91, u'Corki': 56.16, u'Darius': 50.94, u'Tryndamere': 46.29, u'Yorick': 51.33, u'Xerath': 53.05, u'Riven': 51.55, u'Gangplank': 49, u'Malphite': 53, u'Poppy': 51.95, u'Karthus': 53.93, u'Jayce': 52.7, u'Nunu': 52.53, u'Trundle': 49.06, u'Graves': 50.04, u'Gnar': 46.76, u'Shyvana': 48.19, u'Renekton': 50.14, u'XinZhao': 49.13, u'Fizz': 44.38, u'Kassadin': 50.29, u'Vladimir': 46.06, u'Kindred': 48.47, u'Cassiopeia': 51.11, u'Maokai': 47.61, u'Kayle': 53.94, u'Hecarim': 54.7, u'Khazix': 50.3, u'Olaf': 49.78, u'Ziggs': 55.36, u'DrMundo': 47.32, u'Akali': 44.02, u'Volibear': 52.32, u'Yasuo': 50.52, u'Kennen': 52.19, u'Rengar': 46.52, u'Ryze': 45.54, u'Shen': 48.02, u'Zac': 52.49, u'Talon': 41.04, u'Swain': 53.98, u'Sion': 51, u'Nasus': 51.78, u'TwistedFate': 53.99, u'Chogath': 49.75, u'Udyr': 51.7, u'Ivern': 53.79, u'Sejuani': 52.36, u'Nocturne': 52.32, u'Zilean': 53.98, u'Azir': 44.58, u'Rumble': 49.55, u'Skarner': 53.6, u'Teemo': 51.31, u'Urgot': 49.28, u'Amumu': 51.73, u'Galio': 53.07, u'Heimerdinger': 48.91, u'Anivia': 55.37, u'Velkoz': 55.13, u'Singed': 53.28, u'Taliyah': 50.48, u'Varus': 46.75, u'Twitch': 49.56, u'Garen': 46.98, u'Diana': 52.49, u'MasterYi': 46.88, u'Elise': 49.93, u'Ekko': 46.93, u'Mordekaiser': 48.66, u'Aatrox': 42.1, u'TahmKench': 51.42, u'FiddleSticks': 51.72, u'Pantheon': 49.11, u'Fiora': 49.93, u'AurelionSol': 52.78, u'LeeSin': 51.47, u'Malzahar': 54.83, u'Lissandra': 50.55, u'RekSai': 50.42, u'Irelia': 51.31, u'JarvanIV': 50.9, u'Veigar': 50.16, u'Nautilus': 51.7, u'Evelynn': 50.9, u'Gragas': 48.96, u'Vi': 53.26, u'KogMaw': 55.91, u'Quinn': 49.83}
picks = {}
top_picks = []

"""
for champ in champion_names:
    champ_entries = data[champ].value_counts()
    print champ_entries

print picks

for i in range(5):
    top_champ = max(picks, key=picks.get)
    top_picks.append(top_champ)
    picks.pop(champ, None)
"""

print "Blue wins: ", num_blue_wins
print "Red wins: ", num_red_wins
print "Average Mastery (-1 to 1): ", avg_mastery
#80print "Top 5 Most Picked Champions: ", top_picks



################################################################################
"""
Step 3: Create Training and Testing Data

After loading in the data, split it into a training and test set

"""
print "Creating training and test data..."

features = list(data.columns[:-1])
target = data.columns[-1]

X = data[features]
y = data[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


################################################################################
"""
Step 4: Preprocessing

Engage in preprocessing (specifically PCA) of the data to reduce input dimensionality

"""
print "Preprocessing..."

n_components = 30

pca = PCA(svd_solver='randomized', n_components = n_components).fit(X_train)

X_train_pca = pca.transform(X_train)
X_test_pca = pca.transform(X_test)



################################################################################

"""
Step 5: Classification

3 Classifiers to make:

1. SVMs
2. Decision Forests
3. Logistic Regression
"""

# Create Baseline Performance model
"""
for i in range(700):
    for champ in champion_names:


"""
def trainTestClassifier(X_train, X_test, y_train, y_test, clf_type, *params):

    classifiers = {
    "svm": SVC,
    "lr" : LogisticRegression,
    "rf" : RandomForestClassifier,
    "dt" : DecisionTreeClassifier,
    "sgd": SGDClassifier,
    "nb" : GaussianNB
    }
    if clf_type == "nb":
        clf = classifiers[clf_type]()
    else:
        clf = classifiers[clf_type](random_state=42)


    if params:
        clf = GridSearchCV(clf, params)

    # train
    clf = clf.fit(X_train, y_train)

    # test
    y_pred = clf.predict(X_test)


    clf_accuracy = accuracy_score(y_test, y_pred)

    #clf_f1_score = f1_score(y_test, y_pred)


    return clf_accuracy


print "Fitting classifiers..."

# Parameters for Optimizer
svm_parameters = { 'C':[1e3, 5e3, 1e4, 5e4, 1e5, 1.0, 0.5, 0.0001],
                    'gamma': [0.0001, 0.0005, 0.001, 0.01, 0.1, 0.5, 0.7, 'auto'] }

lr_parameters = { 'C':[1e3, 5e3, 1e4, 5e4, 1e5, 1.0, 0.1],
                  'solver': ['newton-cg','lbfgs','liblinear']}

rf_parameters = {"n_estimators": [5,10,15],
                "max_depth": [3, None],
                "bootstrap": [True,False]}


classifiers = { "svm": { 'C':[1e3, 5e3, 1e4, 5e4, 1e5, 1.0, 0.5, 0.0001],
                        'gamma': [0.0001, 0.0005, 0.001, 0.01, 0.1, 0.5, 0.7,'auto']},
                "lr": { 'C':[1e3, 5e3, 1e4, 5e4, 1e5, 1.0, 0.1],
                        'solver': ['newton-cg','lbfgs','liblinear']},
                "rf": { "n_estimators": [5,10,15],
                        "max_depth": [3, None],
                        "bootstrap": [True,False]},
                "nb": {},
                "sgd": { 'loss' : ['hinge', 'log', 'modified_huber', 'squared_hinge', 'perceptron'],
                         'penalty' : ['none', 'l2', 'l1', 'elasticnet'],
                         'alpha' : [0.7,0.5,0.1,0.01,0.001,0.0001,0.00001],
                         'eta0' : [0.1],
                         'learning_rate' : ['constant','optimal','invscaling']
                       },
                "dt": {}
              }

for clf_type, clf_params in classifiers.iteritems():
    #print "clf_type: ", clf_type
    #print "clf_params: ", clf_params
    clf_accuracy = trainTestClassifier(X_train_pca, X_test_pca, y_train, y_test, clf_type)
    print clf_type.upper() + " Accuracy: " + str(clf_accuracy)
