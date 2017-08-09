# -*- coding: utf-8 -*-
"""
Created on Fri May 13 17:05:35 2016

@author: huliqun
"""
import falcon
import datetime

from workserver.util import GLBConfig
from workserver.service.ServiceBase import ServiceBase
from workserver.module.models import User, PayLog

class payMoneyResource(ServiceBase):
    def on_get(self, req, resp):
        self.initialize()
        req_para = falcon.util.uri.parse_query_string(req.query_string)        
        
        if 'userid' not in req_para.keys():
            self.errorReturn(GLBConfig.API_ERROR,'userid 不存在.')
        if 'payTime' not in req_para.keys():
            self.errorReturn(GLBConfig.API_ERROR,'payTime 不存在.')
            
        if req_para['payTime'] != '1' and req_para['payTime'] != '2':
            self.errorReturn(GLBConfig.API_ERROR,'payTime 不正确.')

        user = self.session.query(User).filter(User.userid == req_para['userid']).first()
        if user is None:
            self.errorReturn(GLBConfig.API_ERROR ,'用户不存在.')
        
        sDdate = datetime.date.today()
        if user.expdate > sDdate:
            sDdate = user.expdate
        if req_para['payTime'] == '1':
            delta = datetime.timedelta(days=183) 
            eDate = sDdate + delta
            user.expdate = eDate
            user.payhtimes += 1
          
        if req_para['payTime'] == '2':
            delta = datetime.timedelta(days=365) 
            eDate = sDdate + delta
            user.expdate = eDate
            user.paytimes += 1
        
        user.modifyTime = datetime.datetime.now()
        
        log = PayLog(userid = user.userid,
                    payType = req_para['payTime'],
                    fromDate = sDdate,
                    toDate = eDate)
        self.session.add(log)
        self.session.commit()
        self.result['data'] = ''
                
        req.context['result'] = self.result
        resp.set_header('Powered-By', 'huliquns@126.com')
        resp.status = falcon.HTTP_200
        self.release()
