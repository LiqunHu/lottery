# -*- coding: utf-8 -*-
"""
Created on Fri May 13 17:05:35 2016

@author: huliqun
"""
import falcon

from workserver.util import GLBConfig
from workserver.service.ServiceBase import ServiceBase
from workserver.module.models import User, MatchData, MatchInfo500Time, MatchInfoD
from workserver.util import SysUtil


class getGameResultResource(ServiceBase):
    def on_get(self, req, resp):
        self.initialize()
        req_para = falcon.util.uri.parse_query_string(req.query_string)

        matches = []
        if 'userid' in req_para.keys():
            u = self.session.query(User).filter(
                User.userid == req_para['userid']).first()
            if u is None:
                self.errorReturn(GLBConfig.API_ERROR, '用户不存在.')

            for md, mi, m in self.session.query(MatchData, MatchInfoD, MatchInfo500Time).\
                    filter(MatchData.userid == u.userid).\
                    filter(MatchData.date >= SysUtil.getYesterday()).\
                    filter(MatchData.matchAID == MatchInfoD.matchid).\
                    filter(MatchInfoD.match == MatchInfo500Time.match).all():
                matches.append(m)

            for md, mi, m in self.session.query(MatchData, MatchInfoD, MatchInfo500Time).\
                    filter(MatchData.singleFlag == GLBConfig.M_DUAL).\
                    filter(MatchData.userid == u.userid).\
                    filter(MatchData.date >= SysUtil.getYesterday()).\
                    filter(MatchData.matchBID == MatchInfoD.matchid).\
                    filter(MatchInfoD.match == MatchInfo500Time.match).all():
                matches.append(m)

        else:
            matches = self.session.query(MatchInfo500Time).\
                filter(MatchInfo500Time.mststus != '完').all()
            matchesB = self.session.query(MatchInfo500Time).\
                filter(MatchInfo500Time.mststus == '完').all()
            for m in matchesB:
                matches.append(m)

        maData = []
        if matches:
            for m in matches:
                maData.append({'match': m.match,
                               'mtime': m.mtime.strftime('%Y-%m-%d %H:%M'),
                               'matchtype': m.matchtype,
                               'matchzhu': m.matchzhu,
                               'matchke': m.matchke,
                               'zhuScore': m.zhuScore,
                               'keScore': m.keScore,
                               'zhuHScore': m.zhuHScore,
                               'keHScore': m.keHScore,
                               'mststus': m.mststus})

        self.result['data'] = maData

        req.context['result'] = self.result
        resp.set_header('Powered-By', 'huliquns@126.com')
        resp.status = falcon.HTTP_200
        self.release()
