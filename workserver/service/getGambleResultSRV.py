# -*- coding: utf-8 -*-
"""
Created on Fri May 13 17:05:35 2016

@author: huliqun
"""
import falcon
import datetime
import json
from sqlalchemy.sql import func, or_, and_

from workserver.util import GLBConfig
from workserver.service.ServiceBase import ServiceBase
from workserver.module.models import User,UserData, MatchInfoD, MatchData, AccountRunning, MatchInfo, DealerMatch
from workserver.util import SysUtil

class getGambleResultResource(ServiceBase):
    def on_get(self, req, resp):
        self.initialize()
        req_para = falcon.util.uri.parse_query_string(req.query_string)
        
        if 'userid' not in req_para.keys():
            self.errorReturn(GLBConfig.API_ERROR, 'userid 不存在.')
        if 'gambleFlag' not in req_para.keys():
            self.errorReturn(GLBConfig.API_ERROR, 'gambleFlag 不存在.')
        
        u = self.session.query(User).filter(User.userid == req_para['userid']).first()
        if u is None:
            self.errorReturn(GLBConfig.API_ERROR, '用户不存在.')
            
        udata = self.session.query(UserData).filter(UserData.userid == u.userid).first()
        if udata is None:
            self.errorReturn(GLBConfig.API_ERROR, '目标金额未设置.')
        
        if u.accounttype == GLBConfig.ATYPE_GROUP:
            if datetime.date.today() > u.expdate:
                self.errorReturn(GLBConfig.API_ERROR, '用户已过期.')
        
        if u.accounttype == GLBConfig.ATYPE_PERSION:
            if udata.mode == GLBConfig.MODE_A:
                if 'dealerid' not in req_para.keys():
                    if 'matchA' not in req_para.keys() \
                            or 'AResult' not in req_para.keys() \
                            or 'matchB' not in req_para.keys() \
                            or 'BResult' not in req_para.keys():
                        self.errorReturn(GLBConfig.API_ERROR, '接口参数不正确.')
            if udata.mode == GLBConfig.MODE_C or udata.mode == GLBConfig.MODE_D:
                if 'matchid' not in req_para.keys():
                    self.errorReturn(GLBConfig.API_ERROR, '接口参数不正确.')                
        self.matchCalcMoney(u, udata, req_para)
        
        matches = self.session.query(MatchData).\
            filter(MatchData.userid == u.userid).\
            filter(MatchData.status == GLBConfig.ENABLE).\
            filter(MatchData.date == SysUtil.getTomorrow()).all()
        
        maData = []
        sumMoney = 0.00
        for m in matches:
            if m.singleFlag == GLBConfig.M_SINGLE:
                matInfo = self.session.query(MatchInfoD).filter(MatchInfoD.matchid == m.matchAID).first()
                maData.append({'match': m.matchAID,
                   'matchtype': matInfo.matchtype,
                   'zhu': matInfo.matchzhu,
                   'ke': matInfo.matchke,
                   'wrate': matInfo.wrate,
                   'drate': matInfo.drate,
                   'lrate': matInfo.lrate,
                   'result': m.matchAResult,
                   'money': m.money})
            else:
                if udata.mode == GLBConfig.MODE_A or udata.mode == GLBConfig.MODE_B:
                    mA = self.session.query(MatchInfoD).filter( MatchInfoD.matchid == m.matchAID ).first()
                    mB = self.session.query(MatchInfoD).filter( MatchInfoD.matchid == m.matchBID ).first()
                    maData.append({'matchAID': m.matchAID,
                                   'matchAResult': m.matchAResult,
                                   'matchAtype':mA.matchtypename,
                                   'matchAzhu':mA.matchzhu,
                                   'matchAke':mA.matchke,
                                   'matchAw':mA.wrate,
                                   'matchAd':mA.drate,
                                   'matchAl':mA.lrate,
                                   'matchBID':m.matchBID,
                                   'matchBResult':m.matchBResult,
                                   'matchBtype':mB.matchtypename,
                                   'matchBzhu':mB.matchzhu,
                                   'matchBke':mB.matchke,
                                   'matchBw':mB.wrate,
                                   'matchBd':mB.drate,
                                   'matchBl':mB.lrate,
                                   'money': m.money})
                elif udata.mode == GLBConfig.MODE_C or udata.mode == GLBConfig.MODE_D:
                    matInfo = self.session.query(MatchInfoD).filter(MatchInfoD.matchid == m.matchAID).first()
                    maData.append({'matchid': m.matchAID,
                                   'matchResult': m.matchAResult,
                                   'matchtype':matInfo.matchtypename,
                                   'matchzhu':matInfo.matchzhu,
                                   'matchke':matInfo.matchke,
                                   'rete':m.rate,
                                   'money':m.money})
            sumMoney += m.money
        self.result['data'] = maData
        self.result['sumMoney'] = sumMoney
        
        if req_para['gambleFlag'] == '1':
            self.session.commit()
        else:
            self.session.rollback()

        req.context['result'] = self.result
        resp.set_header('Powered-By', 'huliquns@126.com')
        resp.status = falcon.HTTP_200
        self.release()                           
                               

    def matchCalcMoney(self, u, udata, req_para):
        self.matchresult(u, udata, SysUtil.getLast2())
        self.matchresult(u, udata, SysUtil.getYesterday())
        self.matchresult(u, udata, SysUtil.getToday())    
            
        ct = self.session.query(func.count('*')).\
            filter(MatchData.userid == u.userid).\
            filter(MatchData.date == SysUtil.getToday()).\
            filter(func.abs(MatchData.ResultMoney) < 0.001).scalar()
        
        if datetime.datetime.now().time() < datetime.time(19,0,0):
            if ct != 0:
                self.errorReturn(GLBConfig.API_ERROR, '有比赛结果未出.')
        
        self.session.commit()
        
        self.session.query(MatchData).\
            filter(MatchData.userid == u.userid).\
            filter(MatchData.date == SysUtil.getTomorrow()).delete()
        
        self.session.flush()
        if u.accounttype == GLBConfig.ATYPE_GROUP:
            self.getMatchGroup(u, udata)
        elif u.accounttype == GLBConfig.ATYPE_PERSION:
            if udata.mode == GLBConfig.MODE_A:
                if 'dealerid' in req_para.keys():
                    self.getMatchModeA(u, udata, req_para['dealerid'])
                if 'matchA' in req_para.keys():
                    self.getMatchModeASelfChoice(u, udata, req_para['matchA'], req_para['AResult'], req_para['matchB'], req_para['BResult'])
            if udata.mode == GLBConfig.MODE_B:
                self.getMatchModeB(u, udata)
            if udata.mode == GLBConfig.MODE_C:
                self.getMatchModeC(u, udata, req_para['matchid'])
            if udata.mode == GLBConfig.MODE_D:
                self.getMatchModeD(u, udata, req_para['matchid'])
        
    def getMatchMoney(self, m):
        mA= self.session.query(MatchInfo).filter(MatchInfo.matchid == m.matchAID).first()
        if mA is None:
            return 0
            
        if m.singleFlag == GLBConfig.M_DUAL:
            mB= self.session.query(MatchInfo).filter(MatchInfo.matchid == m.matchBID).first()
            if mA is None:
                return 0
            
        if mA.mResult:
            if m.singleFlag == GLBConfig.M_SINGLE:
                if mA.mResult == m.matchAResult:
                    return m.rate * m.money
            elif m.singleFlag == GLBConfig.M_DUAL:
                if mA.mResult == m.matchAResult and mB.mResult == m.matchBResult:
                    return m.rate * m.money
            elif m.singleFlag == GLBConfig.M_HAFU:
                if mA.zhuHScore > mA.keHScore:
                    hafuResult = 'w'
                elif mA.zhuHScore == mA.keHScore:
                    hafuResult = 'd'
                elif mA.zhuHScore == mA.keHScore:
                    hafuResult = 'l'
                if mA.zhuScore > mA.keScore:
                    hafuResult += 'w'
                elif mA.zhuScore == mA.keScore:
                    hafuResult += 'd'
                elif mA.zhuScore == mA.keScore:
                    hafuResult += 'l'
                if m.matchAResult == hafuResult:
                    return m.rate * m.money
            elif m.singleFlag == GLBConfig.M_SCORE:
                mScores = int(mA.zhuScore) + int(mA.keScore)
                if int(m.matchAResult) == mScores:
                    return m.rate * m.money
            return -m.money
        return 0
        
    def matchresult(self, u, ud, date):
        account = self.session.query(AccountRunning).\
            filter(AccountRunning.userid == u.userid).\
            filter(AccountRunning.date == date).delete()
        self.session.flush()
            
        account = self.session.query(AccountRunning).\
            filter(AccountRunning.userid == u.userid).\
            filter(AccountRunning.date < date).\
            filter(AccountRunning.status == GLBConfig.ENABLE).\
            order_by(AccountRunning.date.desc()).first()
            
        matches = self.session.query(MatchData).\
            filter(MatchData.userid == u.userid).\
            filter(MatchData.date == date).all()
            
        sumMoney = 0.00
        winMoney = 0.00
        
        i=0
        for m in matches:
            sumMoney += m.money
            m.ResultMoney = self.getMatchMoney(m)
            if m.ResultMoney == 0:
                return
            if m.ResultMoney > 0:
                winMoney += m.ResultMoney
            i+=1
            self.session.flush()
        fixTotal = 0.00
        fTotalResult = 0.00
        fRiskMoney = 0.00
        if account:
            fixTotal = account.fixTotal
            fTotalResult = account.totalResult+winMoney - sumMoney
            fRiskMoney = account.riskMoney+winMoney - sumMoney
        if u.accounttype == GLBConfig.ATYPE_PERSION and ud.mode == GLBConfig.MODE_A:
            if fTotalResult > 0.00:
                fixTotal = fixTotal + fTotalResult 
                fTotalResult = 0.00
                fRiskMoney = 0.00
        else:
            if fTotalResult > 5 * ud.basemoney:
                fixTotal = fixTotal + fTotalResult 
                fTotalResult = 0.00
                fRiskMoney = 0.00
            
        ar = AccountRunning(userid = u.userid,
                            date = date,
                            useMoney = sumMoney,
                            dResult = winMoney - sumMoney,
                            riskMoney = fRiskMoney,
                            totalResult = fTotalResult,
                            fixTotal = fixTotal)
        self.session.add(ar)
        self.session.flush()
    
    def getMatchGroup(self, u, ud):
        tomorrow = SysUtil.getTomorrow()
