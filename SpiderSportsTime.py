# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 16:45:49 2016

@author: Administrator
"""
import urllib
from bs4 import BeautifulSoup
from sqlalchemy.sql import func
from selenium import webdriver
import datetime
import random
import re
import time

from workserver.util import SysUtil
from workserver.batch.BatchBase import BatchBase
from workserver.module.models import MatchInfo500Time

glb_browser = webdriver.PhantomJS()

class SpiderSportsTimeBatch(BatchBase):
    def run(self):
        self.initialize()
        try:
            year = str(datetime.datetime.now().year) + '-'
            the_page = glb_browser.page_source
            soup = BeautifulSoup(the_page, 'html.parser')
            table = soup.find('table', id='table_match')
            if table:
                trs = table.find('tbody').find_all('tr')
                self.session.query(MatchInfo500Time).delete()
                self.session.commit()
                for line in trs:
                    tds = line.find_all('td')
                    if len(tds) < 5:
                        continue
                    if line.has_attr('time'):
                        mtime = datetime.datetime.strptime(line['time'],"%Y-%m-%d %H:%M:%S")
                    else:
                        mtime = datetime.datetime.strptime(year+tds[3].text,"%Y-%m-%d %H:%M")
                        
                    matchid = mtime.strftime('%Y%m%d') + tds[0].text
                    match = tds[0].text
                    matchtype = tds[1].text
                    matchzhu = tds[5].find('a').text
                    matchke = tds[7].find('a').text
                    scores = tds[6].find_all('a')
                    if scores[0].text == '':
                        zhuScore = None
                    else:
                        zhuScore = int(scores[0].text)
                        
                    if scores[2].text == '':
                        keScore = None
                    else:
                        keScore = int(scores[2].text)
                        
                    hScore = self.getScore(tds[8].text)
                    
                    m = MatchInfo500Time( matchid = matchid,
                                          match = match,
                                          mtime = mtime,
                                          matchtype = matchtype,
                                          matchzhu = matchzhu,
                                          matchke = matchke,
                                          zhuScore = zhuScore,
                                          keScore = keScore,
                                          zhuHScore = hScore[0],
                                          keHScore = hScore[1],
                                          mststus = tds[4].text )
                    self.session.add(m)
                    self.session.flush()
                self.session.commit()
                self.logger.info('finish')
        except Exception as ex:
            SysUtil.exceptionPrint(self.logger, ex)
        self.release()
                
    def getScore(self, ScoreStr):
        if ScoreStr is None:
            return [None,None]
        patternScore=re.compile('(\d+) - (\d+)');
        ScoreT = patternScore.findall(ScoreStr)
        if not ScoreT:
            return [None,None]
        else:
            return [int(ScoreT[0][0]),int(ScoreT[0][1])]
        
        
if __name__ == '__main__':
    i = 0
    glb_browser.get('http://live.500.com/')
    while True:
        i +=1
        if i % 200 == 0:
            try:
                glb_browser.get('http://live.500.com/')
            except Exception as ex:
                print(ex)
                time.sleep(random.randint(200))
                continue
            i = 0
        SpiderSportsTimeBatch().run()
        time.sleep(random.randint(20,40))