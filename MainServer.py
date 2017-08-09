# -*- coding: utf-8 -*-
"""
Created on Wed May 18 10:18:23 2016

@author: huliqun
@email: huliquns@126.com
"""
from wsgiref import simple_server
import falcon

from workserver.util import DataFormat
from workserver.util import LogUtil
from workserver.util import SysUtil

from workserver.service import userRegSRV, payMoneySRV, setBaseMoneySRV, getCurrentResultSRV, getGambleResultSRV,\
        getMatchResultSRV, getAccountLogSRV, getdealerSRV, getGameResultSRV, getMatchesSRV, setDealerMatchSRV, getRecommendSRV


LogUtil.initLog()
SysUtil.global_init()
# Configure your WSGI server to load "things.app" (app is a WSGI callable)
app = falcon.API(middleware=[
    DataFormat.JSONTranslator()
])

app.add_route('/sports/webService/userReg', userRegSRV.userRegResource())
app.add_route('/sports/webService/payMoney', payMoneySRV.payMoneyResource())
app.add_route('/sports/webService/setBaseMoney', setBaseMoneySRV.setBaseMoneyResource())
app.add_route('/sports/webService/getCurrentResult', getCurrentResultSRV.getCurrentResultResource())
app.add_route('/sports/webService/getGambleResult', getGambleResultSRV.getGambleResultResource())
#app.add_route('/sports/webService/getMatchResult', getMatchResultSRV.getMatchResultResource())
app.add_route('/sports/webService/getGameResult', getGameResultSRV.getGameResultResource())
app.add_route('/sports/webService/getAccountLog', getAccountLogSRV.getAccountLogResource())
#app.add_route('/sports/webService/getdealer', getdealerSRV.GetDealerSRVResource())
app.add_route('/sports/webService/getRecommend', getRecommendSRV.GetRecommendSRVResource())
app.add_route('/sports/webService/setDealerMatch', setDealerMatchSRV.setDealerMatchSRVResource())
app.add_route('/sports/webService/getMatches', getMatchesSRV.getMatchesResource())
#app.add_route('/sports/webService/dealwithdealer', dealwithdealerSRV.DealWithDealerResource())

# Useful for debugging problems in your API; works with pdb.set_trace(). You
# can also use Gunicorn to host your app. Gunicorn can be configured to
# auto-restart workers when it detects a code change, and it also works
# with pdb.
if __name__ == '__main__':
    httpd = simple_server.make_server('0.0.0.0', 9000, app)
    httpd.serve_forever()

#gunicorn -b 127.0.0.1:9000 MainServer:app