#            filter(or_(and_(MatchInfoD.date==tomorrow,MatchInfoD.matchTime < datetime.time(22,00,00)), 
#                       and_(MatchInfoD.date==SysUtil.getToday(),MatchInfoD.matchTime >= datetime.time(22,00,00)) )).\
        matches = self.session.query(MatchInfoD).\
            filter(MatchInfoD.date==tomorrow).\
            filter(MatchInfoD.singleFlag == '1').\
            filter(MatchInfoD.minrate > 0.1).\
            order_by(MatchInfoD.wrate).all()
            
        count = 0
        for m in matches:
            rateList = (m.wrate,m.drate,m.lrate)
            rateAIdex = SysUtil.getMaxIndex(rateList)
            rateBIdex = SysUtil.getMidIndex(rateList)
            
            if m.minrate < 1.46:
                if m.rankDValue > 8 or m.rankDValue < -8:
                    rateAIdex = 0
                    rateBIdex = 2
                    
            if m.matchtypename == '欧洲杯' and m.minrate < 1.30:
                rateAIdex = SysUtil.getMinIndex(rateList)
                rateBIdex = SysUtil.getMidIndex(rateList)
            
            if m.matchtypename == '奥运女足' and m.minrate < 1.351:
                rateAIdex = SysUtil.getMinIndex(rateList)
                rateBIdex = SysUtil.getMidIndex(rateList)
            
            if m.matchtypename == '奥运男足' and m.minrate < 1.351:
                rateAIdex = SysUtil.getMinIndex(rateList)
                rateBIdex = SysUtil.getMidIndex(rateList)
            
            mA = MatchData(userid = u.userid,
                    date = tomorrow,
                    matchAID = m.matchid,
                    matchAResult = SysUtil.getMatchResult(rateAIdex),
                    rate = rateList[rateAIdex],
                    singleFlag = GLBConfig.M_SINGLE)
            self.session.add(mA)
            
            mB = MatchData(userid = u.userid,
                    date = tomorrow,
                    matchAID = m.matchid,
                    matchAResult = SysUtil.getMatchResult(rateBIdex),
                    rate = rateList[rateBIdex],
                    singleFlag = GLBConfig.M_SINGLE)
            self.session.add(mB)
            self.session.flush()
            count += 1
            if count > 2:
                break
        if count > 0:
            self.calMoney(u, ud, count)
                
    def calMoney(self, u, ud, count):
        tomorrow = SysUtil.getTomorrow()
        money = ud.basemoney
        account = self.session.query(AccountRunning).\
            filter(AccountRunning.userid == u.userid).\
            filter(AccountRunning.status == GLBConfig.ENABLE).\
            filter(AccountRunning.date < tomorrow).\
            order_by(AccountRunning.date.desc()).first()
        
        if account:
            if account.riskMoney < 0:
                if u.accounttype == GLBConfig.ATYPE_GROUP:
                    money = ((-1)*account.riskMoney/(ud.basemoney) + 1) * ud.basemoney *count/3
                elif u.accounttype == GLBConfig.ATYPE_PERSION:
                    if ud.mode == GLBConfig.MODE_A or ud.mode == GLBConfig.MODE_B:
                        money = ((-1)*account.riskMoney/(ud.basemoney) + 1) * ud.basemoney * count/3
                    elif ud.mode == GLBConfig.MODE_C or ud.mode == GLBConfig.MODE_D:
                        money = ((-1)*account.riskMoney/(ud.basemoney) + 1) * ud.basemoney * count * 1.5
                if money < ud.basemoney*0.8:
                    money = ud.basemoney*0.8  
        
        matches = self.session.query(MatchData).\
            filter(MatchData.userid == u.userid).\
            filter(MatchData.status == GLBConfig.ENABLE).\
            filter(MatchData.date == tomorrow).all()
        
        if len(matches) > 0:
            base = matches[0].rate
            sumRPara = 1
            for m in matches[1:]:
                sumRPara += base/m.rate
            
            baseMoney = money / sumRPara
            for m in matches:
                m.money = round(base/m.rate*baseMoney/2,0)*2
                self.session.flush()
                
    def getMatchModeA(self, u, udata, dealerid):
        tomorrow = SysUtil.getTomorrow()

        matches = self.session.query(DealerMatch).\
            filter(DealerMatch.dealerid == int(dealerid)).\
            filter(DealerMatch.date == tomorrow).first()
            
        if matches is None:
            self.errorReturn(GLBConfig.API_ERROR, '无推荐内容.')
        
        ma = self.session.query(MatchInfoD).filter(MatchInfoD.matchid == matches.matchAID).first()
        mb = self.session.query(MatchInfoD).filter(MatchInfoD.matchid == matches.matchBID).first()
        
        listA = (ma.wrate, ma.drate, ma.lrate)
        listB = (mb.wrate, mb.drate, mb.lrate)
        
        account = self.session.query(AccountRunning).\
            filter(AccountRunning.userid == u.userid).\
            filter(AccountRunning.status == GLBConfig.ENABLE).\
            filter(AccountRunning.date < tomorrow).\
            order_by(AccountRunning.date.desc()).first()
            
        money = 0.0
        if account:
            if account.riskMoney < 0:
                money = account.riskMoney
                
        rate = listA[SysUtil.getResultIndex(matches.matchAResult)] * listB[SysUtil.getResultIndex(matches.matchBResult)]
        mMoney = (udata.basemoney - money) / (rate-1.00)
        
        md = MatchData(userid = u.userid,
                    date = tomorrow,
                    matchAID = matches.matchAID,
                    matchAResult = matches.matchAResult,
                    matchBID = matches.matchBID,
                    matchBResult = matches.matchBResult,
                    rate = rate,
                    money = mMoney,
                    dealerid = dealerid,
                    singleFlag = '2')
        self.session.add(md)
        self.session.flush()
        
    def getMatchModeASelfChoice(self, u, udata, matchA, AResult, matchB, BResult):  
        tomorrow = SysUtil.getTomorrow()
        ma = self.session.query(MatchInfoD).filter(MatchInfoD.matchid == matchA).first()
        if ma is None:
            self.errorReturn(GLBConfig.API_ERROR, '比赛不存在.')
        mb = self.session.query(MatchInfoD).filter(MatchInfoD.matchid == matchB).first()
        if mb is None:
            self.errorReturn(GLBConfig.API_ERROR, '比赛不存在.')
        
        listA = (ma.wrate, ma.drate, ma.lrate)
        listB = (mb.wrate, mb.drate, mb.lrate)
        
        account = self.session.query(AccountRunning).\
            filter(AccountRunning.userid == u.userid).\
            filter(AccountRunning.status == GLBConfig.ENABLE).\
            filter(AccountRunning.date < tomorrow).\
            order_by(AccountRunning.date.desc()).first()
            
        money = 0.0
        if account:
            if account.riskMoney < 0:
                money = account.riskMoney
                
        rate = listA[SysUtil.getResultIndex(AResult)] * listB[SysUtil.getResultIndex(BResult)]
        mMoney = (udata.basemoney - money) / (rate-1.00)
        
        md = MatchData(userid = u.userid,
                    date = tomorrow,
                    matchAID = matchA,
                    matchAResult = AResult,
                    matchBID = matchB,
                    matchBResult = BResult,
                    rate = rate,
                    money = mMoney,
                    singleFlag = '2')
        self.session.add(md)
        self.session.flush()
        
    def getMatchModeB(self, u, ud):
        tomorrow = SysUtil.getTomorrow()

