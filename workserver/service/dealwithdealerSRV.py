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
from workserver.module.models import User, UserData, MatchInfoD, MatchData, AccountRunning, MatchInfo, DealerMatch
from workserver.util import SysUtil


class DealWithDealerResource(ServiceBase):
    def on_get(self, req, resp):
        self.initialize()
        req_para = falcon.util.uri.parse_query_string(req.query_string)

        if 'userid' not in req_para.keys():
            self.errorReturn(GLBConfig.API_ERROR, 'userid 不存在.')
        if 'dealerid' not in req_para.keys():
            self.errorReturn(GLBConfig.API_ERROR, 'dealerid 不存在.')
        if 'gambleFlag' not in req_para.keys():
            self.errorReturn(GLBConfig.API_ERROR, 'gambleFlag 不存在.')

        u = self.session.query(User).filter(
            User.userid == req_para['userid']).first()
        if u is None:
            self.errorReturn(GLBConfig.API_ERROR, '用户不存在.')

        if u.accounttype != GLBConfig.ATYPE_PERSION:
            self.errorReturn(GLBConfig.API_ERROR, '账户类型错误.')

        if u.expdate > datetime.date.today:
            self.errorReturn(GLBConfig.API_ERROR, '用户已过期.')

        self.matchCalcMoney(u, req_para['dealerid'])

        matches = self.session.query(MatchData).\
            filter(MatchData.userid == u.userid).\
            filter(MatchData.date == SysUtil.getTomorrow()).all()

        maData = []
        sumMoney = 0.00
        for m in matches:
            matInfo = self.session.query(MatchInfoD).filter(
                MatchInfoD.matchid == m.matchAID).first()
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

        req.context['result'] = self.result
        resp.set_header('Powered-By', 'huliquns@126.com')
        resp.status = falcon.HTTP_200
        self.release()

    def matchCalcMoney(self, u, dealerid):
        udata = self.session.query(UserData).filter(
            UserData.userid == u.userid).first()
        if udata is None:
            self.errorReturn(GLBConfig.API_ERROR, '目标金额未设置.')

        self.matchresult(u, udata, SysUtil.getYesterday())
        self.matchresult(u, udata, SysUtil.getToday())

        ct = self.session.query(func.count('*')).\
            filter(MatchData.userid == u.userid).\
            filter(MatchData.date == SysUtil.getToday()).\
            filter(func.abs(MatchData.ResultMoney) < 0.001).scalar()

        if datetime.datetime.now().time() < datetime.time(19, 0, 0):
            if ct != 0:
                self.errorReturn(GLBConfig.API_ERROR, '有比赛结果未出.')

        self.getMatch(u, udata, dealerid)

    def getMatchMoney(self, m):
        mA = self.session.query(MatchInfo).filter(
            MatchInfo.matchid == m.matchAID).first()
        if mA is None:
            return 0.0

        mB = self.session.query(MatchInfo).filter(
            MatchInfo.matchid == m.matchBID).first()
        if mA is None:
            return 0.0

        if mA.mResult and mB.mResult:
            if mA.mResult == m.matchAResult and mB.mResult == m.matchBResult:
                return m.rate * m.money
            else:
                return -m.money
        return 0.0

    def matchresult(self, u, ud, date):
        account = self.session.query(AccountRunning).\
            filter(AccountRunning.userid == u.userid).\
            filter(AccountRunning.date == date).delete()
        self.session.flush()

        account = self.session.query(AccountRunning).\
            filter(AccountRunning.userid == u.userid).\
            filter(AccountRunning.date < date).\
            order_by(AccountRunning.date.desc()).first()

        matches = self.session.query(MatchData).\
            filter(MatchData.userid == u.userid).\
            filter(MatchData.date == date).all()

        sumMoney = 0.00
        winMoney = 0.00

        i = 0
        for m in matches:
            sumMoney += m.money
            m.ResultMoney = self.getMatchMoney(m)
            winMoney += m.ResultMone
            i += 1
            self.session.flush()

        fixTotal = account.fixTotal
        fTotalResult = account.totalResult + winMoney
        fRiskMoney = account.riskMoney + winMoney
        if fTotalResult > 0.00:
            fixTotal = fixTotal + fTotalResult
            fTotalResult = 0.00
            fRiskMoney = 0.00

        ar = AccountRunning(userid=u.userid,
                            date=date,
                            useMoney=sumMoney,
                            dResult=winMoney,
                            riskMoney=fRiskMoney,
                            totalResult=fRiskMoney,
                            fixTotal=fixTotal)
        self.session.add(ar)
        self.session.flush()

    def getMatch(self, u, udata, dealerid):
        tomorrow = SysUtil.getTomorrow()
        self.session.query(MatchData).\
            filter(MatchData.userid == u.userid).\
            filter(MatchData.date == tomorrow).delete()

        self.session.flush()

        matches = self.session.query(DealerMatch).\
            filter(DealerMatch.dealerid == int(dealerid)).\
            filter(DealerMatch.date == SysUtil.getTomorrow()).first()

        if matches is None:
            self.errorReturn(GLBConfig.API_ERROR, '无推荐内容.')

        ma = self.session.query(MatchInfoD).filter(
            MatchInfoD.matchid == matches.matchAID).first()
        mb = self.session.query(MatchInfoD).filter(
            MatchInfoD.matchid == matches.matchBID).first()

        listA = (ma.wrate, ma.drate, ma.lrate)
        listB = (mb.wrate, mb.drate, mb.lrate)

        account = self.session.query(AccountRunning).\
            filter(AccountRunning.userid == u.userid).\
            filter(AccountRunning.date < tomorrow).\
            order_by(AccountRunning.date.desc()).first()

        money = 0.0
        if account:
            if account.riskMoney < 0:
                money = account.riskMoney

        rate = listA[SysUtil.getResultIndex(
            matches.matchAResult)] * listB[SysUtil.getResultIndex(matches.matchBResult)]
        mMoney = (udata.basemony - money) / (rate - 1.00)

        md = MatchData(userid=u.userid,
                       date=tomorrow,
                       matchAID=matches.matchAID,
                       matchAResult=matches.matchAResult,
                       matchBID=matches.matchBID,
                       matchBResult=matches.matchBResult,
                       rate=rate,
                       money=mMoney,
                       singleFlag='2')
        self.session.add(md)
        self.session.flush(md)
