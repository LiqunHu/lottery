# -*- coding: utf-8 -*-
"""
Created on Wed May 18 16:28:01 2016

@author: huliqun
"""

from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy.engine import reflection

from workserver.util import SysUtil
from workserver.util import GLBConfig
from workserver.module.models import User, UserData, PayLog, AccountRunning, MatchData, AccountRunningBatch, MatchDataBatch,\
Dealer, MatchInfo, MatchInfo500, MatchInfoD, MatchInfo500D, DealerMatch, MatchInfo500Time,\
PinnacleSports, PinnacleLeagues, PinnacleTimestamp, PinnacleFixtures, PinnacleSettledFixtures, PinnacleSettledSpecialFixtures

# 为了解决mysql gone away尝试使用NullPool和设置POOL_RECYCLE为5s
#engine = create_engine(DB_CONNECT_STRING, encoding=DB_ENCODING, echo=DB_ECHO, pool_recycle=POOL_RECYCLE, poolclass=NullPool)


def InitTables(engine):
    # delete all tables
    #Base.metadata.drop_all(engine)
    #create all tables
    #Base.metadata.create_all(engine)
    db = scoped_session(sessionmaker(bind=engine))
    tables = reflection.Inspector.from_engine(engine).get_table_names()
    
    if 'tbl_user' not in tables:
        User.__table__.create(engine)
        db.commit()
    
    if 'tbl_userdata' not in tables:
        UserData.__table__.create(engine)
        db.commit()
        
    if 'tbl_paylog' not in tables:
        PayLog.__table__.create(engine)
        db.commit()
    
    if 'tbl_account_running' not in tables:
        AccountRunning.__table__.create(engine)
        db.commit()
        
    if 'tbl_matchdata' not in tables:
        MatchData.__table__.create(engine)
        db.commit()
        
    if 'tbl_account_running_batch' not in tables:
        AccountRunningBatch.__table__.create(engine)
        db.commit()
        
    if 'tbl_matchdata_batch' not in tables:
        MatchDataBatch.__table__.create(engine)
        db.commit()
    
    if 'tbl_dealer' not in tables:
        Dealer.__table__.create(engine)
        db.commit()
        
    if 'tbl_matchinfo' not in tables:
        MatchInfo.__table__.create(engine)
        db.commit()
    
    if 'tbl_matchinfo_500' not in tables:
        MatchInfo500.__table__.create(engine)
        db.commit()
    
    if 'tbl_matchinfod' not in tables:
        MatchInfoD.__table__.create(engine)
        db.commit()
        
    if 'tbl_matchinfo_500d' not in tables:
        MatchInfo500D.__table__.create(engine)
        db.commit()
        
    if 'tbl_dealermatch' not in tables:
        DealerMatch.__table__.create(engine)
        db.commit()
        
    if 'tbl_matchinfo_500time' not in tables:
        MatchInfo500Time.__table__.create(engine)
        db.commit()
        
    if 'tbl_pinnacle_sports' not in tables:
        PinnacleSports.__table__.create(engine)
        db.commit()
        
    if 'tbl_pinnacle_leagues' not in tables:
        PinnacleLeagues.__table__.create(engine)
        db.commit()
    
    if 'tbl_pinnacle_timestamp' not in tables:
        PinnacleTimestamp.__table__.create(engine)
        db.commit()
    
    if 'tbl_pinnacle_fixtures' not in tables:
        PinnacleFixtures.__table__.create(engine)
        db.commit()
    
    if 'tbl_pinnacle_settled_fixtures' not in tables:
        PinnacleSettledFixtures.__table__.create(engine)
        db.commit()
        
    if 'tbl_pinnacle_settled_Special_fixtures' not in tables:
        PinnacleSettledSpecialFixtures.__table__.create(engine)
        db.commit()

if __name__ == '__main__':
    SysUtil.global_init()
    engine = SysUtil.get_engine_handle()
    def msg(msg, *args):
        msg = msg % args
        print("\n\n\n" + "-" * len(msg.split("\n")[0]))
        print(msg)
        print("-" * len(msg.split("\n")[0]))

    msg("Creating Tree Table:")

    InitTables(engine)