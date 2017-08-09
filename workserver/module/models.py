# -*- coding: utf-8 -*-
"""
Created on Wed May 18 10:18:23 2016

@author: huliqun
"""
from sqlalchemy import Column, Integer, SmallInteger, String, Date, Time,\
    Text, DateTime, func,BigInteger,Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from workserver.util import GLBConfig

Base = declarative_base()

class User(Base):
    __tablename__ = 'tbl_user'
    userid = Column(String(100), primary_key=True, nullable=False)
    username = Column(String(60), nullable=False)
    accounttype = Column(String(10), nullable=False)
    phone = Column(String(60))
    local = Column(String(250))
    IDNo = Column(String(250))
    _password = Column('password', String(64), default='')
    regdate = Column(DateTime(), default=func.now(), nullable=False)
    expdate = Column(Date())
    payhtimes = Column(Integer, default=0, nullable=False)
    paytimes = Column(Integer, default=0, nullable=False)
    maketime = Column(DateTime(), default=func.now(), nullable=False)
    modifyTime = Column(DateTime(), default=func.now(), nullable=False)
        
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        import hashlib
        # encrypt the password with md5
        self._password = hashlib.md5(password.encode('utf-8')).hexdigest()

class UserData(Base):
    __tablename__ = 'tbl_userdata'
    userid = Column(String(100), primary_key=True, nullable=False)
    basemoney = Column(Float, default=0.0)
    mode = Column(String(10), default='A')
     
class PayLog(Base):
    __tablename__ = 'tbl_paylog'
    uid = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(String(100))
    payDate = Column(Date(), default=func.now(), nullable=False)
    payType = Column(String(10))
    fromDate = Column(DateTime())
    toDate = Column(DateTime())

class AccountRunning(Base):
    __tablename__ = 'tbl_account_running'
    uid = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(String(100))
    date = Column(Date())
    useMoney = Column(Float, default=0.0)
    dResult = Column(Float, default=0.0)
    riskMoney = Column(Float, default=0.0)
    totalResult = Column(Float, default=0.0)
    fixTotal = Column(Float, default=0.0)
    status = Column(String(5), default='1')
    
class MatchData(Base):
    __tablename__ = 'tbl_matchdata'
    uid = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(String(100))
    date = Column(Date())
    singleFlag = Column(String(10))
    matchAID = Column(String(50))
    matchAResult = Column(String(10))
    matchBID = Column(String(50))
    matchBResult = Column(String(10))
    rate = Column(Float, default=0.0)
    money = Column(Float, default=0.0)
    ResultMoney = Column(Float, default=0.0)
    dealerid = Column(Integer)
    status = Column(String(5), default='1')
    
class AccountRunningBatch(Base):
    __tablename__ = 'tbl_account_running_batch'
    uid = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date())
    useMoney = Column(Float, default=0.0)
    dResult = Column(Float, default=0.0)
    riskMoney = Column(Float, default=0.0)
    totalResult = Column(Float, default=0.0)
    fixTotal = Column(Float, default=0.0)
    matchCount = Column(Integer)
    status = Column(String(5), default='1')

class MatchDataBatch(Base):
    __tablename__ = 'tbl_matchdata_batch'
    uid = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date())
    singleFlag = Column(String(10))
    matchAID = Column(String(50))
    matchAResult = Column(String(10))
    matchBID = Column(String(50))
    matchBResult = Column(String(10))
    rate = Column(Float, default=0.0)
    money = Column(Float, default=0.0)
    ResultMoney = Column(Float, default=0.0)
    status = Column(String(5), default='1')    

class Dealer(Base):
    __tablename__ = 'tbl_dealer'
    uid = Column(Integer, primary_key=True, autoincrement=True)
    dealertype = Column(String(10)) 
    name = Column(String(30))
    straightwin = Column(Integer, default=0)
    straightlost = Column(Integer, default=0)
    rule = Column(String(100))
    dealerdesc = Column(Text)
    
class DealerMatch(Base):
    __tablename__ = 'tbl_dealermatch'
    uid = Column(Integer, primary_key=True, autoincrement=True)
    dealerid = Column(BigInteger)
    date = Column(Date())
    matchAID = Column(String(50))
    matchAResult = Column(String(10))
    matchBID = Column(String(50))
    matchBResult = Column(String(10))
    winFlag = Column(String(10))
    matchdesc = Column(Text)
    
