# -*- coding: utf-8 -*-
"""
Created on Fri May 13 16:13:02 2016

@author: huliqun
"""
import logging

from workserver.util import LogUtil
from workserver.util import SysUtil


class BatchBase(object):
    db = None
    dbr = None

    def __init__(self):
        className = self.__class__.__name__
        LogUtil.initLogBatch(className)
        SysUtil.global_init()
        self.engine = SysUtil.get_engine_handle()
        self.db = SysUtil.get_db_handle()
        self.logger = logging.getLogger('batchLog_' + className)

    def initialize(self):
        self.session = self.db()

    def release(self):
        self.session.close()

    def errorReturn(self):
        self.session.rollback()
        self.session.close()