#            filter(or_(and_(MatchInfoD.date==tomorrow,MatchInfoD.matchTime < datetime.time(22,00,00)), 
#                       and_(MatchInfoD.date==SysUtil.getToday(),MatchInfoD.matchTime >= datetime.time(22,00,00)) )).\
        matches = self.session.query(MatchInfoD).\
            filter(MatchInfoD.date==tomorrow).\
            filter(MatchInfoD.singleFlag == '1').\
            filter(MatchInfoD.minrate > 0.1).\
            order_by(MatchInfoD.wrate).all()
            
        count = 0
        for m in matches:
            rateList = (m.wrate,m.drate,m.lrate)
            rateBIdex = SysUtil.getMidIndex(rateList)
            
            if m.minrate < 1.46:
                if m.randDValue > 8 or m.randDValue < -8:
                    rateBIdex = 2
                    
            if m.matchtypename == '欧洲杯' and m.minrate < 1.30:
                rateBIdex = SysUtil.getMidIndex(rateList)
            
            if m.matchtypename == '奥运女足' and m.minrate < 1.351:
                rateBIdex = SysUtil.getMidIndex(rateList)
            
            if m.matchtypename == '奥运男足' and m.minrate < 1.351:
                rateBIdex = SysUtil.getMidIndex(rateList)
            
            mB = MatchData(userid = u.userid,
                    date = tomorrow,
                    matchAID = m.matchid,
                    matchAResult = SysUtil.getMatchResult(rateBIdex),
                    rate = rateList[rateBIdex],
                    singleFlag = GLBConfig.M_SINGLE)
            self.session.add(mB)
            self.session.flush()
            count += 1
            if count > 2:
                break
        if count > 0:
            self.calMoney(u, ud, count)
            
    def getMatchModeC(self, u, ud ,matchid):
        tomorrow = SysUtil.getTomorrow()
        m = self.session.query(MatchInfoD).\
            filter(MatchInfoD.matchid == matchid).first()
            
        count = 1
        md1 = MatchData(userid = u.userid, date = tomorrow, singleFlag = GLBConfig.M_HAFU, matchAID = m.matchid, matchAResult = 'dw', rate = m.dw)
        self.session.add(md1)
        md2 = MatchData(userid = u.userid, date = tomorrow, singleFlag = GLBConfig.M_HAFU, matchAID = m.matchid, matchAResult = 'dd', rate = m.dd)
        self.session.add(md2)
        md3 = MatchData(userid = u.userid, date = tomorrow, singleFlag = GLBConfig.M_HAFU, matchAID = m.matchid, matchAResult = 'dl', rate = m.dl)
        self.session.add(md3)
        self.session.flush()
        if count > 0:
            self.calMoney(u, ud, count)
            
    def getMatchModeD(self, u, ud ,matchid):
        tomorrow = SysUtil.getTomorrow()
        m = self.session.query(MatchInfoD).\
            filter(MatchInfoD.matchid == matchid).first()
            
        count = 1
        md1 = MatchData(userid = u.userid, date = tomorrow, singleFlag = GLBConfig.M_SCORE, matchAID = m.matchid, matchAResult = '2', rate = m.s2)
        self.session.add(md1)
        md2 = MatchData(userid = u.userid, date = tomorrow, singleFlag = GLBConfig.M_SCORE, matchAID = m.matchid, matchAResult = '3', rate = m.s3)
        self.session.add(md2)
        md3 = MatchData(userid = u.userid, date = tomorrow, singleFlag = GLBConfig.M_SCORE, matchAID = m.matchid, matchAResult = '4', rate = m.s4)
        self.session.add(md3)
        self.session.flush()
        if count > 0:
            self.calMoney(u, ud, count)