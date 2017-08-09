# -*- coding: utf-8 -*-
"""
Created on Fri May 20 09:51:58 2016

@author: huliqun
"""

DEBUG = False
dbEchoFlag = False

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = 'zc7#_66#g%u2n$j_)j$-r(swt63d(2l%wc2y=wqt_m8kpy%04*'
#TOKEN_AGE = 86400
#DOMAIN = ''


log_file = './log/server.log'
#log_file = '/home/pwork/workserver/log/serverlog'

dbUrl='mysql+pymysql://root:123456@localhost:33306/lottery?charset=utf8'
#dbUrl='mysql+pymysql://root:password@192.168.2.65:3306/worksp?charset=utf8'
#dbUrl='sqlite:///matchDData.db'

#spyder config
spyderErrorTimes = 3
spyderTimeout = 10
spyderDelayTime = 10
