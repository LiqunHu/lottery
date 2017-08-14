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
from workserver.module.models import DuotoneBallLottery


class SpiderDuotoneBallLotteryBatch(BatchBase):
    def run(self):
        self.initialize()
        end = self.getEnd()
        maxNper = self.session.query(
            func.max(DuotoneBallLottery.nper).label('max_nper')).first()
        if maxNper.max_nper:
            start = "%05d" % (int(maxNper.max_nper) + 1)
        else:
            start = '03001'

        self.getPage(start, end)
        self.release()

    def getEnd(self):
        url = 'http://datachart.500.com/ssq/history/history.shtml'
        content = urllib.request.urlopen(url, timeout=10).read()
        message = content.decode('gbk').encode('utf8')
        soup = BeautifulSoup(message, 'html.parser')
        end = soup.find_all(id="end")
        if len(end) > 0:
            return end[0]['value']
        else:
            return None
        
    def getContent(self, url):
        try:
            content = urllib.request.urlopen(url, timeout=10).read()
            return content
        except Exception as ex:
            SysUtil.exceptionPrint(self.logger, ex)
            return None

    def getPage(self, start, end):
        pageSize = 200
        for num in range(int(start), int(end), pageSize):
            time.sleep(random.randint(1, 20))
            start_str = "%05d" % num
            print(start_str)
            endNum = num + pageSize - 1
            if endNum > int(end):
                endNum = int(end)
            end_str = "%05d" % endNum
            url = 'http://datachart.500.com/ssq/history/newinc/history.php?start=' + \
                start_str + '&end=' + end_str
            
            content = self.getContent(url)
            i = 0
            while not content:
                time.sleep(10)
                content = self.getContent(url)
                i = i+1
                if i>10:
                    break
            
            if not content:
                return
            
            soup = BeautifulSoup(content, 'html.parser')
            table = soup.find_all(id="tdata")
            if len(table) > 0:
                for trr in table[0].findAll('tr'):
                    tds = trr.findAll('td')
                    try:
                        d = DuotoneBallLottery(
                            nper=tds[0].text,
                            r1=int(tds[1].text),
                            r2=int(tds[2].text),
                            r3=int(tds[3].text),
                            r4=int(tds[4].text),
                            r5=int(tds[5].text),
                            r6=int(tds[6].text),
                            rArray=str([tds[1].text, tds[2].text, tds[3].text,
                                        tds[4].text, tds[5].text, tds[6].text]),
                            b=int(tds[7].text),
                            hSun=int(tds[8].text.replace(',','')) if tds[8].text != '\xa0' else 0,  # 快乐星期天
                            jackpotBonuses=int(tds[9].text.replace(',','')),
                            firstPrizeNum=tds[10].text.replace(',',''),  # 一等奖注数
                            firstPrizeMoney=tds[11].text.replace(',',''),  # 一等奖奖金
                            secondPrizeNum=tds[12].text.replace(',',''),  # 二等奖注数
                            secondPrizeMoney=tds[13].text.replace(',',''),  # 二等奖奖金
                            totalBet=tds[14].text.replace(',',''),
                            lotteryDate=datetime.datetime.strptime(
                                tds[15].text, '%Y-%m-%d').date()
                        )
                        self.session.add(d)
                        self.session.commit()
                    except Exception as ex:
                        SysUtil.exceptionPrint(self.logger, ex)
            else:
                pass

if __name__ == '__main__':
    SpiderDuotoneBallLotteryBatch().run()
