# -*- coding: utf-8 -*-
"""
Created on Fri May 13 17:05:35 2016

@author: huliqun
"""
import falcon
import datetime

from workserver.util import GLBConfig
from workserver.service.ServiceBase import ServiceBase
from workserver.module.models import User
from workserver.util import SysUtil


class userRegResource(ServiceBase):
    def on_get(self, req, resp):
        self.initialize()
        req_para = falcon.util.uri.parse_query_string(req.query_string)

        if 'userid' not in req_para.keys():
            self.errorReturn(GLBConfig.API_ERROR, 'userid 不存在.')
        if 'username' not in req_para.keys():
            self.errorReturn(GLBConfig.API_ERROR, 'username不存在.')
        if 'phone' not in req_para.keys():
            self.errorReturn(GLBConfig.API_ERROR, 'phone不存在.')

        if 'accounttype' not in req_para.keys():
            accounttype = '0'  # 0 业主版 #1 彩民版
        else:
            accounttype = req_para['accounttype']

        user = self.session.query(User).filter(
            User.userid == req_para['userid']).first()
        if user is not None:
            self.errorReturn(GLBConfig.API_ERROR, '用户已经存.')

        try:
            d = datetime.datetime.now()
            delta = datetime.timedelta(days=30)
            expD = d + delta
            user = User(userid=req_para['userid'],
                        username=req_para['username'],
                        accounttype=accounttype,
                        phone=req_para['phone'],
                        local=req_para['local'],
                        IDNo=req_para['IDNo'],
                        expdate=expD
                        )
            self.session.add(user)
            self.session.commit()
            self.result['data'] = 'successReg'
        except Exception as ex:
            SysUtil.exceptionPrint(self.logger, ex)
            self.session.rollback()
            self.errorReturn(GLBConfig.SYSTEM_ERROR, '系统错误')

        req.context['result'] = self.result
        resp.set_header('Powered-By', 'huliquns@126.com')
        resp.status = falcon.HTTP_200
        self.release()