class MatchInfo(Base):
    __tablename__ = 'tbl_matchinfo'
    matchid = Column(String(50), primary_key=True)
    match = Column(String(30))
    date = Column(Date())
    matchTime = Column(Time())
    matchtype = Column(String(50))
    matchtypename = Column(String(50))
    matchzhu = Column(String(50))
    matchke = Column(String(50))
    matchzhuf = Column(String(50))
    matchkef = Column(String(50))
    zhuHScore = Column(Integer)
    keHScore = Column(Integer)
    zhuScore = Column(Integer)
    keScore = Column(Integer)
    mResult = Column(String(10))
    status = Column(String(20))
    wrate = Column(Float, default=0.0)
    drate = Column(Float, default=0.0)
    lrate = Column(Float, default=0.0)
    minrate = Column(Float, default=0.0)
    fixScore = Column(Integer)
    fixResult = Column(String(10))
    wrateS = Column(Float, default=0.0)
    drateS = Column(Float, default=0.0)
    lrateS = Column(Float, default=0.0)
    minrateS = Column(Float, default=0.0)
    singleFlag = Column(String(10))
    score = Column(Integer)
    s0 = Column(Float, default=0.0)
    s1 = Column(Float, default=0.0)
    s2 = Column(Float, default=0.0)
    s3 = Column(Float, default=0.0)
    s4 = Column(Float, default=0.0)
    s5 = Column(Float, default=0.0)
    s6 = Column(Float, default=0.0)
    s7 = Column(Float, default=0.0)
    ww = Column(Float, default=0.0)
    wd = Column(Float, default=0.0)
    wl = Column(Float, default=0.0)
    dw = Column(Float, default=0.0)
    dd = Column(Float, default=0.0)
    dl = Column(Float, default=0.0)
    lw = Column(Float, default=0.0)
    ld = Column(Float, default=0.0)
    ll = Column(Float, default=0.0)
    infoUrl = Column(String(200))
    zhuRank = Column(Integer, default=7) 
    keRank = Column(Integer, default=7)
    rankDValue = Column(Integer, default=0)
 
class MatchInfo500(Base):
    __tablename__ = 'tbl_matchinfo_500'
    matchid = Column(String(50), primary_key=True)
    mid = Column(String(50))
    match = Column(String(30))
    date = Column(Date())
    mdate = Column(Date())
    mtime = Column(DateTime())
    matchtype = Column(String(50))
    matchzhu = Column(String(50))
    matchke = Column(String(50))
    zhuRank = Column(Integer, default=7) 
    keRank = Column(Integer, default=7)
    rankDValue = Column(Integer, default=0)
    zhuHScore = Column(Integer)
    keHScore = Column(Integer)
    zhuScore = Column(Integer)
    keScore = Column(Integer)
    mResult = Column(String(10))
    status = Column(String(20))
    wrate = Column(Float, default=0.0)
    drate = Column(Float, default=0.0)
    lrate = Column(Float, default=0.0)
    minrate = Column(Float, default=0.0)
    fixScore = Column(Integer)
    fixResult = Column(String(10))
    wrateS = Column(Float, default=0.0)
    drateS = Column(Float, default=0.0)
    lrateS = Column(Float, default=0.0)
    minrateS = Column(Float, default=0.0)
    singleFlag = Column(String(10)) 

class MatchInfoD(Base):
    __tablename__ = 'tbl_matchinfod'
    matchid = Column(String(50), primary_key=True)
    match = Column(String(30))
    date = Column(Date())
    matchTime = Column(Time())
    matchtype = Column(String(50))
    matchtypename = Column(String(50))
    matchzhu = Column(String(50))
    matchke = Column(String(50))
    matchzhuf = Column(String(50))
    matchkef = Column(String(50))
    zhuHScore = Column(Integer)
    keHScore = Column(Integer)
    zhuScore = Column(Integer)
    keScore = Column(Integer)
    mResult = Column(String(10))
    status = Column(String(20))
    wrate = Column(Float, default=0.0)
    drate = Column(Float, default=0.0)
    lrate = Column(Float, default=0.0)
    minrate = Column(Float, default=0.0)
    fixScore = Column(Integer)
    fixResult = Column(String(10))
    wrateS = Column(Float, default=0.0)
    drateS = Column(Float, default=0.0)
    lrateS = Column(Float, default=0.0)
    minrateS = Column(Float, default=0.0)
    singleFlag = Column(String(10))
    score = Column(Integer)
    s0 = Column(Float, default=0.0)
    s1 = Column(Float, default=0.0)
    s2 = Column(Float, default=0.0)
    s3 = Column(Float, default=0.0)
    s4 = Column(Float, default=0.0)
    s5 = Column(Float, default=0.0)
    s6 = Column(Float, default=0.0)
    s7 = Column(Float, default=0.0)
    ww = Column(Float, default=0.0)
    wd = Column(Float, default=0.0)
    wl = Column(Float, default=0.0)
    dw = Column(Float, default=0.0)
    dd = Column(Float, default=0.0)
    dl = Column(Float, default=0.0)
    lw = Column(Float, default=0.0)
    ld = Column(Float, default=0.0)
    ll = Column(Float, default=0.0)
    infoUrl = Column(String(200))
    zhuRank = Column(Integer, default=7) 
    keRank = Column(Integer, default=7)
    rankDValue = Column(Integer, default=0)
 
