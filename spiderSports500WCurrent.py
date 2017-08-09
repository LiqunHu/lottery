# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 16:45:49 2016

@author: Administrator
"""
import urllib
import datetime
import re
import random
from bs4 import BeautifulSoup

from workserver.util import GLBConfig
from workserver.util import SysUtil
from workserver.batch.BatchBase import BatchBase
from workserver.module.models import MatchInfoD, MatchInfo500D, Dealer, DealerMatch

class SpiderSports500WCurrentBatch(BatchBase):
    def run(self):
        self.initialize()
        self.session.query(MatchInfo500D).delete()
        self.session.flush()
        
        urlid500W = 'http://trade.500.com/jczq/?date='+SysUtil.getToday().isoformat()+'&playtype=both'
        content500W = urllib.request.urlopen(urlid500W,timeout = 10).read()
        message500W = content500W.decode('gbk')
        soup500W = BeautifulSoup(message500W, 'html.parser')
        tb500Wdate = soup500W.findAll('div','bet_date')
        for i in range(0,len(tb500Wdate)):
            dateInfo = self.getDate(tb500Wdate[i].contents[0])
            tb500Wtb = soup500W.findAll('table','bet_table')
            trs500W = tb500Wtb[i].findAll('tr')
            self.getMatchSync(trs500W,dateInfo,i)
        
        self.getDealerMatch()
        self.release()
            
    def getDealerMatch(self):
        dealers = self.session.query(Dealer).filter(Dealer.dealertype == GLBConfig.D_TYPE_C).all()
        
        for d in dealers:
            if len(self.session.query(DealerMatch).\
                filter(DealerMatch.dealerid == d.uid).\
                filter(DealerMatch.date == SysUtil.getTomorrow()).all()) > 0:
                continue
            
            if d.uid == 1:
                matches = self.session.query(MatchInfoD).\
                    filter(MatchInfoD.date == SysUtil.getTomorrow()).\
                    filter(MatchInfoD.minrate >= 2.0).\
                    filter(MatchInfoD.minrate <= 3.0).all()
            elif d.uid == 2:
                matches = self.session.query(MatchInfoD).\
                    filter(MatchInfoD.date == SysUtil.getTomorrow()).\
                    filter(MatchInfoD.minrate >= 1.0).\
                    filter(MatchInfoD.minrate <= 2.5).all()
            elif d.uid == 3:
                matches = self.session.query(MatchInfoD).\
                    filter(MatchInfoD.date == SysUtil.getTomorrow()).\
                    filter(MatchInfoD.minrate >= 1.5).\
                    filter(MatchInfoD.minrate <= 2.5).all()
        
            if len(matches) > 1:
                choice = random.sample(matches,2)
                rateAList = (choice[0].wrate,choice[0].drate,choice[0].lrate)
                minRateAIdex = SysUtil.getMinIndex(rateAList)
                      
                rateBList = (choice[1].wrate,choice[1].drate,choice[1].lrate)
                minRateBIdex = SysUtil.getMinIndex(rateBList)
    
                dm = DealerMatch(dealerid = d.uid,
                    date = SysUtil.getTomorrow(),
                    matchAID = choice[0].matchid,
                    matchAResult = SysUtil.getMatchResult(minRateAIdex),
                    matchBID = choice[1].matchid,
                    matchBResult = SysUtil.getMatchResult(minRateBIdex),
                    matchdesc = ''
                    )
                self.session.add(dm)
                self.session.commit()
        
                
    def getDate(self, dataStr):
        patternWeek=re.compile(u'[\u4e00-\u9fa5]{3}');
        patternDate=re.compile(u'\d{4}-\d{2}-\d{2}');
        weekday = ''
        text = patternWeek.findall(dataStr)[0]
        if text == u'星期一':
            weekday = u'周一'
        if text == u'星期二':
            weekday = u'周二'
        if text == u'星期三':
            weekday = u'周三'
        if text == u'星期四':
            weekday = u'周四'
        if text == u'星期五':
            weekday = u'周五'
        if text == u'星期六':
            weekday = u'周六'
        if text == u'星期日':
            weekday = u'周日'
        return [text,patternDate.findall(dataStr)[0],weekday]       
    
    def getMDate(self, date, TimeStr):
        patternDate=re.compile(u'\d{4}-\d{2}-\d{2}');
        timeD = patternDate.findall(TimeStr)
        patternTime=re.compile(u'\d{2}:\d{2}:\d{2}');
        timeT = patternTime.findall(TimeStr)
        if len(timeT)>0:
            d = date
            if timeT[0] > '23:40:00':
                delta = datetime.timedelta(days=1) 
                d += delta 
                return d
        if not timeT:
            return datetime.datetime.strptime(TimeStr,"%Y-%m-%d").date()
        else:
            return datetime.datetime.strptime(timeD[0],"%Y-%m-%d").date()
        
    def getWDLRate(self, tdInfo):
        divS = tdInfo.findAll('div')
        spans = divS[0].findAll('span')
        rate=(0.00,0.00,0.00)
        rateF=(0.00,0.00,0.00)
        if len(spans) == 3:
            rate=(float(spans[0]['data-sp']),float(spans[1]['data-sp']),float(spans[2]['data-sp']))
            
        spansF = divS[1].findAll('span')
        if len(spansF) == 3:
            rateF = (float(spansF[0]['data-sp']),float(spansF[1]['data-sp']),float(spansF[2]['data-sp']))
        return [rate,rateF]
        
    def getNum(self, NumStr):
        if NumStr is None:
            return '0'
        patternNum=re.compile('\[(\d+)\]');
        NumT = patternNum.findall(NumStr)
        if not NumT:
            return 0
        else:
            return int(NumT[0])
    
    def getScore(self, ScoreStr):
        if ScoreStr is None:
            return ['','']
        patternScore=re.compile('(\d+):(\d+)');
        ScoreT = patternScore.findall(ScoreStr)
        if not ScoreT:
            return ['','']
        else:
            return [int(ScoreT[0][0]),int(ScoreT[0][1])]

    def getMResult(self, ScoreR):
        mResult = ''
        if ScoreR[0] > ScoreR[1]:
            mResult = 'W'
        elif ScoreR[0] == ScoreR[1]:
            mResult = 'D'
        else:
            mResult = 'L'
        return mResult
    
    def getMResultF(self, ScoreR,fixScore):
        fixResult = ''
        try:
            if ScoreR[0] + fixScore > ScoreR[1]:
                fixResult = 'W'
            elif ScoreR[0] + fixScore == ScoreR[1]:
                fixResult = 'D'
            else:
                fixResult = 'L'
        except Exception as ex:
            pass
        return fixResult

    def getMinRate(self, my_list):
        minNum = my_list[0]
        if minNum > 40:
            return 0.00
        for i in my_list:
            if i < minNum:
                minNum = i
        return minNum
        
    def getMatchSync(self,trs500W,dateInfo,num):
        try:
            for line in trs500W:
                tds = line.findAll('td')
                
                mid = line['mid']
                match = dateInfo[2]+tds[0].a.contents[0]
                date = datetime.datetime.strptime(dateInfo[1],"%Y-%m-%d").date()
                mdate = self.getMDate(date,line['pendtime'])
                matchid = mdate.isoformat().replace(u'-','')+match
                mtime = datetime.datetime.strptime(line['pendtime'],"%Y-%m-%d %H:%M:%S")
                matchtype = line['lg']
                matchzhu = tds[3].a['title']
                zhuRank = self.getNum(tds[3].span.text)
                
                matchke = tds[5].a['title']
                keRank = self.getNum(tds[5].span.text)
                rankDValue = zhuRank - keRank
                if zhuRank == 0:
                    rankDValue = 4
                rates = self.getWDLRate(tds[7]) 
                wrate,drate,lrate=rates[0]        
                wrateS,drateS,lrateS=rates[1]
                minrate = self.getMinRate( (rates[0][0], rates[0][1], rates[0][2]) )
                minrateS  = self.getMinRate( (rates[1][0], rates[1][1], rates[1][2]) )
                               
                fixScore = int(tds[6].findAll('p')[1].text)
                singleFlag = '0'
                if tds[0].has_attr('class'):
                    singleFlag = '1'
                
                zhuScore = None
                keScore = None
                mResult = ''
                fixResult = ''
                status = '0'
                if len(tds[4].text) > 0:
                    scores = self.getScore(tds[4].text)
                    zhuScore = scores[0]
                    if not zhuScore:
                        zhuScore = None
                    keScore = scores[1]
                    if not keScore:
                        keScore = None
                    mResult = self.getMResult(scores)
                    fixResult = self.getMResultF(scores,fixScore)
                    status = '1'
                
                mi = MatchInfo500D(matchid = matchid,
                                  mid = mid,
                                  match = match,
                                  date = date,
                                  mdate = mdate,
                                  mtime = mtime,
                                  matchtype = matchtype,
                                  matchzhu = matchzhu,
                                  zhuRank = zhuRank,
                                  matchke = matchke,
                                  keRank = keRank,
                                  rankDValue = rankDValue,
                                  zhuScore = zhuScore,
                                  keScore = keScore,
                                  mResult = mResult,
                                  status = status,
                                  wrate = wrate,
                                  drate = drate,
                                  lrate = lrate,
                                  minrate = minrate,
                                  fixScore = fixScore,
                                  fixResult = fixResult,
                                  wrateS = wrateS,
                                  drateS = drateS,
                                  lrateS = lrateS,
                                  minrateS = minrateS,
                                  singleFlag = singleFlag)
                self.session.add(mi)
                
#                m = self.session.query(MatchInfoD).filter(MatchInfoD.matchid == mi.matchid).first()
#                if m is not None:
#                    m.matchTime = mi.mtime.time()
#                    m.zhuRank = mi.zhuRank
#                    m.keRank = mi.keRank
#                    m.rankDValue = mi.rankDValue
#                self.session.flush()
                
            self.session.commit()
            
            return True
        except Exception as ex:
            SysUtil.exceptionPrint(self.logger, ex)
            return False
    
if __name__ == '__main__':  
    SpiderSports500WCurrentBatch().run()