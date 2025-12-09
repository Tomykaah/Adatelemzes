import numpy as np
import pandas as pd
from datetime import datetime as dt
import ownfunctions as of

games             = pd.read_csv('Games.csv', low_memory = False)
players           = pd.read_csv('Players.csv', low_memory = False)
playerStatistics  = pd.read_csv('PlayerStatistics.csv', low_memory = False)
teamStatistics    = pd.read_csv('TeamStatistics.csv', low_memory = False)
teamHistories     = pd.read_csv('TeamHistories.csv', low_memory = False)

##### 1. Ki volt az a játékos, aki a legtöbb pontot dobta egy meccsen az NBA történelmében?
#mostPoints = playerStatistics['points'].max()
#mostPointsPlayer = playerStatistics[playerStatistics['points'] == mostPoints]
#mostPointsName = mostPointsPlayer['firstName'] + ' ' + mostPointsPlayer['lastName']
#print(mostPointsName)

##### 2. Melyik az a csapat, amelyik a legtöbb győzelmet érte el összesen?
#mostWinsTeam = teamStatistics.groupby('teamId')['win'].sum().idxmax()
#print('The team: ',teamHistories[teamHistories['teamId'] == mostWinsTeam][['teamCity', 'teamName']], ', max wins: ', teamStatistics.groupby('teamId')['win'].sum().max())

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
print('A legidősebb játékos az utolsó mérkőzésén, amikor pályára lépett ', longestCareerPlayerFirstName,' ', longestCareerPlayerLastName, ' volt, összesen ', longestCareer, ' napig.')
    