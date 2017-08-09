# -*- coding: utf-8 -*-
"""
Created on Fri May 13 17:05:35 2016

@author: huliqun
"""
import falcon
from sqlalchemy import text

from workserver.util import GLBConfig
from workserver.service.ServiceBase import ServiceBase
from workserver.module.models import AccountRunning
from workserver.util import SysUtil

class getAccountLogResource(ServiceBase):
    def on_get(self, req, resp):
        self.initialize()
        req_para = falcon.util.uri.parse_query_string(req.query_string)
        
        if 'userid' not in req_para.keys():
            self.errorReturn(GLBConfig.API_ERROR, 'userid 不存在.')
        
        maData = []
        for a in self.session.query(AccountRunning).\
                filter(AccountRunning.userid == req_para['userid']).\
                filter(AccountRunning.status == GLBConfig.ENABLE).\
                order_by(AccountRunning.date.desc()).all():
            maData.append({
                           'date': a.date.isoformat(),
                           'usemoney':a.useMoney,
                           'dresult':a.dResult,
                           'totalresult':a.totalResult + a.fixTotal
                           })
        accountMsg = {}
        try:
            result = self.session.execute(text('select basemoney from tbl_userdata where userid = :uid'), {'uid': req_para['userid'] }).first()
            accountMsg['baseMoney'] = result[0]
            
            result = self.session.execute(text('select expdate from tbl_user where userid = :uid'), {'uid': req_para['userid'] }).first()
            accountMsg['expdate'] = result[0].isoformat()

            result = self.session.execute(text('select min(date) from tbl_account_running where status = "1" and userid = :uid'), {'uid': req_para['userid'] }).first()
            accountMsg['fromDate'] = result[0].isoformat()

            result = self.session.execute(text('select max(date) from tbl_account_running where status = "1" and userid = :uid'), {'uid': req_para['userid'] }).first()
            accountMsg['toDate'] = result[0].isoformat()

            result = self.session.execute(text('select max(usemoney) from tbl_account_running where status = "1" and  userid = :uid'), {'uid': req_para['userid'] }).first()
            accountMsg['maxUse'] = result[0]

            result = self.session.execute(text('select sum(usemoney) from tbl_account_running where status = "1" and userid = :uid'), {'uid': req_para['userid'] }).first()
            accountMsg['sumUse'] = result[0]
            
            result = self.session.execute(text('select truncate(sum(usemoney + dResult),2) from tbl_account_running where status = "1" and userid = :uid'), {'uid': req_para['userid'] }).first()
            accountMsg['sumWin'] = result[0]

            result = self.session.execute(text('select max(usemoney)*0.08 from tbl_account_running where status = "1" and userid = :uid'), {'uid': req_para['userid'] }).first()
            accountMsg['sumCommission'] = result[0]
        except Exception as ex:
            SysUtil.exceptionPrint(self.logger, ex)
            self.errorReturn(GLBConfig.SYSTEM_ERROR, '系统错误.')
        
        self.result['data'] = maData
        self.result['accountMsg'] = accountMsg 
        req.context['result'] = self.result
        resp.set_header('Powered-By', 'huliquns@126.com')
        resp.status = falcon.HTTP_200
        self.release()