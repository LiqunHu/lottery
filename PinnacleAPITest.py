# -*- coding: utf-8 -*-
"""
Created on Wed May 18 10:18:23 2016

@author: huliqun
@email: huliquns@126.com
"""

import logging
from workserver.util import LogUtil

from workserver.util import PinnacleAPI

if __name__ == '__main__':
    LogUtil.initLog()
    logger = logging.getLogger('serverLog')
#    print(PinnacleAPI.GetSportsV2(logger))
    
#    print(PinnacleAPI.GetLeaguesV2(1, logger))
#    print(PinnacleAPI.GetFixtures(15, logger=logger))
    print(PinnacleAPI.GetFixtures(29, logger=logger))
#    print(PinnacleAPI.GetSettledFixtures(15, logger=logger))
#    print(PinnacleAPI.GetSpecialFixtures(15, logger=logger))
#    print(PinnacleAPI.GetSettledSpecialFixtures(15, logger=logger))
#    print(PinnacleAPI.GetTeaserGroups('HONGKONG', logger=logger))
#    print(PinnacleAPI.GetOdds(15, logger=logger))
#    print(PinnacleAPI.GetOdds(29, leagueIds=['1769'], oddsFormat='HONGKONG', logger=logger))
#    print(PinnacleAPI.GetOddsParlay(15, logger=logger))
#    print(PinnacleAPI.GetTeaserOdds(1, logger=logger))
#    print(PinnacleAPI.GetSpecialOdds(29, logger=logger))
#    print(PinnacleAPI.GetCurrencies(logger=logger))
#    print(PinnacleAPI.GetClientBalance(logger=logger))
#    print(PinnacleAPI.GetLine(29,1728,308195882,0,'SPREAD','DECIMAL',logger=logger))
#    legs = [
#            {
#              'uniqueLegId': '9CED620A-0E78-4FA4-A314-BDB1FF34E25A',
#              'eventId': '383910968',
#              'periodNumber': '0',
#              'legBetType': 'SPREAD',
#              'team': 'TEAM1',
#              'handicap': 0.75
#            }   
#           ]
#    print(PinnacleAPI.GetParlayLine('Decimal', legs,logger=logger))
#    legs = [
#            {
#                'legId': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
#                'eventId': 480168370,
#                'betType': 'SPREAD',
#                'team': 'Team2',
#                'periodNumber': 0,
#                'handicap': 1
#            } 
#           ]
#    print(PinnacleAPI.GetTeaserLines(1, 'Decimal', legs,logger=logger))
#    print(PinnacleAPI.GetSpecialLines(598758142, 598758144, 'american', logger=logger))
#    legs = [
#            {
#                'uniqueLegId': '719B13BC-0237-45AB-B997-4AB8C9C810C5',
#                'lineId': 138029470,
#                'sportId': 29,
#                'eventId': 383910968,
#                'periodNumber':  0,
#                'legBetType': 'SPREAD',
#                'team': 'TEAM1'
#            } 
#           ]
#    print(PinnacleAPI.PlaceParlayBet('059AA152-DB79-4226-B003-42531EC7C006', 'TRUE', 'DECIMAL', 10, ['PARLAY'], legs, logger=logger))
#    legs = [
#            {
#                'legId': '24E999C0-9AA7-480E-F490-89B219C4D01A',
#                'betType': 'SPREAD',
#                'eventId': 480174385,
#                'lineId': 210663830,
#                'handicap': -4.5,
#                'team': 'Team1'
#            } 
#           ]
#    print(PinnacleAPI.PlaceTeaserBet('48175E97-02B7-4EA8-BCEF-9E557A80CE8F', 50, 'AMERICAN', 'RISK', 1, legs, logger=logger))
#    bets = [
#            {
#                'uniqueRequestId':    '3ca3e7a7-1111-4907-8b84-00f02e814b8d',
#                'acceptBetterLine':   'TRUE',
#                'oddsFormat':         'AMERICAN',
#                'winRiskStake':       'RISK',
#                'stake':              406.79,
#                'lineId':             33997608,
#                'specialId':          480692762,
#                'contestantId':       480692764,
#            } 
#           ]
#    print(PinnacleAPI.PlaceSpecialBet(bets, logger=logger))
#    print(PinnacleAPI.GetBets(betlist='settled', fromDate='2016-06-01', toDate='2016-07-01', logger=logger))
#    print(PinnacleAPI.GetInrunning(logger=logger))
#    print(PinnacleAPI.GetTranslations('zh-CN','Championship',logger=logger))
#    print(PinnacleAPI.GetPeriods(29, logger=logger))
#    print(PinnacleAPI.GetCancellationReasons(logger=logger))

