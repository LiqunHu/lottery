# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 16:54:06 2016

@author: Administrator
"""
import datetime

from workserver.util import SysUtil
from workserver.module.models import AccountRunningBatch, MatchDataBatch, MatchInfo

SysUtil.global_init()

engine = SysUtil.get_engine_handle()
db = SysUtil.get_db_handle()
session = db()

def dateRange(start,end):
    begin = datetime.datetime.strptime(start,"%Y-%m-%d")
    end = datetime.datetime.strptime(end,"%Y-%m-%d")
    d = begin
    delta = datetime.timedelta(days=1)
    dateList = []
    while d <= end:
        dateList.append(d.strftime("%Y-%m-%d"))
        d += delta
    return dateList

def clearData():
    try:
        session.query(MatchDataBatch).delete()
        session.query(AccountRunningBatch).delete()
        session.commit()
    except Exception as e:
        print(e)

def getMatchDraw(date):
    matches = session.query(MatchInfo).\
        filter(MatchInfo.date == date).\
        filter(MatchInfo.s0 > 1.0).\
        filter(MatchInfo.minrate > 1.2).\
        filter(MatchInfo.minrate < 2.1).all()

    count = 0
    if matches:
        for m in matches:
            md1 = MatchDataBatch( date = date, singleFlag = '4', matchAID = m.matchid, matchAResult = '2', rate = m.s2)
            session.add(md1)
            md2 = MatchDataBatch( date = date, singleFlag = '4', matchAID = m.matchid, matchAResult = '3', rate = m.s3)
            session.add(md2)
            md3 = MatchDataBatch( date = date, singleFlag = '4', matchAID = m.matchid, matchAResult = '4', rate = m.s4)
            session.add(md3)
            session.commit()
            count += 1
            if count > 0:
                break
    return count

def calMoney(date, money):
    matches = session.query(MatchDataBatch).\
        filter(MatchDataBatch.date == date).all()
    if matches:
        base = matches[0].rate
        sumRPara = 1
        for m in matches[1:]:
            sumRPara += base/m.rate
        baseMoney = money / sumRPara
        for m in matches:
            m.money = round(base/m.rate*baseMoney/2,0)*2
        session.commit()

def getMatchMoney(m):
    if m.singleFlag == '4':
        mi = session.query(MatchInfo).\
            filter(MatchInfo.matchid == m.matchAID).first()
        if mi:
            mScore = int(mi.zhuScore) + int(mi.keScore)
            if int(m.matchAResult) == mScore:
                return m.rate * m.money
        else:
            return None
    return 0.00

def calMatResult(date, account, basemoney):
    matches = session.query(MatchDataBatch).\
        filter(MatchDataBatch.date == date).all()

    winMoney = 0.00
    sumMoney = 0.00
    for m in matches:
        sumMoney += m.money
        matchMoney = getMatchMoney(m)
        if matchMoney is None:
            return 0

        if matchMoney:
            winMoney += matchMoney
            m.ResultMoney = matchMoney

    if account:
        fixTotal = account.fixTotal
        fTotalResult = account.totalResult + winMoney - sumMoney
        fRiskMoney = account.riskMoney + winMoney - sumMoney
        if fTotalResult > 10 * basemoney:
            fixTotal = account.fixTotal + fTotalResult
            fTotalResult = 0.00
            fRiskMoney = 0.00
    else:
        fixTotal = 0.00
        fTotalResult = winMoney - sumMoney
        fRiskMoney = winMoney - sumMoney

    ac = AccountRunningBatch(
        date = date,
        useMoney = sumMoney,
        dResult = winMoney-sumMoney,
        riskMoney = fRiskMoney,
        totalResult = fTotalResult,
        fixTotal = fixTotal)
    session.add(ac)
    session.commit()

if __name__ == '__main__':
    clearData()
    basemoney = 200.00
    for date in dateRange('2016-10-24','2017-02-01'):
        money = basemoney
        totalResult = 0.00
        riskMoney = 0.00
        fixTotal = 0.00
        matchCount = getMatchDraw(date)

        if matchCount == 0:
            continue
        if matchCount < 3:
            print(date)
            print(matchCount)


        account = session.query(AccountRunningBatch).order_by(AccountRunningBatch.date.desc()).first()
        if account:
            if account.riskMoney < 0:
                money = ((-1)*account.riskMoney/(basemoney) + 1) * basemoney *matchCount*1.5
                if money < basemoney*0.8:
                    money = basemoney*0.8
#            else:
#                money = basemoney *matchCount/3


        calMoney(date,money)
        calMatResult(date,account,basemoney)
