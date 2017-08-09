# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 16:45:49 2016

@author: Administrator
"""
from sqlalchemy.sql import func
import re
import time
import datetime

import workserver.settings as settings
from workserver.util import SysUtil
from workserver.util import PinnacleAPI
from workserver.batch.BatchBase import BatchBase
from workserver.module.models import PinnacleSports, PinnacleLeagues, PinnacleTimestamp, PinnacleFixtures,\
     PinnacleSettledFixtures, PinnacleSettledSpecialFixtures

TRANS_CODE = 'zh-CN'

class PinnacleSyncBatch(BatchBase):
    def run(self):
        self.initialize()
        
        self.GetSports()
#        self.GetLeagues()
#        self.GetFixtures()
#        self.GetSettledFixtures()
#        self.GetSettledSpecialFixtures()
        
        self.release()
    
    def GetSports(self):
        JSrsp = PinnacleAPI.GetSportsV2(self.logger)
        errorC = 0
        while not JSrsp:
            if errorC > settings.spyderErrorTimes:
                break
            time.sleep(settings.spyderDelayTime)
            JSrsp = PinnacleAPI.GetSportsV2(self.logger)
            errorC+=1
        if JSrsp:
            sports = JSrsp['sports']
            transStr = '|'.join([ s['name'] for s in sports])
            transRst = PinnacleAPI.GetTranslations(TRANS_CODE,transStr,self.logger)
            
            for s in sports:
                sp = self.session.query(PinnacleSports).\
                    filter(PinnacleSports.id == s['id']).\
                    filter(PinnacleSports.name == s['name']).first()
                if sp:
                    sp.hasOfferings = s['hasOfferings']
                    sp.leagueSpecialsCount = s['leagueSpecialsCount']
                    sp.eventSpecialsCount = s['eventSpecialsCount']
                    sp.eventCount = s['eventCount']
                    sp.modifyTime = datetime.datetime.now()
                else:
                    spi = PinnacleSports(
                        id = s['id'],
                        name = s['name'],
                        cnname = PinnacleAPI.GetTransResult(s['name'],TRANS_CODE,transRst),
                        hasOfferings = s['hasOfferings'],
                        leagueSpecialsCount = s['leagueSpecialsCount'],
                        eventSpecialsCount = s['eventSpecialsCount'],
                        eventCount = s['eventCount'])
                    self.session.add(spi)
            self.session.commit()
            
    def GetLeagues(self):
        for s in self.session.query(PinnacleSports).all():
            JSrsp = PinnacleAPI.GetLeaguesV2(s.id, self.logger)
            errorC = 0
            while not JSrsp:
                if errorC > settings.spyderErrorTimes:
                    break
                time.sleep(settings.spyderDelayTime)
                JSrsp = PinnacleAPI.GetLeaguesV2(s.id, self.logger)
                errorC+=1
            if JSrsp:
                leagues = JSrsp['leagues']
                transStr = '|'.join([ l['name'] for l in leagues])
                transRst = PinnacleAPI.GetTranslations(TRANS_CODE,transStr,self.logger)
                for l in leagues:
                    lg = self.session.query(PinnacleLeagues).\
                        filter(PinnacleLeagues.id == l['id']).\
                        filter(PinnacleLeagues.name == l['name']).first()
                    if lg:
                        lg.hasOfferings = l['hasOfferings']
                        lg.allowRoundRobins = l['allowRoundRobins']
                        lg.leagueSpecialsCount = l['leagueSpecialsCount']
                        lg.eventSpecialsCount = l['eventSpecialsCount']
                        lg.eventCount = l['eventCount']
                        lg.modifyTime = datetime.datetime.now()
                    else:
                        lgi = PinnacleLeagues(
                            id = l['id'],
                            sportId = s.id,
                            name = l['name'],
                            cnname = PinnacleAPI.GetTransResult(l['name'],TRANS_CODE,transRst),
                            homeTeamType = l['homeTeamType'], 
                            hasOfferings = l['hasOfferings'],
                            allowRoundRobins = l['allowRoundRobins'],
                            leagueSpecialsCount = l['leagueSpecialsCount'],
                            eventSpecialsCount = l['eventSpecialsCount'],
                            eventCount = l['eventCount'])
                        self.session.add(lgi)
                self.session.commit()
    
    def GetFixtures(self):
        for s in self.session.query(PinnacleSports).\
                    filter(PinnacleSports.hasOfferings == True).all():
            ts = self.session.query(PinnacleTimestamp).\
                    filter(PinnacleTimestamp.tstype == 'Fixtures').\
                    filter(PinnacleTimestamp.sportId == s.id).first()
            if ts:
                JSrsp = PinnacleAPI.GetFixtures(s.id, since=ts.value1,logger=self.logger)
            else:
                JSrsp = PinnacleAPI.GetFixtures(s.id, logger=self.logger)
                
            errorC = 0
            while not JSrsp:
                if errorC > settings.spyderErrorTimes:
                    break
                time.sleep(settings.spyderDelayTime)
                if ts:
                    JSrsp = PinnacleAPI.GetFixtures(s.id, since=ts.value1,logger=self.logger)
                else:
                    JSrsp = PinnacleAPI.GetFixtures(s.id, logger=self.logger)
                errorC+=1
            
            if JSrsp:
                if ts:
                    ts.value1 = JSrsp['last']
                    ts.modifyTime = datetime.datetime.now()
                else:
                    tsi = PinnacleTimestamp(
                            tstype = 'Fixtures',
                            sportId = s.id,  
                            value1 = JSrsp['last'])
                    self.session.add(tsi)
                    
                for l in JSrsp['league']:
                    print(l['id'])
                    transHomeStr = '|'.join([ e['home'] for e in l['events']])
                    transHomeRst = PinnacleAPI.GetTranslations(TRANS_CODE,transHomeStr,self.logger)
                    transAwayStr = '|'.join([ e['away'] for e in l['events']])
                    transAwayRst = PinnacleAPI.GetTranslations(TRANS_CODE,transAwayStr,self.logger)
                    for e in l['events']:
                        fx = self.session.query(PinnacleFixtures).\
                            filter(PinnacleFixtures.id == e['id']).first()
                        if fx:
                            fx.starts = datetime.datetime.strptime(e['starts'],'%Y-%m-%dT%H:%M:%SZ')
                            fx.home = e['home']
                            fx.cnhome = PinnacleAPI.GetTransResult(e['home'],TRANS_CODE,transHomeRst)
                            fx.away = e['away']
                            fx.cnaway = PinnacleAPI.GetTransResult(e['away'],TRANS_CODE,transAwayRst)
                            fx.rotNum = e['rotNum']
                            fx.liveStatus = e['liveStatus']
                            fx.status = e['status']
                            fx.parlayRestriction = e['parlayRestriction']
                            fx.modifyTime = datetime.datetime.now()
                            if 'homePitcher' in e.keys():
                                fx.homePitcher = e['homePitcher']
                                fx.awayPitcher = e['awayPitcher']
                        else:
                            fxi = PinnacleFixtures(
                                id = e['id'],
                                sportId = s.id,
                                leagueId = l['id'],
                                starts = datetime.datetime.strptime(e['starts'],'%Y-%m-%dT%H:%M:%SZ'),
                                home = e['home'],
                                cnhome = PinnacleAPI.GetTransResult(e['home'],TRANS_CODE,transHomeRst),
                                away = e['away'],
                                cnaway = PinnacleAPI.GetTransResult(e['away'],TRANS_CODE,transAwayRst),
                                rotNum = e['rotNum'],
                                liveStatus = e['liveStatus'],
                                status = e['status'],
                                parlayRestriction = e['parlayRestriction'],
                                homePitcher = e['homePitcher'] if 'homePitcher' in e.keys() else None,
                                awayPitcher = e['awayPitcher'] if 'awayPitcher' in e.keys() else None
                            )
                            self.session.add(fxi)
                    self.session.commit()
        self.session.commit()
        
    def GetSettledFixtures(self):
        for s in self.session.query(PinnacleSports).\
                    filter(PinnacleSports.hasOfferings == True).all():
            ts = self.session.query(PinnacleTimestamp).\
                    filter(PinnacleTimestamp.tstype == 'SettledFixtures').\
                    filter(PinnacleTimestamp.sportId == s.id).first()
            if ts:
                JSrsp = PinnacleAPI.GetSettledFixtures(s.id, since=ts.value1,logger=self.logger)
            else:
                JSrsp = PinnacleAPI.GetSettledFixtures(s.id, logger=self.logger)
                
            errorC = 0
            while not JSrsp:
                if errorC > settings.spyderErrorTimes:
                    break
                time.sleep(settings.spyderDelayTime)
                if ts:
                    JSrsp = PinnacleAPI.GetSettledFixtures(s.id, since=ts.value1,logger=self.logger)
                else:
                    JSrsp = PinnacleAPI.GetSettledFixtures(s.id, logger=self.logger)
                errorC+=1
            
            if JSrsp:
                if ts:
                    ts.value1 = JSrsp['last']
                    ts.modifyTime = datetime.datetime.now()
                else:
                    tsi = PinnacleTimestamp(
                            tstype = 'SettledFixtures',
                            sportId = s.id,  
                            value1 = JSrsp['last'])
                    self.session.add(tsi)
                    
                for l in JSrsp['leagues']:
                    print(l['id'])
                    for e in l['events']:
                        for p in e['periods']:
                            sfx = self.session.query(PinnacleSettledFixtures).\
                                filter(PinnacleSettledFixtures.settlementId == p['settlementId']).first()
                            
                            m = re.match(r'\d+-\d+-\d+T\d+:\d+:\d+.\d+Z', p['settledAt'])
                            if m:
                                formatStr = '%Y-%m-%dT%H:%M:%S.%fZ'
                            else:
                                formatStr = '%Y-%m-%dT%H:%M:%SZ'
                                
                            if sfx:
                                sfx.number = p['number']
                                sfx.settledAt = datetime.datetime.strptime(p['settledAt'], formatStr) if p['settledAt'] else None
                                sfx.status = p['status']
                                sfx.team1Score = p['team1Score']
                                sfx.team2Score = p['team2Score']
                                sfx.modifyTime = datetime.datetime.now()
                            else:
                                sfxi = PinnacleSettledFixtures(
                                    settlementId = p['settlementId'],
                                    sportId = s.id,
                                    leagueId = l['id'],
                                    eventId = e['id'],
                                    number = p['number'],
                                    settledAt = datetime.datetime.strptime(p['settledAt'], formatStr) if p['settledAt'] else None,
                                    status = p['status'],
                                    team1Score = p['team1Score'],
                                    team2Score = p['team2Score'])
                                self.session.add(sfxi)
                    self.session.commit()
        self.session.commit()
        
    def GetSettledSpecialFixtures(self):
        for s in self.session.query(PinnacleSports).\
                    filter(PinnacleSports.hasOfferings == True).all():
            ts = self.session.query(PinnacleTimestamp).\
                    filter(PinnacleTimestamp.tstype == 'SettledSpecialFixtures').\
                    filter(PinnacleTimestamp.sportId == s.id).first()
            if ts:
                JSrsp = PinnacleAPI.GetSettledSpecialFixtures(s.id, since=ts.value1,logger=self.logger)
            else:
                JSrsp = PinnacleAPI.GetSettledSpecialFixtures(s.id, logger=self.logger)
            
            errorC = 0
            while not JSrsp:
                if errorC > settings.spyderErrorTimes:
                    break
                time.sleep(settings.spyderDelayTime)
                if ts:
                    JSrsp = PinnacleAPI.GetSettledSpecialFixtures(s.id, since=ts.value1,logger=self.logger)
                else:
                    JSrsp = PinnacleAPI.GetSettledSpecialFixtures(s.id, logger=self.logger)
                errorC+=1
                
            if JSrsp:
                if ts:
                    ts.value1 = JSrsp['last']
                    ts.modifyTime = datetime.datetime.now()
                else:
                    tsi = PinnacleTimestamp(
                            tstype = 'SettledSpecialFixtures',
                            sportId = s.id,  
                            value1 = JSrsp['last'])
                    self.session.add(tsi)
                    
                for l in JSrsp['leagues']:
                    print(l['id'])
                    for sp in l['specials']:
                        ssfx = self.session.query(PinnacleSettledSpecialFixtures).\
                            filter(PinnacleSettledSpecialFixtures.settlementId == sp['settlementId']).first()
                        
                        m = re.match(r'\d+-\d+-\d+T\d+:\d+:\d+.\d+Z', sp['settledAt'])
                        if m:
                            formatStr = '%Y-%m-%dT%H:%M:%S.%fZ'
                        else:
                            formatStr = '%Y-%m-%dT%H:%M:%SZ'
                            
                        if ssfx:
                            ssfx.settledAt = datetime.datetime.strptime(sp['settledAt'], formatStr) if sp['settledAt'] else None
                            ssfx.modifyTime = datetime.datetime.now()
                        else:
                            ssfxi = PinnacleSettledSpecialFixtures(
                                settlementId = sp['settlementId'],
                                SpecialId = sp['id'],
                                sportId = s.id,
                                leagueId = l['id'],
                                settledAt = datetime.datetime.strptime(sp['settledAt'], formatStr) if sp['settledAt'] else None)
                            self.session.add(ssfxi)
                    self.session.commit()
        self.session.commit()
        
if __name__ == '__main__':  
    PinnacleSyncBatch().run()