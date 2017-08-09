# -*- coding: utf-8 -*-
"""
Created on Fri May 13 17:05:35 2016

@author: huliqun
"""
import falcon

from workserver.service.ServiceBase import ServiceBase
from workserver.module.models import DealerMatch, Dealer, MatchInfoD
from workserver.util import SysUtil

class GetDealerSRVResource(ServiceBase):
    def on_get(self, req, resp):
        self.initialize()
        maData = []
        for m, d in self.session.query(DealerMatch, Dealer).\
                filter(DealerMatch.date == SysUtil.getTomorrow()).\
                filter(DealerMatch.dealerid == Dealer.uid).all():
            mA = self.session.query(MatchInfoD).filter(
                MatchInfoD.matchid == m.matchAID).first()
            mB = self.session.query(MatchInfoD).filter(
                MatchInfoD.matchid == m.matchBID).first()
            maData.append({'dealerid': m.dealerid,
                           'dealername': d.name,
                           'dealtype': d.dealertype,
                           'dealerdesc': d.dealerdesc,
                           'matchdesc': m.matchdesc,
                           'matchAID': m.matchAID,
                           'matchAResult': m.matchAResult,
                           'matchAtype': mA.matchtypename,
                           'matchAzhu': mA.matchzhu,
                           'matchAke': mA.matchke,
                           'matchAw': mA.wrate,
                           'matchAd': mA.drate,
                           'matchAl': mA.lrate,
                           'matchBID': m.matchBID,
                           'matchBResult': m.matchBResult,
                           'matchBtype': mB.matchtypename,
                           'matchBzhu': mB.matchzhu,
                           'matchBke': mB.matchke,
                           'matchBw': mB.wrate,
                           'matchBd': mB.drate,
                           'matchBl': mB.lrate
                           })
        self.result['data'] = maData
        req.context['result'] = self.result
        resp.set_header('Powered-By', 'huliquns@126.com')
        resp.status = falcon.HTTP_200
        self.release()
