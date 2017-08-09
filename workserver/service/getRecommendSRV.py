# -*- coding: utf-8 -*-
"""
Created on Fri May 13 17:05:35 2016

@author: huliqun
"""
import falcon

from workserver.util import GLBConfig
from workserver.service.ServiceBase import ServiceBase
from workserver.module.models import DealerMatch, Dealer, MatchInfoD, UserData
from workserver.util import SysUtil

class GetRecommendSRVResource(ServiceBase):
    def on_get(self, req, resp):
        self.initialize()        
        maData = []
        req_para = falcon.util.uri.parse_query_string(req.query_string)
        if 'userid' not in req_para.keys():
            self.errorReturn(GLBConfig.API_ERROR,'userid 不存在.')
            
        udata = self.session.query(UserData).filter(UserData.userid == req_para['userid']).first()
        if udata is None:
            self.errorReturn(GLBConfig.API_ERROR, '目标金额未设置.')
        
        rType = udata.mode
        
        if rType == GLBConfig.MODE_A: # 推荐2串1
            for m, d in self.session.query(DealerMatch, Dealer).\
                    filter(DealerMatch.date == SysUtil.getTomorrow()).\
                    filter(DealerMatch.dealerid == Dealer.uid).all():
                mA = self.session.query(MatchInfoD).filter( MatchInfoD.matchid == m.matchAID ).first()
                mB = self.session.query(MatchInfoD).filter( MatchInfoD.matchid == m.matchBID ).first()
                maData.append({'dealerid': m.dealerid,
                               'dealername': d.name,
                               'dealtype': d.dealertype,
                               'dealerdesc': d.dealerdesc,
                               'matchdesc': m.matchdesc,
                               'matchAID': m.matchAID,
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
                               'matchBl':mB.lrate
                               })
        elif rType == GLBConfig.MODE_C: #推荐半全场
            for m in self.session.query(MatchInfoD).\
                    filter(MatchInfoD.date == SysUtil.getTomorrow()).\
                    filter(MatchInfoD.ww > 1.0).\
                    filter(MatchInfoD.minrate > 1.9).\
                    filter(MatchInfoD.minrate < 3.0).all():
                maData.append({'matchid': m.matchid,
                               'matchtype': m.matchtypename,
                               'matchzhu':m.matchzhu,
                               'matchke':m.matchke,
                               's0': m.s0,
                               's1': m.s1,
                               's2': m.s2,
                               's3': m.s3,
                               's4': m.s4,
                               's5': m.s5,
                               's6': m.s6,
                               's7': m.s7,
                               'ww': m.ww,
                               'wd': m.wd,
                               'wl': m.wl,
                               'dw': m.dw,
                               'dd': m.dd,
                               'dl': m.dl,
                               'lw': m.lw,
                               'ld': m.ld,
                               'll': m.ll
                               })
        elif rType == GLBConfig.MODE_D: #推荐总进球
            for m in self.session.query(MatchInfoD).\
                    filter(MatchInfoD.date == SysUtil.getTomorrow()).\
                    filter(MatchInfoD.s0 > 1.0).\
                    filter(MatchInfoD.minrate > 1.2).\
                    filter(MatchInfoD.minrate < 2.1).all():
                maData.append({'matchid': m.matchid,
                               'matchtype': m.matchtypename,
                               'matchzhu':m.matchzhu,
                               'matchke':m.matchke,
                               's0': m.s0,
                               's1': m.s1,
                               's2': m.s2,
                               's3': m.s3,
                               's4': m.s4,
                               's5': m.s5,
                               's6': m.s6,
                               's7': m.s7,
                               'ww': m.ww,
                               'wd': m.wd,
                               'wl': m.wl,
                               'dw': m.dw,
                               'dd': m.dd,
                               'dl': m.dl,
                               'lw': m.lw,
                               'ld': m.ld,
                               'll': m.ll
                               })
    
#        print(maData)
        self.result['data'] = maData
        req.context['result'] = self.result
        resp.set_header('Powered-By', 'huliquns@126.com')
        resp.status = falcon.HTTP_200
        self.release()