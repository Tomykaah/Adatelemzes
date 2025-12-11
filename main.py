import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime as dt
import ownfunctions as of

games             = pd.read_csv('Games.csv', low_memory = False)
players           = pd.read_csv('Players.csv', low_memory = False)
playerStatistics  = pd.read_csv('PlayerStatistics.csv', low_memory = False)
teamStatistics    = pd.read_csv('TeamStatistics.csv', low_memory = False)
teamHistories     = pd.read_csv('TeamHistories.csv', low_memory = False)
playerStatistics['season'] = playerStatistics['gameDateTimeEst'].apply(of.determine_season)
##### 1. Ki volt az a játékos, aki a legtöbb pontot dobta egy meccsen az NBA történelmében?
mostPoints = playerStatistics['points'].max()
mostPointsPlayer = playerStatistics[playerStatistics['points'] == mostPoints]
mostPointsName = mostPointsPlayer['firstName'] + ' ' + mostPointsPlayer['lastName']

print('###1###')
print('A legtöbb pontot dobó játékos: ', mostPointsName, ', pontszáma: ', mostPoints)

##### 2. Melyik az a csapat, amelyik a legtöbb győzelmet érte el összesen?
mostWinsTeam = teamStatistics.groupby('teamId')['win'].sum().idxmax()
print('###2###')
print('A legtöbb győzelmet elérő csapat: ', teamHistories[teamHistories['teamId'] == mostWinsTeam][['teamCity', 'teamName']].drop_duplicates(), ', győzelmeik száma: ', teamStatistics.groupby('teamId')['win'].sum().max())

##### 3. Ki az a játékos, aki a legidősebb volt, amikor utolsó mérkőzését játszotta?
longestCareer = 0

playersWithAge = players.dropna(subset = ['birthdate'])
playersWithAge = playersWithAge[playersWithAge['birthdate'] != '1900-01-01']

playerStatistics['gameDateTimeEst'] = playerStatistics['gameDateTimeEst'].apply(of.convert_ts_to_right_format)
for index, row in playersWithAge.iterrows():
    lastGame = playerStatistics[playerStatistics['personId'] == row['personId']].sort_values(by = ['gameDateTimeEst'], ascending = False)

    if lastGame.empty:
        continue
    
    lastGame = lastGame.iloc[0]
    lastGameDate = lastGame['gameDateTimeEst']
    
    birthDate = dt.strptime(row['birthdate'], '%Y-%m-%d').date()
    currentCareer = lastGameDate - birthDate    
    
    if longestCareer < currentCareer.days:
        longestCareer = currentCareer.days
        longestCareerPlayer = row['personId']

longestCareerPlayerFirstName = players[players['personId'] == longestCareerPlayer]['firstName'].values[0]
longestCareerPlayerLastName = players[players['personId'] == longestCareerPlayer]['lastName'].values[0]

print('###3###')
print('A legidősebb játékos az utolsó mérkőzésén, amikor pályára lépett ', longestCareerPlayerFirstName,' ', longestCareerPlayerLastName, ' volt, összesen ', longestCareer, ' napig tartott karrierje.')

##### 4. Melyik csapatnak volt a legtöbb nemzetiségű játékosa egy szezonban?

teamPlayerList = playerStatistics[['firstName', 'lastName', 'personId', 'playerteamCity', 'playerteamName', 'season']].drop_duplicates().sort_values(by = ['season', 'playerteamCity', 'playerteamName'], ascending = True)
teamPlayerList = teamPlayerList.merge(players[['personId', 'country']], on = 'personId', how = 'left').dropna(subset = ['country'])
teamPlayerList = teamPlayerList.drop_duplicates(subset = ['playerteamCity', 'playerteamName', 'season', 'country'])

maxNationalities = teamPlayerList.groupby(['playerteamCity', 'playerteamName', 'season'])['country'].count().max()

maxNationalitiesTeam = teamPlayerList.groupby(['playerteamCity', 'playerteamName', 'season'])['country'].count().idxmax()

print('###4###')
print('A csapat: ', maxNationalitiesTeam, ', nemzetiségek száma: ', maxNationalities)

##### 5. Hogyan változott évről évre a legtöbbet átlagoló játékosok(pl. top25) pontszámainak átlaga?
topN = 25
averages = playerStatistics.groupby(['season', 'personId'])['points'].mean().reset_index()
averages = averages.groupby('season').apply(lambda x: x.nlargest(topN, 'points')).reset_index(drop = True)

averageTop = averages.groupby('season')['points'].mean()

seasons = averages['season'].unique()

x = np.array(averages['season'])
y = np.array(averages['points'])
z = np.array(averageTop)
v = np.array(seasons)

plt.plot(x, y, '.', color = 'green')
plt.plot(v, z, '-', color = 'red')

plt.xticks(rotation = 60)
plt.xlabel('Szezon')
plt.ylabel('Pontátlag')

plt.show()