# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 16:45:49 2016

@author: Administrator
"""
import urllib
import datetime
import json
import re

from workserver.util import SysUtil
from workserver.batch.BatchBase import BatchBase
from workserver.module.models import MatchInfoD
import spiderSports500WCurrent, SpiderSports, SpiderSports500W

class SpiderSportsCurrentBatch(BatchBase):
    def run(self):
        self.initialize()
        self.getMatch()
        self.getHafu()
        self.getTtg()
        self.release()
        
    def getMatch(self):
        urlM = "http://i.sporttery.cn/odds_calculator/get_odds?i_format=json&i_callback=getData&poolcode[]=hhad&poolcode[]=had&_=1460170422871"   
        try:
#            self.session.execute(text('truncate table tbl_matchinfod'))
            self.session.query(MatchInfoD).delete()
            self.session.flush()
            content = urllib.request.urlopen(urlM,timeout = 10).read()
            message = content.decode('gbk')
            message = message.replace('getData(','')
            message = message.replace(');','')
            decode = json.loads(message)
            matchInfos=decode['data']
            for match in matchInfos:
                wrate = drate = lrate = wrateS = drateS = lrateS = 0.0
                fixScore = '0'
                if matchInfos[match]['status'] != 'Selling':
                    continue
                matchid = matchInfos[match]['date'].replace('-','') + matchInfos[match]['num']
                singleFlag = '0'
                if matchInfos[match].get('had') is not None:
                    wrate = float(matchInfos[match]['had']['h'])
                    drate = float(matchInfos[match]['had']['d'])
                    lrate = float(matchInfos[match]['had']['a'])
                    singleFlag = matchInfos[match]['had']['single']
                minrate = min(wrate,drate,lrate)
                if matchInfos[match].get('hhad') is not None:
                    fixScore = matchInfos[match]['hhad']['fixedodds']
                    wrateS = float(matchInfos[match]['hhad']['h'])
                    drateS = float(matchInfos[match]['hhad']['d'])
                    lrateS = float(matchInfos[match]['hhad']['a'])
                minrateS = min(wrateS,drateS,lrateS)
                orderP=re.compile('(\d+)');
                rankMsg = orderP.findall(matchInfos[match]['h_order'])
                zhuRank = int(rankMsg[0]) if len(rankMsg) > 0 else 7
                rankMsg = orderP.findall(matchInfos[match]['a_order'])
                keRank = int(rankMsg[0]) if len(rankMsg) > 0 else 7
                
                mi = MatchInfoD(matchid = matchid,
                                match = matchInfos[match]['num'],
                                date = datetime.datetime.strptime(matchInfos[match]['date'], '%Y-%m-%d').date(),
                                matchTime = datetime.datetime.strptime(matchInfos[match]['time'], '%H:%M:%S').time(),
                                matchtype = matchInfos[match]['l_cn'],
                                matchtypename = matchInfos[match]['l_cn_abbr'],
                                matchzhu = matchInfos[match]['h_cn'],
                                matchke = matchInfos[match]['a_cn'],
                                status = matchInfos[match]['status'],
                                wrate = wrate,
                                drate = drate,
                                lrate = lrate,
                                minrate = minrate,
                                fixScore = fixScore,
                                wrateS = wrateS,
                                drateS = drateS,
                                lrateS = lrateS,
                                minrateS = minrateS,
                                zhuRank = zhuRank,
                                keRank = keRank,
                                rankDValue = zhuRank - keRank,
                                singleFlag = singleFlag)
                self.session.add(mi)
            self.session.commit()
            
            return True
        except Exception as ex:
            SysUtil.exceptionPrint(self.logger, ex)
            return False        
    
    def getHafu(self):
        urlM = "http://i.sporttery.cn/odds_calculator/get_odds?i_format=json&i_callback=getData&poolcode[]=hafu&_=1486372321610"   
        try:
            content = urllib.request.urlopen(urlM,timeout = 10).read()
            message = content.decode('gbk')
            message = message.replace('getData(','')
            message = message.replace(');','')
            decode = json.loads(message)
            matchInfos=decode['data']
            for match in matchInfos:
                if matchInfos[match]['status'] != 'Selling':
                    continue
                matchid = matchInfos[match]['date'].replace('-','') + matchInfos[match]['num']
                m = self.session.query(MatchInfoD).filter(MatchInfoD.matchid == matchid).first()
                if m is not None:
                    m.ww = float(matchInfos[match]['hafu']['hh'])
                    m.wd = float(matchInfos[match]['hafu']['ad'])
                    m.wl = float(matchInfos[match]['hafu']['ha'])
                    m.dw = float(matchInfos[match]['hafu']['dh'])
                    m.dd = float(matchInfos[match]['hafu']['dd'])
                    m.dl = float(matchInfos[match]['hafu']['da'])
                    m.lw = float(matchInfos[match]['hafu']['ah'])
                    m.ld = float(matchInfos[match]['hafu']['ad'])
                    m.ll = float(matchInfos[match]['hafu']['aa'])
            self.session.commit()
            
            return True
        except Exception as ex:
            SysUtil.exceptionPrint(self.logger, ex)
            return False 
        
    def getTtg(self):
        urlM = "http://i.sporttery.cn/odds_calculator/get_odds?i_format=json&i_callback=getData&poolcode[]=ttg&_=1486376411945"   
        try:
            content = urllib.request.urlopen(urlM,timeout = 10).read()
            message = content.decode('gbk')
            message = message.replace('getData(','')
            message = message.replace(');','')
            decode = json.loads(message)
            matchInfos=decode['data']
            for match in matchInfos:
                if matchInfos[match]['status'] != 'Selling':
                    continue
                matchid = matchInfos[match]['date'].replace('-','') + matchInfos[match]['num']
                m = self.session.query(MatchInfoD).filter(MatchInfoD.matchid == matchid).first()
                if m is not None:
                    m.s0 = float(matchInfos[match]['ttg']['s0'])
                    m.s1 = float(matchInfos[match]['ttg']['s1'])
                    m.s2 = float(matchInfos[match]['ttg']['s2'])
                    m.s3 = float(matchInfos[match]['ttg']['s3'])
                    m.s4 = float(matchInfos[match]['ttg']['s4'])
                    m.s5 = float(matchInfos[match]['ttg']['s5'])
                    m.s6 = float(matchInfos[match]['ttg']['s6'])
                    m.s7 = float(matchInfos[match]['ttg']['s7'])
            self.session.commit()
            
            return True
        except Exception as ex:
            SysUtil.exceptionPrint(self.logger, ex)
            return False
        
if __name__ == '__main__':  
    SpiderSportsCurrentBatch().run()
    spiderSports500WCurrent.SpiderSports500WCurrentBatch().run()
    SpiderSports.SpiderSportsBatch().run()
    SpiderSports500W.SpiderSports500WBatch().run()