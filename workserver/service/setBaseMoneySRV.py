# -*- coding: utf-8 -*-
"""
Created on Fri May 13 17:05:35 2016

@author: huliqun
"""
import falcon

from workserver.util import GLBConfig
from workserver.service.ServiceBase import ServiceBase
from workserver.module.models import User, UserData, AccountRunning, MatchData
from workserver.util import SysUtil

class setBaseMoneyResource(ServiceBase):
    def on_get(self, req, resp):
        self.initialize()
        req_para = falcon.util.uri.parse_query_string(req.query_string)
        
        if 'userid' not in req_para.keys():
            self.errorReturn(GLBConfig.API_ERROR,'userid 不存在.')
            
        if 'reset' not in req_para.keys():
            self.errorReturn(GLBConfig.API_ERROR,'reset 不存在.')
        
        try:
            user = self.session.query(User).filter(User.userid == req_para['userid']).first()
            if user is None:
                self.errorReturn(GLBConfig.API_ERROR ,'用户不存在.')
            
            self.session.query(UserData).filter(UserData.userid == user.userid).delete()
            self.session.query(MatchData).filter(MatchData.userid == user.userid).update({MatchData.status: '0'})

            if req_para['reset'] == '1':
                self.session.query(AccountRunning).filter(AccountRunning.userid == user.userid).update({AccountRunning.status: '0'})
            self.session.flush()
            
            if 'mode' in req_para.keys():
                mode = req_para['mode']
            else:
                mode = 'A'
            udata = UserData(userid = user.userid,
                             basemoney = SysUtil.moneyNumFormat(req_para['basemoney']),
                             mode = mode)
            self.session.add(udata)
            self.session.commit()
        except Exception as ex:
            SysUtil.exceptionPrint(self.logger, ex)
            self.session.rollback()
            self.errorReturn(GLBConfig.SYSTEM_ERROR, '系统错误')
                
        req.context['result'] = self.result
        resp.set_header('Powered-By', 'huliquns@126.com')
        resp.status = falcon.HTTP_200
        self.release()
