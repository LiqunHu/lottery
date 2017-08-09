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
            filter(MatchInfo.date==date).\
            filter(MatchInfo.singleFlag == '1').\
            filter(MatchInfo.minrate > 0.1).\
            order_by(MatchInfo.wrate).all()
        
    count = 0
    if matches:
        for m in matches:
            rateList = (m.wrate,m.drate,m.lrate)
            rateAIdex = SysUtil.getMaxIndex(rateList)
            rateBIdex = SysUtil.getMidIndex(rateList)
            
            if m.minrate < 1.46:
                if m.rankDValue > 8 or m.rankDValue < -8:
                    rateAIdex = 0
                    rateBIdex = 2
            
            mA = MatchDataBatch(date = date,
                    matchAID = m.matchid,
                    matchAResult = SysUtil.getMatchResult(rateAIdex),
                    rate = rateList[rateAIdex],
                    singleFlag = '1')
            session.add(mA)
            
            mB = MatchDataBatch(date = date,
                    matchAID = m.matchid,
                    matchAResult = SysUtil.getMatchResult(rateBIdex),
                    rate = rateList[rateBIdex],
                    singleFlag = '1')
            session.add(mB)
            session.commit()
            count += 1
            if count > 2:
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
    if m.singleFlag == '1':
        mA= session.query(MatchInfo).filter(MatchInfo.matchid == m.matchAID).first()
        if mA:
            if mA.mResult == m.matchAResult:
                return m.rate * m.money
        else:
            return None
    if m.singleFlag == '3':
        mi = session.query(MatchInfo).\
            filter(MatchInfo.matchid == m.matchAID).first()
        if mi:
            if mi.zhuHScore == mi.keHScore:
                if mi.zhuScore > mi.keScore:
                    if m.matchAResult == 'dw':
                        return m.rate * m.money
                        
                if mi.zhuScore == mi.keScore:
                    if m.matchAResult == 'dd':
                        return m.rate * m.money
                        
                if mi.zhuScore < mi.keScore:
                    if m.matchAResult == 'dl':
                        return m.rate * m.money
        else:
            return None
    return 0
        
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
    basemoney = 500.00
    for date in dateRange('2015-01-01','2017-03-14'):
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
                money = ((-1)*account.riskMoney/(basemoney) + 1) * basemoney *matchCount/3
                if money < basemoney*0.8:
                    money = basemoney*0.8
#            else:
#                money = basemoney *matchCount/3
            
            
        calMoney(date,money)
        calMatResult(date,account,basemoney)