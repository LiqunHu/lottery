# -*- coding: utf-8 -*-
"""
Created on Fri May 13 17:05:35 2016

@author: huliqun
"""
import falcon

from workserver.service.ServiceBase import ServiceBase
from workserver.module.models import DealerMatch, Dealer, MatchInfoD
from workserver.util import SysUtil
from workserver.util import GLBConfig


class setDealerMatchSRVResource(ServiceBase):
    def on_get(self, req, resp):
        self.initialize()
        req_para = falcon.util.uri.parse_query_string(req.query_string)
        if 'dealerid' not in req_para.keys()\
                or 'matchA' not in req_para.keys() \
                or 'AResult' not in req_para.keys() \
                or 'matchB' not in req_para.keys() \
                or 'BResult' not in req_para.keys() \
                or 'desc' not in req_para.keys():
            self.errorReturn(GLBConfig.API_ERROR, '接口参数不正确.')

        if req_para['AResult'] not in ('W', 'D', 'L'):
            self.errorReturn(GLBConfig.API_ERROR, '接口参数不正确.')
        if req_para['BResult'] not in ('W', 'D', 'L'):
            self.errorReturn(GLBConfig.API_ERROR, '接口参数不正确.')

        d = self.session.query(Dealer).\
            filter(Dealer.uid == req_para['dealerid']).\
            filter(Dealer.dealertype == GLBConfig.D_TYPE_H).first()
        if d is None:
            self.errorReturn(GLBConfig.API_ERROR, 'dealer不存在.')

        mA = self.session.query(MatchInfoD).filter(
            MatchInfoD.matchid == req_para['matchA']).first()
        if mA is None:
            self.errorReturn(GLBConfig.API_ERROR, '比赛不存在.')
        mB = self.session.query(MatchInfoD).filter(
            MatchInfoD.matchid == req_para['matchB']).first()
        if mB is None:
            self.errorReturn(GLBConfig.API_ERROR, '比赛不存在.')

        self.session.query(DealerMatch).\
            filter(DealerMatch.date == SysUtil.getTomorrow()).\
            filter(DealerMatch.dealerid == req_para['dealerid']).delete()
        self.session.flush()

        dm = DealerMatch(
            dealerid=req_para['dealerid'],
            date=SysUtil.getTomorrow(),
            matchAID=req_para['matchA'],
            matchAResult=req_para['AResult'],
            matchBID=req_para['matchB'],
            matchBResult=req_para['BResult'],
            matchdesc=req_para['desc']
        )
        self.session.add(dm)
        self.session.commit()

        self.result['data'] = 'success'

        req.context['result'] = self.result
        resp.set_header('Powered-By', 'huliquns@126.com')
        resp.status = falcon.HTTP_200
        self.release()
