# -*- coding: utf-8 -*-
"""
Created on Tue May 17 10:59:20 2016

@author: huliqun
"""
import random, string
import json
import traceback
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.pool import QueuePool

import workserver.settings as settings

#http://stackoverflow.com/questions/5022066/how-to-serialize-sqlalchemy-result-to-json
def json_alchemy_encoder(revisit_self = False, fields_excape = []):
    _visited_objs = []
    class AlchemyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj.__class__, DeclarativeMeta):
                # don't re-visit self
                if revisit_self:
                    if obj in _visited_objs:
                        return None
                    _visited_objs.append(obj)

                # go through each field in this SQLalchemy class
                fields = {}
                for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                    val = obj.__getattribute__(field)

                    # is this field another SQLalchemy object, or a list of SQLalchemy objects?
                    if isinstance(val.__class__, DeclarativeMeta) or (isinstance(val, list) and len(val) > 0 and isinstance(val[0].__class__, DeclarativeMeta)):
                        # unless we're expanding this field, stop here
                        if field in fields_excape:
                            # not expanding this field: set it to None and continue
                            continue
                    try:
                        json.dumps(val)     # this will fail on non-encodable values, like other classes
                        fields[field] = val
                    except TypeError:    # 添加了对datetime的处理
                        if isinstance(val, datetime.datetime):
                            if field == 'modifytime':
                                fields[field] = val.strftime('%Y-%m-%d %H:%M:%S')
                            else:
                                fields[field] = val.strftime('%Y-%m-%d')
                        elif isinstance(val, datetime.date):
                            fields[field] = val.isoformat()
                        elif isinstance(val, datetime.timedelta):
                            fields[field] = (datetime.datetime.min + val).time().isoformat()
                        else:
                            fields[field] = None
                # a json-encodable dict
                return fields

            return json.JSONEncoder.default(self, obj)
    return AlchemyEncoder

def schema2Json(schemaIns):
    return json.loads(json.dumps(schemaIns, cls=json_alchemy_encoder(False, []), check_circular=False))    
    
class GlobalVar:
    engine_handle = None
    enginer_handle = None
    db_handle = None
    dbr_handle = None
    glb_browser = None
    glb_browser_in_use = 0

def global_init():
    GlobalVar.engine_handle = create_engine(settings.dbUrl) # encoding="utf-8",poolclass=QueuePool, pool_size=50, pool_recycle=3600, echo=False
    GlobalVar.db_handle = sessionmaker(bind=GlobalVar.engine_handle)
    
def get_engine_handle():
    return GlobalVar.engine_handle
    
def get_db_handle():
    return GlobalVar.db_handle
    
def random_word(length):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))

def exceptionPrint(logger, ex):
    if logger:
        logger.error(traceback.print_exc())
        logger.error(ex)
    else:
        print(ex)

def getTomorrow():
    return datetime.date.today() + datetime.timedelta(days=1)
    
def getToday(): 
    return datetime.date.today()

def getLast2():
    return datetime.date.today() - datetime.timedelta(days=2)
 
def getYesterday():
    return datetime.date.today() - datetime.timedelta(days=1)
    
def numMoneyFormat(num):
    return '%.2f' % (num)
    
def moneyNumFormat(money):
    return float(money)
    
def getMinIndex(my_list):
    minNum = min(my_list)
    return my_list.index(minNum)

def getMaxIndex(my_list):
    maxNum = max(my_list)
    return my_list.index(maxNum)

def getMidIndex(my_list):
    idexG = [0,1,2]
    idexG.remove(getMinIndex(my_list))
    idexG.remove(getMaxIndex(my_list))
    return idexG[0]

def getMatchResult(indexM):
    if indexM == 0:
        return 'W'
    if indexM == 1:
        return 'D'   
    if indexM == 2:
        return 'L'
        
def getResultIndex(result):
    if result == 'W':
        return 0
    if result == 'D':
        return 1 
    if result == 'L':
        return 2