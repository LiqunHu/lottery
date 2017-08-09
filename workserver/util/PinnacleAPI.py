# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 15:17:46 2016

@author: Administrator
"""
import base64
import urllib
import http
import json

from . import SysUtil

APIHOST = 'api.pinnacle.com'
GLB_TIMEOUT = 10
#username = 'LH874811'
#password = '!55286668hlq'

username = 'JL946281'
password = 'DJ851217@'

def authorization(usr, pwd):
    return 'Basic ' + base64.b64encode((usr + ':' + pwd).encode(encoding="utf-8")).decode()
    
def GetSportsV1(logger = None):
    try:
        headers = {'Authorization': authorization(username, password)}       
        host = APIHOST
        url = '/v1/sports'
        conn = http.client.HTTPSConnection(host, timeout=GLB_TIMEOUT)
        conn.request('GET', url, '', headers)
        response = conn.getresponse()
        print(response.status, response.reason)
        print(response.read().decode())
        conn.close()
    except Exception as ex:
        SysUtil.exceptionPrint(logger, ex)
        return None

def GetSportsV2(logger = None):
    try:
        headers = {'Authorization': authorization(username, password)}
    #    params = {'username':'xxxx'}        
    #    data = urllib.urlencode(params)        
        host = APIHOST
        url = '/v2/sports'
        conn = http.client.HTTPSConnection(host, timeout=GLB_TIMEOUT)
        conn.request('GET', url, '', headers)
        response = conn.getresponse()
        msg = response.read()
        rspjson = None
        if msg:
            rspjson = json.loads(msg.decode())
        conn.close()
        return rspjson
    except Exception as ex:
        SysUtil.exceptionPrint(logger, ex)
        return None

def GetLeaguesV1(sportid ,logger = None):
    try:
        headers = {'Authorization': authorization(username, password)} 
        params = {'SportID': sportid}        
        data = urllib.parse.urlencode(params)        
        host = APIHOST
        url = '/v1/leagues?'
        conn = http.client.HTTPSConnection(host, timeout=GLB_TIMEOUT)
        conn.request('GET', url + data, '', headers)
        response = conn.getresponse()
        print(response.status, response.reason)
        print(response.read().decode())
        conn.close()
    except Exception as ex:
        SysUtil.exceptionPrint(logger, ex)
        return None
        
def GetLeaguesV2(sportId ,logger = None):
    try:
        headers = {'Authorization': authorization(username, password)} 
        params = {'SportID': sportId}        
        data = urllib.parse.urlencode(params)        
        host = APIHOST
        url = '/v2/leagues?'
        conn = http.client.HTTPSConnection(host, timeout=GLB_TIMEOUT)
        conn.request('GET', url + data, '', headers)
        response = conn.getresponse()
        msg = response.read()
        rspjson = None
        if msg:
            rspjson = json.loads(msg.decode())
        conn.close()
        return rspjson
    except Exception as ex:
        SysUtil.exceptionPrint(logger, ex)
        return None
        
def GetFixtures(sportId, leagueIds=[], since=None, islive=None, logger=None):
    try:
        headers = {'Authorization': authorization(username, password)}
        params = {}
        if sportId:
            params['sportId'] = sportId
        if leagueIds:
            params['leagueIds'] = ','.join(leagueIds)
        if since:
            params['since'] = since
        if islive:
            params['islive'] = islive
        data = urllib.parse.urlencode(params)        
        host = APIHOST
        url = '/v1/fixtures?'
        conn = http.client.HTTPSConnection(host, timeout=GLB_TIMEOUT)
        conn.request('GET', url + data, '', headers)
        response = conn.getresponse()
        msg = response.read()
        rspjson = None
        if msg:
            rspjson = json.loads(msg.decode())
        conn.close()
        return rspjson
    except Exception as ex:
        SysUtil.exceptionPrint(logger, ex)
        return None
    
def GetSettledFixtures(sportId, leagueIds=[], since=None, logger=None):
    try:
        headers = {'Authorization': authorization(username, password)}
        params = {}
        if sportId:
            params['sportId'] = sportId
        if leagueIds:
            params['leagueIds'] = ','.join(leagueIds)
        if since:
            params['since'] = since
        data = urllib.parse.urlencode(params)        
        host = APIHOST
        url = '/v1/fixtures/settled?'
        conn = http.client.HTTPSConnection(host, timeout=GLB_TIMEOUT)
        conn.request('GET', url + data, '', headers)
        response = conn.getresponse()
        msg = response.read()
        rspjson = None
        if msg:
            rspjson = json.loads(msg.decode())
        conn.close()
        return rspjson
    except Exception as ex:
        SysUtil.exceptionPrint(logger, ex)
        return None
        
def GetSpecialFixtures(sportId, leagueIds=[], category=None, eventId=None, specialId=None, since=None, logger=None):
    try:
        headers = {'Authorization': authorization(username, password)}
        params = {}
        if sportId:
            params['sportId'] = sportId
        if leagueIds:
            params['leagueIds'] = ','.join(leagueIds)
        if category:
            params['category'] = category
        if eventId:
            params['eventId'] = eventId
        if specialId:
            params['specialId'] = specialId
        if since:
            params['since'] = since
        data = urllib.parse.urlencode(params)        
        host = APIHOST
        url = '/v1/fixtures/special?'
        conn = http.client.HTTPSConnection(host, timeout=GLB_TIMEOUT)
        conn.request('GET', url + data, '', headers)
        response = conn.getresponse()
        msg = response.read()
        rspjson = None
        if msg:
            rspjson = json.loads(msg.decode())
        conn.close()
        return rspjson
    except Exception as ex:
        SysUtil.exceptionPrint(logger, ex)
        return None
        
def GetSettledSpecialFixtures(sportId, leagueIds=[], since=None, logger=None):
    try:
        headers = {'Authorization': authorization(username, password)}
        params = {}
        if sportId:
            params['sportId'] = sportId
        if leagueIds:
            params['leagueIds'] = ','.join(leagueIds)
        if since:
            params['since'] = since
        data = urllib.parse.urlencode(params)        
        host = APIHOST
        url = '/v1/fixtures/special/settled?'
        conn = http.client.HTTPSConnection(host, timeout=GLB_TIMEOUT)
        conn.request('GET', url + data, '', headers)
        response = conn.getresponse()
        msg = response.read()
        rspjson = None
        if msg:
            rspjson = json.loads(msg.decode())
        conn.close()
        return rspjson
    except Exception as ex:
        SysUtil.exceptionPrint(logger, ex)
        return None
        
def GetTeaserGroups(oddsFormat, logger=None):
    try:
        headers = {'Authorization': authorization(username, password)}
        params = {'oddsFormat': oddsFormat}
        data = urllib.parse.urlencode(params)        
        host = APIHOST
        url = '/v1/teaser/groups?'
        conn = http.client.HTTPSConnection(host, timeout=GLB_TIMEOUT)
        conn.request('GET', url + data, '', headers)
        response = conn.getresponse()
        msg = response.read()
        rspjson = None
        if msg:
            rspjson = json.loads(msg.decode())
        conn.close()
        return rspjson
    except Exception as ex:
        SysUtil.exceptionPrint(logger, ex)
        return None
        
def GetOdds(sportId, leagueIds=[], since=None, islive=None, oddsFormat=None, logger=None):
    try:
        headers = {'Authorization': authorization(username, password)}
        params = {}
        if sportId:
            params['sportId'] = sportId
        if leagueIds:
            params['leagueIds'] = ','.join(leagueIds)
        if since:
            params['since'] = since
        if islive:
            params['islive'] = islive
        if oddsFormat:
            params['oddsFormat'] = oddsFormat
        data = urllib.parse.urlencode(params)        
        host = APIHOST
        url = '/v1/odds?'
        conn = http.client.HTTPSConnection(host, timeout=GLB_TIMEOUT)
        conn.request('GET', url + data, '', headers)
        response = conn.getresponse()
        msg = response.read()
        rspjson = None
        if msg:
            rspjson = json.loads(msg.decode())
        conn.close()
        return rspjson
    except Exception as ex:
        SysUtil.exceptionPrint(logger, ex)
        return None
        
def GetOddsParlay(sportId, leagueIds=[], since=None, islive=None, oddsFormat=None, logger=None):
    try:
        headers = {'Authorization': authorization(username, password)}
        params = {}
        if sportId:
            params['sportId'] = sportId
        if leagueIds:
            params['leagueIds'] = ','.join(leagueIds)
        if since:
            params['since'] = since
        if islive:
            params['islive'] = islive
        if oddsFormat:
            params['oddsFormat'] = oddsFormat
        data = urllib.parse.urlencode(params)        
        host = APIHOST
        url = '/v1/odds/parlay?'
        conn = http.client.HTTPSConnection(host, timeout=GLB_TIMEOUT)
        conn.request('GET', url + data, '', headers)
        response = conn.getresponse()
        msg = response.read()
        rspjson = None
        if msg:
            rspjson = json.loads(msg.decode())
        conn.close()
        return rspjson
    except Exception as ex:
        SysUtil.exceptionPrint(logger, ex)
        return None
        
def GetTeaserOdds(teaserId, logger=None):
    try:
        headers = {'Authorization': authorization(username, password)}
        params = {'teaserId': teaserId}
        data = urllib.parse.urlencode(params)        
        host = APIHOST
        url = '/v1/odds/teaser?'
        conn = http.client.HTTPSConnection(host, timeout=GLB_TIMEOUT)
        conn.request('GET', url + data, '', headers)
        response = conn.getresponse()
        msg = response.read()
        rspjson = None
        if msg:
            rspjson = json.loads(msg.decode())
        conn.close()
        return rspjson
    except Exception as ex:
        SysUtil.exceptionPrint(logger, ex)
        return None

def GetSpecialOdds(sportId, leagueIds=[], since=None, specialId=None, oddsFormat=None, logger=None):
    try:
        headers = {'Authorization': authorization(username, password)}
        params = {}
        if sportId:
            params['sportId'] = sportId
        if leagueIds:
            params['leagueIds'] = ','.join(leagueIds)
        if since:
            params['since'] = since
        if specialId:
            params['specialId'] = specialId
        if oddsFormat:
            params['oddsFormat'] = oddsFormat
        data = urllib.parse.urlencode(params)        
        host = APIHOST
        url = '/v1/odds/special?'
        conn = http.client.HTTPSConnection(host, timeout=GLB_TIMEOUT)
        conn.request('GET', url + data, '', headers)
        response = conn.getresponse()
        msg = response.read()
        rspjson = None
        if msg:
            rspjson = json.loads(msg.decode())
        conn.close()
        return rspjson
    except Exception as ex:
        SysUtil.exceptionPrint(logger, ex)
        return None   

def GetCurrencies(logger=None):
    try:
        headers = {'Authorization': authorization(username, password)}       
        host = APIHOST
        url = '/v2/currencies'
        conn = http.client.HTTPSConnection(host, timeout=GLB_TIMEOUT)
        conn.request('GET', url, '', headers)
        response = conn.getresponse()
        msg = response.read()
        rspjson = None
        if msg:
            rspjson = json.loads(msg.decode())
        conn.close()
        return rspjson
    except Exception as ex:
        SysUtil.exceptionPrint(logger, ex)
        return None 
    
def GetClientBalance(logger=None):
    try:
        headers = {'Authorization': authorization(username, password)}
        host = APIHOST
        url = '/v1/client/balance'
        conn = http.client.HTTPSConnection(host, timeout=GLB_TIMEOUT)
        conn.request('GET', url, '', headers)
        response = conn.getresponse()
        msg = response.read()
        rspjson = None
        if msg:
            rspjson = json.loads(msg.decode())
        conn.close()
        return rspjson
    except Exception as ex:
        SysUtil.exceptionPrint(logger, ex)
        return None 
    
def GetLine(sportId, leagueId, eventId , periodNumber, betType, oddsFormat, team=None, side=None, handicap=None, logger=None):
    try:
        headers = {'Authorization': authorization(username, password)} 
        params = {}
        if sportId:
            params['sportId'] = sportId
        if leagueId:
            params['leagueId'] = leagueId
        if eventId:
            params['eventId'] = eventId
        if periodNumber:
            params['periodNumber'] = periodNumber
        if betType:
            params['betType'] = betType
        if oddsFormat:
            params['oddsFormat'] = oddsFormat
        if team:
            params['team'] = team
        if side:
            params['side'] = side
        if handicap:
            params['handicap'] = handicap
        data = urllib.parse.urlencode(params)
        host = APIHOST
        url = '/v1/line?'
        conn = http.client.HTTPSConnection(host, timeout=GLB_TIMEOUT)
        conn.request('GET', url + data, '', headers)
        response = conn.getresponse()
        msg = response.read()
        rspjson = None
        if msg:
            rspjson = json.loads(msg.decode())
        conn.close()
        return rspjson
    except Exception as ex:
        SysUtil.exceptionPrint(logger, ex)
        return None
    
def GetParlayLine(oddsFormat, legs, logger=None):
    try:
        headers = {'Authorization': authorization(username, password),
                   'Content-Type': 'application/json',
                   }
        params = {}
        if oddsFormat:
            params['oddsFormat'] = oddsFormat
        if legs:
            params['legs'] = legs
        host = APIHOST
        url = '/v1/line/parlay'
        conn = http.client.HTTPSConnection(host, timeout=GLB_TIMEOUT)
        conn.request('POST', url, json.dumps(params).encode(), headers)
        response = conn.getresponse()
        msg = response.read()
        rspjson = None
        if msg:
            rspjson = json.loads(msg.decode())
        conn.close()
        return rspjson
    except Exception as ex:
        SysUtil.exceptionPrint(logger, ex)
        return None
    
def GetTeaserLines(teaserId, oddsFormat, legs, logger=None):
    try:
        headers = {'Authorization': authorization(username, password),
                   'Content-Type': 'application/json',
                   }
        params = {}
        if teaserId:
            params['teaserId'] = teaserId
        if oddsFormat:
            params['oddsFormat'] = oddsFormat
        if legs:
            params['legs'] = legs
        host = APIHOST
        url = '/v1/line/teaser'
        conn = http.client.HTTPSConnection(host, timeout=GLB_TIMEOUT)
        conn.request('POST', url, json.dumps(params).encode(), headers)
        response = conn.getresponse()
        msg = response.read()
        rspjson = None
        if msg:
            rspjson = json.loads(msg.decode())
        conn.close()
        return rspjson
    except Exception as ex:
        SysUtil.exceptionPrint(logger, ex)
        return None

def GetSpecialLines(specialId, contestantId, oddsFormat, logger=None):
    try:
        headers = {'Authorization': authorization(username, password)}
        params = {}
        if specialId:
            params['specialId'] = specialId
        if contestantId:
            params['contestantId'] = contestantId
        if oddsFormat:
            params['oddsFormat'] = oddsFormat
        data = urllib.parse.urlencode(params)
        host = APIHOST
        url = '/v1/line/special?'
        conn = http.client.HTTPSConnection(host, timeout=GLB_TIMEOUT)
        conn.request('GET', url + data, '', headers)
        response = conn.getresponse()
        msg = response.read()
        rspjson = None
        if msg:
            rspjson = json.loads(msg.decode())
        conn.close()
        return rspjson
    except Exception as ex:
        SysUtil.exceptionPrint(logger, ex)
        return None  
    
def PlaceParlayBet(uniqueRequestId, acceptBetterLine, oddsFormat, riskAmount, roundRobinOptions, legs, logger=None):
    try:
        headers = {'Authorization': authorization(username, password),
                   'Content-Type': 'application/json',
                   }
        params = {}
        if uniqueRequestId:
            params['uniqueRequestId'] = uniqueRequestId
        if acceptBetterLine:
            params['acceptBetterLine'] = acceptBetterLine
        if oddsFormat:
            params['oddsFormat'] = oddsFormat
        if riskAmount:
            params['riskAmount'] = riskAmount
        if roundRobinOptions:
            params['roundRobinOptions'] = roundRobinOptions
        if legs:
            params['legs'] = legs
        host = APIHOST
        url = '/v1/bets/parlay'
        conn = http.client.HTTPSConnection(host, timeout=GLB_TIMEOUT)
        conn.request('POST', url, json.dumps(params).encode(), headers)
        response = conn.getresponse()
        msg = response.read()
        rspjson = None
        if msg:
            rspjson = json.loads(msg.decode())
        conn.close()
        return rspjson
    except Exception as ex:
        SysUtil.exceptionPrint(logger, ex)
        return None    
    
def PlaceTeaserBet(uniqueRequestId, teaserId, oddsFormat, winRiskStake, stake, legs, logger=None):
    try:
        headers = {'Authorization': authorization(username, password),
                   'Content-Type': 'application/json',
                   }
        params = {}
        if uniqueRequestId:
            params['uniqueRequestId'] = uniqueRequestId
        if teaserId:
            params['teaserId'] = teaserId
        if oddsFormat:
            params['oddsFormat'] = oddsFormat
        if winRiskStake:
            params['winRiskStake'] = winRiskStake
        if stake:
            params['stake'] = stake
        if legs:
            params['legs'] = legs
        host = APIHOST
        url = '/v1/bets/teaser'
        conn = http.client.HTTPSConnection(host, timeout=GLB_TIMEOUT)
        conn.request('POST', url, json.dumps(params).encode(), headers)
        response = conn.getresponse()
        msg = response.read()
        rspjson = None
        if msg:
            rspjson = json.loads(msg.decode())
        conn.close()
        return rspjson
    except Exception as ex:
        SysUtil.exceptionPrint(logger, ex)
        return None

def PlaceSpecialBet(bets, logger=None):
    try:
        headers = {'Authorization': authorization(username, password),
                   'Content-Type': 'application/json',
                   }
        params = {}
        if bets:
            params['bets'] = bets
        host = APIHOST
        url = '/v1/bets/special'
        conn = http.client.HTTPSConnection(host, timeout=GLB_TIMEOUT)
        conn.request('POST', url, json.dumps(params).encode(), headers)
        response = conn.getresponse()
        msg = response.read()
        rspjson = None
        if msg:
            rspjson = json.loads(msg.decode())
        conn.close()
        return rspjson
    except Exception as ex:
        SysUtil.exceptionPrint(logger, ex)
        return None
    
def GetBets(betlist=None, betids=None, fromDate=None, toDate=None, logger=None):
    try:
        headers = {'Authorization': authorization(username, password)}
        params = {}
        if betlist:
            params['betlist'] = betlist
        if betids:
            params['betids'] = betids
        if fromDate:
            params['fromDate'] = fromDate
        if toDate:
            params['toDate'] = toDate
        data = urllib.parse.urlencode(params)
        host = APIHOST
        url = '/v1/bets?'
        conn = http.client.HTTPSConnection(host, timeout=GLB_TIMEOUT)
        conn.request('GET', url + data, '', headers)
        response = conn.getresponse()
        msg = response.read()
        rspjson = None
        if msg:
            rspjson = json.loads(msg.decode())
        conn.close()
        return rspjson
    except Exception as ex:
        SysUtil.exceptionPrint(logger, ex)
        return None
    
def GetInrunning(logger=None):
    try:
        headers = {'Authorization': authorization(username, password)}       
        host = APIHOST
        url = '/v1/inrunning'
        conn = http.client.HTTPSConnection(host, timeout=GLB_TIMEOUT)
        conn.request('GET', url, '', headers)
        response = conn.getresponse()
        msg = response.read()
        rspjson = None
        if msg:
            rspjson = json.loads(msg.decode())
        conn.close()
        return rspjson
    except Exception as ex:
        SysUtil.exceptionPrint(logger, ex)
        return None 
    
def GetTranslations(cultureCodes, baseTexts, logger=None):
    try:
        headers = {'Authorization': authorization(username, password)}
        params = {}
        if cultureCodes:
            params['cultureCodes'] = cultureCodes
        if baseTexts:
            params['baseTexts'] = baseTexts
        data = urllib.parse.urlencode(params)
        host = APIHOST
        url = '/v1/translations?'
        conn = http.client.HTTPSConnection(host, timeout=GLB_TIMEOUT)
        conn.request('GET', url + data, '', headers)
        response = conn.getresponse()
        msg = response.read()
        rspjson = None
        if msg:
            rspjson = json.loads(msg.decode())
        conn.close()
        return rspjson
    except Exception as ex:
#        SysUtil.exceptionPrint(logger, ex)
        return None

def GetPeriods(sportId, logger=None):
    try:
        headers = {'Authorization': authorization(username, password)}
        params = {}
        if sportId:
            params['sportId'] = sportId
        data = urllib.parse.urlencode(params)
        host = APIHOST
        url = '/v1/periods?'
        conn = http.client.HTTPSConnection(host, timeout=GLB_TIMEOUT)
        conn.request('GET', url + data, '', headers)
        response = conn.getresponse()
        msg = response.read()
        rspjson = None
        if msg:
            rspjson = json.loads(msg.decode())
        conn.close()
        return rspjson
    except Exception as ex:
        SysUtil.exceptionPrint(logger, ex)
        return None

def GetCancellationReasons(logger=None):
    try:
        headers = {'Authorization': authorization(username, password)}
        host = APIHOST
        url = '/v1/cancellationreasons'
        conn = http.client.HTTPSConnection(host, timeout=GLB_TIMEOUT)
        conn.request('GET', url, '', headers)
        response = conn.getresponse()
        msg = response.read()
        rspjson = None
        if msg:
            rspjson = json.loads(msg.decode())
        conn.close()
        return rspjson
    except Exception as ex:
        SysUtil.exceptionPrint(logger, ex)
        return None
        
def GetTransResult(text, code, translations):
    if translations:
        for item in translations['translations']:
            if item['text'] == text:
                for trans in item['cultures']:
                    if trans['id'] == code:
                        return trans['text']
    return ''