class MatchInfo500D(Base):
    __tablename__ = 'tbl_matchinfo_500d'
    matchid = Column(String(50), primary_key=True)
    mid = Column(String(50))
    match = Column(String(30))
    date = Column(Date())
    mdate = Column(Date())
    mtime = Column(DateTime())
    matchtype = Column(String(50))
    matchzhu = Column(String(50))
    matchke = Column(String(50))
    zhuRank = Column(Integer, default=7) 
    keRank = Column(Integer, default=7)
    rankDValue = Column(Integer, default=0)
    zhuHScore = Column(Integer)
    keHScore = Column(Integer)
    zhuScore = Column(Integer)
    keScore = Column(Integer)
    mResult = Column(String(10))
    status = Column(String(20))
    wrate = Column(Float, default=0.0)
    drate = Column(Float, default=0.0)
    lrate = Column(Float, default=0.0)
    minrate = Column(Float, default=0.0)
    fixScore = Column(Integer)
    fixResult = Column(String(10))
    wrateS = Column(Float, default=0.0)
    drateS = Column(Float, default=0.0)
    lrateS = Column(Float, default=0.0)
    minrateS = Column(Float, default=0.0)
    singleFlag = Column(String(10)) 
    
class MatchInfo500Time(Base):
    __tablename__ = 'tbl_matchinfo_500time'
    matchid = Column(String(50), primary_key=True)
    match = Column(String(30))
    mtime = Column(DateTime())
    matchtype = Column(String(50))
    matchzhu = Column(String(50))
    matchke = Column(String(50))
    zhuScore = Column(Integer)
    keScore = Column(Integer)
    zhuHScore = Column(Integer)
    keHScore = Column(Integer)
    mststus = Column(String(50))
    
class PinnaclePara(Base):
    __tablename__ = 'tbl_pinnacle_para'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    cnname = Column(String(100))
    hasOfferings = Column(Boolean)
    leagueSpecialsCount = Column(Integer)
    eventSpecialsCount = Column(Integer)
    eventCount = Column(Integer)
    modifyTime = Column(DateTime(), default=func.now(), nullable=False)
    maketime = Column(DateTime(), default=func.now(), nullable=False)    
    
class PinnacleSports(Base):
    __tablename__ = 'tbl_pinnacle_sports'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(100))
    cnname = Column(String(100))
    hasOfferings = Column(Boolean)
    leagueSpecialsCount = Column(Integer)
    eventSpecialsCount = Column(Integer)
    eventCount = Column(Integer)
    modifyTime = Column(DateTime(), default=func.now(), nullable=False)
    maketime = Column(DateTime(), default=func.now(), nullable=False)

class PinnacleLeagues(Base):
    __tablename__ = 'tbl_pinnacle_leagues'
    id = Column(BigInteger, primary_key=True)
    sportId = Column(BigInteger)
    name = Column(String(100))
    cnname = Column(String(100))
    homeTeamType = Column(String(20))
    hasOfferings = Column(Boolean)
    allowRoundRobins = Column(Boolean)
    leagueSpecialsCount = Column(Integer)
    eventSpecialsCount = Column(Integer)
    eventCount = Column(Integer)
    modifyTime = Column(DateTime(), default=func.now(), nullable=False)
    maketime = Column(DateTime(), default=func.now(), nullable=False)

class PinnacleTimestamp(Base):
    __tablename__ = 'tbl_pinnacle_timestamp'
    uid = Column(Integer, primary_key=True, autoincrement=True)
    tstype = Column(String(100))
    sportId = Column(BigInteger)   
    value1 = Column(BigInteger)
    value2 = Column(String(100))
    modifyTime = Column(DateTime(), default=func.now(), nullable=False)
    maketime = Column(DateTime(), default=func.now(), nullable=False)
    
class PinnacleFixtures(Base):
    __tablename__ = 'tbl_pinnacle_fixtures'
    id = Column(BigInteger, primary_key=True)
    sportId = Column(BigInteger)
    leagueId = Column(BigInteger)
    starts = Column(DateTime)
    home = Column(String(100))
    cnhome = Column(String(100))
    away = Column(String(100))
    cnaway = Column(String(100))
    rotNum = Column(String(50))
    liveStatus = Column(String(5))
    status = Column(String(5))
    parlayRestriction = Column(String(5))
    homePitcher = Column(String(100))
    awayPitcher = Column(String(100))
    modifyTime = Column(DateTime(), default=func.now(), nullable=False)
    maketime = Column(DateTime(), default=func.now(), nullable=False)
    
class PinnacleSettledFixtures(Base):
    __tablename__ = 'tbl_pinnacle_settled_fixtures'
    settlementId = Column(BigInteger, primary_key=True)
    sportId = Column(BigInteger)
    leagueId = Column(BigInteger)
    eventId = Column(BigInteger)
    number = Column(Integer)
    settledAt = Column(DateTime)
    status = Column(String(10))
    team1Score = Column(Integer)
    team2Score = Column(Integer)
    modifyTime = Column(DateTime(), default=func.now(), nullable=False)
    maketime = Column(DateTime(), default=func.now(), nullable=False)
    
class PinnacleSettledSpecialFixtures(Base):
    __tablename__ = 'tbl_pinnacle_settled_Special_fixtures'
    settlementId = Column(BigInteger, primary_key=True)
    SpecialId = Column(BigInteger)
    sportId = Column(BigInteger)
    leagueId = Column(BigInteger)
    settledAt = Column(DateTime)
    modifyTime = Column(DateTime(), default=func.now(), nullable=False)
    maketime = Column(DateTime(), default=func.now(), nullable=False)