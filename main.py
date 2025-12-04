import numpy as np
import pandas as pd

games             = pd.read_csv('Games.csv', low_memory = False)
players           = pd.read_csv('Players.csv', low_memory = False)
playerStatistics  = pd.read_csv('PlayerStatistics.csv', low_memory = False)
teamStatistics    = pd.read_csv('TeamStatistics.csv', low_memory = False)
teamHistories     = pd.read_csv('TeamHistories.csv', low_memory = False)

##### 1. Ki volt az a játékos, aki a legtöbb pontot dobta egy meccsen az NBA történelmében?
mostPoints = playerStatistics['points'].max()
mostPointsPlayer = playerStatistics[playerStatistics['points'] == mostPoints]
mostPointsName = mostPointsPlayer['firstName'] + ' ' + mostPointsPlayer['lastName']
print(mostPointsName)

##### 2. Melyik az a csapat, amelyik a legtöbb győzelmet érte el összesen?
mostWinsTeam = teamStatistics.groupby('teamId')['win'].sum().idxmax()
print('The team: ',teamHistories[teamHistories['teamId'] == mostWinsTeam][['teamCity', 'teamName']], ', max wins: ', teamStatistics.groupby('teamId')['win'].sum().max())

##### 3. Ki az a játékos, aki a legidősebb volt, amikor utolsó mérkőzését játszotta?
oldestPlayer = players.groupby('birthdate').idxmax()
print(oldestPlayer['firstName'], oldestPlayer['lastName '])