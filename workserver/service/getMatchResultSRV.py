# -*- coding: utf-8 -*-
"""
Created on Fri May 13 17:05:35 2016

@author: huliqun
"""
import falcon
import datetime
from sqlalchemy.sql import func, or_, and_

from workserver.util import GLBConfig
from workserver.service.ServiceBase import ServiceBase
from workserver.module.models import User,UserData, MatchInfoD, MatchData, AccountRunning
from workserver.util import SysUtil

class getMatchResultResource(ServiceBase):
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
        
        if u.accounttype == GLBConfig.ATYPE_GROUP:
            if u.expdate > datetime.date.today:
                self.errorReturn(GLBConfig.API_ERROR, '用户已过期.')
                
        self.matchCalcMoney(u)
        
        matches = self.session.query(MatchData).\
            filter(MatchData.userid == u.userid).\
            filter(MatchData.date == SysUtil.getTomorrow()).all()
        
        maData = []
        sumMoney = 0.00
        for m in matches:
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
            sumMoney += m.money
        self.result['data'] = maData
        self.result['sumMoney'] = sumMoney
        
        if req_para['gambleFlag'] == '1':
            self.session.commit()
        else:
            self.session.rollback()                               
                               

    def matchCalcMoney(self, u):
        udata = self.session.query(UserData).filter(UserData.userid == u.userid).first()
        if udata is None:
            self.errorReturn(GLBConfig.API_ERROR, '目标金额未设置.')
        
        ct = self.session.query(func.count('*')).\
            filter(MatchData.userid == u.userid).\
            filter(MatchData.date == SysUtil.getToday()).\
            filter(MatchData.ResultMoney == 0).scalar()
        
        if datetime.datetime.now().time() < datetime.time(19,0,0):
            if ct != 0:
                self.errorReturn(GLBConfig.API_ERROR, '有比赛结果未出.')
                
        mCount = self.getMatch(u)
        
        if mCount > 0:
            self.calMoney(u, udata, mCount)
        
        
    def getMatch(self, u):
        tomorrow = SysUtil.getTomorrow
        matches = self.session.query(MatchInfoD).\
            filter(or_(and_(MatchInfoD.date==tomorrow,MatchInfoD.matchTime < '22:00:00'), 
                       and_(MatchInfoD.date==SysUtil.getToday,MatchInfoD.matchTime >= '22:00:00') )).\
            filter(MatchInfoD.singleFlag == '1').\
            filter(MatchInfoD.minrate > 0.1).\
            order_by(MatchInfoD.wrate).all()
            
        count = 0
        for m in matches:
            rateList = (m.wrate,m.drate,m.lrate)
            rateAIdex = getMaxIndex(rateList)
            rateBIdex = getMidIndex(rateList)
            
            if m.minrate < 1.46:
                if m.randDValue > 8 or m.randDValue < -8:
                    rateAIdex = 0
                    rateBIdex = 2
                    
            if m.matchtypename == '欧洲杯' and m.minrate < 1.30:
                rateAIdex = getMinIndex(rateList)
                rateBIdex = getMidIndex(rateList)
            
            if m.matchtypename == '奥运女足' and m.minrate < 1.351:
                rateAIdex = getMinIndex(rateList)
                rateBIdex = getMidIndex(rateList)
            
            if m.matchtypename == '奥运男足' and m.minrate < 1.351:
                rateAIdex = getMinIndex(rateList)
                rateBIdex = getMidIndex(rateList)
            
            mA = MatchData(userid = u.userid,
                    date = tomorrow,
                    matchAID = m.matchid,
                    matchAResult = SysUtil.getMatchResult(rateAIdex),
                    rate = rateList[rateAIdex],
                    singleFlag = '1',
                    matchAFflag = '0')
            self.session.add(mA)
            
            mB = MatchData(userid = u.userid,
                    date = tomorrow,
                    matchAID = m.matchid,
                    matchAResult = SysUtil.getMatchResult(rateBIdex),
                    rate = rateList[rateBIdex],
                    singleFlag = '1',
                    matchAFflag = '0')
            self.session.add(mB)
            self.session.flush()
            count += 1
            if count > 2:
                return count
        return count
                
    def calMoney(self, u, ud, count):
        tomorrow = SysUtil.getTomorrow
        money = ud.basemoney
        account = self.session.query(AccountRunning).\
            filter(AccountRunning.userid == u.userid).\
            filter(AccountRunning.date < tomorrow).\
            order_by(AccountRunning.date.desc()).first()
        
        if account:
            if account.riskMoney < 0:
                money = ((-1)*account.riskMoney/(ud.basemoney) + 1) * ud.basemoney *count/3
                if money < ud.basemoney*0.8:
                    money = ud.basemoney*0.8  
        
        maches = self.session.query(MatchData).\
            filter(MatchData.userid == u.userid).\
            filter(MatchData.date == tomorrow).all()
        
        if len(maches) > 0:
            base = maches[0].rate
            sumRPara = 1
            for m in maches[1:]:
                sumRPara += base/m.rate
                
            for m in maches:
                m.money = round(base/m.rate*ud.baseMoney/2,0)*2
                self.session.flush()