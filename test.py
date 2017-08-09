# -*- coding: utf-8 -*-
"""
Created on Sat Apr 09 21:54:27 2016

@author: Administrator
"""

import urllib
import urllib.parse
import urllib.error
import urllib.request
#延长有效期 payTime=1 半年 payTime=2 一年
#accounttype 0 业主版 单关中高赔
#accounttype 1 彩民版 mode A

#url = 'http://127.0.0.1:8000/sports/webService/payMoney?userid=33333&payTime=2' 

#url = 'http://127.0.0.1:8000/sports/webService/userReg?userid=111111&username=aa&phone=18698729471&local=123456&IDNo=111111&accounttype=0'
#url = 'http://127.0.0.1:8000/sports/webService/setBaseMoney?userid=111111&basemoney=100.00'  设置金额 业主版和现在一样， 才民办小于 100 元, mode 字段 彩民班的模式现在有A B两个
#url = 'http://127.0.0.1:8000/sports/webService/getCurrentResult?userid=111111' 获取投注未出结果的比赛信息 动态比分
#url = 'http://127.0.0.1:8000/sports/webService/getdealer?userid=222222' 获取dealer 信息
#url = 'http://127.0.0.1:8000/sports/webService/getGambleResult?userid=111111&gambleFlag=1&dealerid=1'  投注比赛 彩民版 mode A时需要参数 dealerid 从上个借口中获得的
#url = 'http://127.0.0.1:8000/sports/webService/getAccountLog?userid=111111' 获取账户流水信息

#url = 'http://127.0.0.1:9000/sports/webService/userReg?userid=222222&username=aa&phone=18698729472&local=123456&IDNo=111111&accounttype=1'
#url = 'http://127.0.0.1:9000/sports/webService/setBaseMoney?userid=222222&basemoney=200.00&mode=A&reset=1'
#url = 'http://127.0.0.1:9000/sports/webService/getCurrentResult?userid=222222'
#url = 'http://127.0.0.1:9000/sports/webService/getdealer?userid=222222'
#ecodeq = urllib.parse.urlencode({'dealerid': '4',
#                  'matchA': '20161114周日014',
#                  'AResult': 'L',
#                  'matchB': '20161114周日015',
#                  'BResult': 'L',
#                  'desc': '111111111'
#                  })
#url = 'http://218.61.0.136:9000/sports/webService/setDealerMatch?' + ecodeq
#url = 'http://127.0.0.1:9000/sports/webService/getGambleResult?userid=222222&gambleFlag=1&dealerid=1'
#ecodeq = urllib.parse.urlencode({'userid': '222222',
#                  'gambleFlag': '1',
#                  'matchA': '20161114周日014',
#                  'AResult': 'W',
#                  'matchB': '20161114周日015',
#                  'BResult': 'L',
#                  })
#url = 'http://127.0.0.1:9000/sports/webService/getGambleResult?' + ecodeq
#url = 'http://127.0.0.1:9000/sports/webService/getGameResult?userid=222222'
#url = 'http://127.0.0.1:9000/sports/webService/getGameResult'

#url = 'http://127.0.0.1:8000/sports/webService/userReg?userid=33333&username=aa&phone=18698729473&local=123456&IDNo=111111&accounttype=1'
#url = 'http://127.0.0.1:8000/sports/webService/setBaseMoney?userid=33333&basemoney=100.00&mode=B&reset=0'
#url = 'http://127.0.0.1:8000/sports/webService/getCurrentResult?userid=33333'
#url = 'http://127.0.0.1:8000/sports/webService/getGambleResult?userid=33333&gambleFlag=1&dealerid=1'

#url = 'http://127.0.0.1:9000/sports/webService/getAccountLog?userid=222222'
#url = 'http://218.61.0.136:9000/sports/webService/getAccountLog?userid=o0yUowQlKHq_vlDK-gjPaWR-eGEA'
#url = 'http://127.0.0.1:9000/sports/webService/getMatches'
#url = 'http://218.61.0.136:9000/sports/webService/getdealer?userid=o0yUowQlKHq_vlDK-gjPaWR-eGEA'

# 半全场
#url = 'http://127.0.0.1:9000/sports/webService/getRecommend?userid=o0yUowfE2119Am1juh6BPkapWiS4'
#url = 'http://218.61.0.136:9000/sports/webService/getRecommend?userid=o0yUowfE2119Am1juh6BPkapWiS4'
#url = 'http://127.0.0.1:9000/sports/webService/setBaseMoney?userid=o0yUowfE2119Am1juh6BPkapWiS4&basemoney=200.00&mode=C&reset=0'
#url = 'http://127.0.0.1:9000/sports/webService/getCurrentResult?userid=o0yUowfE2119Am1juh6BPkapWiS4'
#ecodeq = urllib.parse.urlencode({'userid': 'o0yUowfE2119Am1juh6BPkapWiS4',
#                                 'gambleFlag': '1',
#                                 'matchids': '["20170216周三001"]'})
#url = 'http://127.0.0.1:9000/sports/webService/getGambleResult?' + ecodeq

# 总比分
#url = 'http://127.0.0.1:9000/sports/webService/getRecommend?tuserid=o0yUowfE2119Am1juh6BPkapWiS4'
#url = 'http://127.0.0.1:9000/sports/webService/setBaseMoney?userid=o0yUowfE2119Am1juh6BPkapWiS4&basemoney=200.00&mode=D&reset=0'
#url = 'http://127.0.0.1:9000/sports/webService/getCurrentResult?userid=o0yUowfE2119Am1juh6BPkapWiS4'
#ecodeq = urllib.parse.urlencode({'userid': 'o0yUowfE2119Am1juh6BPkapWiS4',
#                                 'gambleFlag': '1',
#                                 'matchids': '["20170217周四002"]'})
#url = 'http://127.0.0.1:9000/sports/webService/getGambleResult?' + ecodeq

#url = 'http://218.61.0.136:9000/sports/webService/getGambleResult?userid=o0yUowQlKHq_vlDK-gjPaWR-eGEA&matchid=20170226周日034&gambleFlag=1'

#ecodeq = urllib.parse.urlencode({'userid': 'o0yUowQlKHq_vlDK-gjPaWR-eGEA',
#                                 'gambleFlag': '1',
#                                 'matchid': '20170226周日034'})
#url = 'http://218.61.0.136:9000/sports/webService/getGambleResult?' + ecodeq

url = 'http://127.0.0.1:9000/sports/webService/getAccountLog?userid=b4f7a0c15f2fd1f69369144ac8cad86f'


try:
     
    response= urllib.request.urlopen(url,timeout = 10)
    msg = response.read()
    print(msg.decode('utf-8'))
except urllib.error.HTTPError as e:
    print(e.code)
    print(e.reason)