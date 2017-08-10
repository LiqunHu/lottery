# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 16:45:49 2016

@author: Administrator
"""
import urllib
import urllib.request
from bs4 import BeautifulSoup
from sqlalchemy.sql import func
import datetime
import random
import re
import time

from workserver.util import SysUtil
from workserver.batch.BatchBase import BatchBase
from workserver.module.models import MatchInfo

import SpiderSports500W

class SpiderSportsBatch(BatchBase):
    def run(self):
        self.initialize()
        end = datetime.date.today()
        maxDate = self.session.query(func.max(MatchInfo.date).label('max_date')).first()
        start = maxDate.max_date + datetime.timedelta(days=1)

        self.getMatresult(start, end)
        self.release()

    def getMinRate(self, my_list):
        minNum = my_list[0]
        if minNum > 40:
            return 0.00
        for i in my_list:
            if i < minNum:
                minNum = i
        return minNum

    def getWDLRate(self, urlWDL):
        try:
            contentWDL = urllib.request.urlopen(urlWDL,timeout = 10).read()
            messageWDL = contentWDL.decode('gbk').encode('utf8')
            soupWDL = BeautifulSoup(messageWDL, 'html.parser')
            tbWDL = soupWDL.findAll('table')
            trrWDL = tbWDL[2].findAll('tr')
            tddWDL = trrWDL[-1].findAll('td')
            tmpRate = re.search("[\d]+\.[\d]+",repr(tddWDL[1]))
            rateA = (99.99,99.99,99.99)
            if tmpRate is not None:
                rateA = (float(re.search("[\d]+\.[\d]+",repr(tddWDL[1])).group()),
                   float(re.search("[\d]+\.[\d]+",repr(tddWDL[2])).group()),
                   float(re.search("[\d]+\.[\d]+",repr(tddWDL[3])).group()))

            rateB = ('0',99.99,99.99,99.99)
            trrWDLS = tbWDL[1].findAll('tr')
            tddWDLS = trrWDLS[-1].findAll('td')
            if len(tddWDLS) >3:
                tmpRateS = re.search("[\d]+\.[\d]+",repr(tddWDLS[3]))
                if tddWDLS[1].text is None:
                    if tmpRateS is not None:
                        rateA = (float(re.search("[\d]+\.[\d]+",repr(tddWDLS[2])).group()),
                                 float(re.search("[\d]+\.[\d]+",repr(tddWDLS[3])).group()),
                                 float(re.search("[\d]+\.[\d]+",repr(tddWDLS[4])).group()))
                else:
                    if tmpRateS is not None:
                        rateB = (int(tddWDLS[1].text),
                                 float(re.search("[\d]+\.[\d]+",repr(tddWDLS[2])).group()),
                                 float(re.search("[\d]+\.[\d]+",repr(tddWDLS[3])).group()),
                                 float(re.search("[\d]+\.[\d]+",repr(tddWDLS[4])).group()))

            trrScore = tbWDL[3].findAll('tr')
            tddScore = trrScore[-1].findAll('td')
    #        print tddScore[1].text
            rateC = (99.99,99.99,99.99,99.99,99.99,99.99,99.99,99.99)
            tmpRateScore = re.search("[\d]+\.[\d]+",repr(tddScore[1].text))
            if tmpRateScore is not None:
                rateC = (float(tddScore[1].text),float(tddScore[2].text),float(tddScore[3].text),
                        float(tddScore[4].text),float(tddScore[5].text),float(tddScore[6].text),
                        float(tddScore[7].text),float(tddScore[8].text))

            trrHF = tbWDL[4].findAll('tr')
            tddHF = trrHF[-1].findAll('td')
            rateD = (99.99,99.99,99.99,99.99,99.99,99.99,99.99,99.99,99.99)
            tmpRateHF = re.search("[\d]+\.[\d]+",repr(tddHF[1].text))
            if tmpRateHF is not None:
                rateD = (float(tddHF[1].text),float(tddHF[2].text),float(tddHF[3].text),
                        float(tddHF[4].text),float(tddHF[5].text),float(tddHF[6].text),
                        float(tddHF[7].text),float(tddHF[8].text),float(tddHF[9].text))

            return (rateA,rateB,rateC,rateD)
        except Exception as ex:
            SysUtil.exceptionPrint(self.logger, ex)
            return None

    def getMatch(self, urlM):
        try:
            content = urllib.request.urlopen(urlM,timeout = 10).read()
            message = content.decode('gbk')
            soup = BeautifulSoup(message, 'html.parser')
            for tabb in soup.findAll('table')[1:2]:
                for trr in tabb.findAll('tr'):
                    tds = trr.findAll('td')
                    if len(tds) < 3:
                        continue
                    if tds[6].text == u'进行中' or tds[6].text == u'取消':
                        continue
                    if tds[7].a is None:
                        continue
                    matchid = tds[0].text.replace('-','')+tds[1].text
                    singleF = re.search(r'(single\.gif)',repr(tds[3]))
                    singleFlag = '0'
                    if singleF:
                        singleFlag = '1'
                    teams = tds[3].findAll('span')
                    scoreh = re.search(r'([\d+]):([\d+])',tds[4].span.text)
                    score = re.search(r'([\d+]):([\d+])',tds[5].span.text)
                    if int(score.groups()[0]) > int(score.groups()[1]):
                        mResult = 'W'
                    elif int(score.groups()[0]) == int(score.groups()[1]):
                        mResult = 'D'
                    else:
                        mResult = 'L'
                    rateurl = 'http://info.sporttery.cn/football/'+tds[7].a['href']
                    rates = self.getWDLRate(rateurl)
                    while not rates:
                        self.logger.info(urlM)
                        self.logger.info(rateurl)
                        rates = self.getWDLRate(rateurl)
                    fixResult = ' '
                    if int(score.groups()[0]) + rates[1][0] > int(score.groups()[1]):
                        fixResult = 'W'
                    elif int(score.groups()[0]) + rates[1][0] == int(score.groups()[1]):
                        fixResult = 'D'
                    else:
                        fixResult = 'L'

                    minrate = self.getMinRate( (rates[0][0],rates[0][1],rates[0][2]) )
                    minrateS  = self.getMinRate( (rates[1][1],rates[1][2],rates[1][3]) )

                    totalScore = int(score.groups()[0]) + int(score.groups()[1])

                    mp = self.session.query(MatchInfo).filter(MatchInfo.matchid == matchid).first()
                    if mp:
                        self.session.delete(mp)
                        self.session.flush()

                    m = MatchInfo(matchid = matchid,
                                match = tds[1].text,
                                date = datetime.datetime.strptime(tds[0].text, '%Y-%m-%d').date(),
                                matchtype = tds[2]['title'],
                                matchtypename = tds[2].text,
                                matchzhu = teams[0]['title'],
                                matchke = teams[2]['title'],
                                matchzhuf = teams[0].text,
                                matchkef = teams[2].text,
                                zhuHScore = int(scoreh.groups()[0]),
                                keHScore = int(scoreh.groups()[1]),
                                zhuScore = int(score.groups()[0]),
                                keScore = int(score.groups()[1]),
                                mResult = mResult,
                                status = tds[6].text,
                                wrate = rates[0][0],
                                drate = rates[0][1],
                                lrate = rates[0][2],
                                minrate = minrate,
                                fixScore = rates[1][0],
                                fixResult = fixResult,
                                wrateS = rates[1][1],
                                drateS = rates[1][2],
                                lrateS = rates[1][3],
                                minrateS = minrateS,
                                singleFlag = singleFlag,
                                score = totalScore,
                                s0 = rates[2][0],
                                s1 = rates[2][1],
                                s2 = rates[2][2],
                                s3 = rates[2][3],
                                s4 = rates[2][4],
                                s5 = rates[2][5],
                                s6 = rates[2][6],
                                s7 = rates[2][7],
                                ww = rates[3][0],
                                wd = rates[3][1],
                                wl = rates[3][2],
                                dw = rates[3][3],
                                dd = rates[3][4],
                                dl = rates[3][5],
                                lw = rates[3][6],
                                ld = rates[3][7],
                                ll = rates[3][8],
                                infoUrl = rateurl)
                    self.session.add(m)
                    self.session.commit()

            return True
        except Exception as ex:
            SysUtil.exceptionPrint(self.logger, ex)
            return False

    def fetchUrl(self, start, end, start_d, end_d):
        for num in range(start,end+1):
            self.logger.info(num)
            urlFech='http://info.sporttery.cn/football/match_result.php?page='+str(num)+'&search_league=0&start_date='+start_d.isoformat()+'&end_date='+end_d.isoformat()+'&dan='
            result = self.getMatch(urlFech)
            while not result:
                self.logger.info(urlFech)
                result = self.getMatch(urlFech)
                time.sleep(random.randint(1,3))

    def getMatresult(self, start_d, end_d):
        self.session.query(MatchInfo).\
            filter(MatchInfo.date == end_d).delete()
        self.session.commit()

        d = self.session.query(func.max(MatchInfo.date)).scalar()
        if d is not None:
            print(d)
            start_d = d - datetime.timedelta(days=1)

        print(start_d)
        print(end_d)

        data = {}
        data['start_date'] = start_d.isoformat()
        data['end_date'] = end_d.isoformat()
        data['search_league'] = '0'
        url = 'http://info.sporttery.cn/football/match_result.php'
        post_data = urllib.parse.urlencode(data)
        req = urllib.request.Request(url=url,data=post_data.encode(),method='POST')
        reqNum = urllib.request.urlopen(req, timeout=10)
        messageNum = reqNum.read().decode('gbk').encode('utf8')
        soupNum = BeautifulSoup(messageNum, 'html.parser')
        alast = soupNum.find("a",title="尾页")
        pageNum = 0
        if not alast:
            pageNum = 2
        else:
            m = re.search(r'match\_result\.php\?page\=(\d+)(.[\S]*)dan=', alast['href'])
            if m:
                pageNum = int(m.groups()[0])

        if pageNum != 0:
            self.logger.info(pageNum)
            start = 1
            for i in range(1,pageNum,100):
                if i == start:
                    continue
                end = i
                self.fetchUrl(start,end,start_d,end_d)
                start = end
            self.fetchUrl(start,pageNum,start_d,end_d)

        self.logger.info('Finish !!!!!!!!!!')


if __name__ == '__main__':
    SpiderSportsBatch().run()
#    SpiderSports500W.SpiderSports500WBatch().run()
