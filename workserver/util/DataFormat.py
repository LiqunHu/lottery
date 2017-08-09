# -*- coding: utf-8 -*-
"""
Created on Fri May 13 16:13:02 2016

@author: huliqun
"""
import logging
import falcon
import json
import cgi

from workserver.util import SysUtil

class Parser(cgi.FieldStorage):

    pass


class MultipartMiddleware(object):

    def __init__(self, parser=None):
        self.parser = parser or Parser

    def parse(self, stream, headers, environ):
        return self.parser(fp=stream, headers=headers, environ=environ)

    def process_request(self, req, resp, **kwargs):

        if 'multipart/form-data' not in (req.content_type or ''):
            return

        # This must be done to avoid a bug in cgi.FieldStorage.
        req.env.setdefault('QUERY_STRING', '')

        form = cgi.FieldStorage(req.stream, headers=req.headers ,environ=req.env)
        for key in form:
            field = form[key]
            if not getattr(field, 'filename', False):
                field = form.getlist(key)
            # TODO: put files in req.files instead when #493 get merged.
            req._params[key] = field

class JSONTranslator(object):
    def __init__(self):
        self.logger = logging.getLogger('serverLog')

    def process_request(self, req, resp):
        # req.stream corresponds to the WSGI wsgi.input environ variable,
        # and allows you to read bytes from the request body.
        #
        # See also: PEP 3333
        if req.content_length in (None, 0):
            # Nothing to do
#            self.logger.info(req.headers)
#            self.logger.info('Message length is 0')
            return
            
        if req.content_type.split(';')[0] == 'application/json':
            body = req.stream.read()
            if not body:
                raise falcon.HTTPBadRequest('Empty request body',
                                            'A valid JSON document is required.')
            try:
                req.context['doc'] = json.loads(body.decode('utf-8'))
                if 'user' in req.context:
                    SysUtil.createOperateLog(req)
    
            except (ValueError, UnicodeDecodeError):
                raise falcon.HTTPError(falcon.HTTP_753,
                                       'Malformed JSON',
                                       'Could not decode the request body. The '
                                       'JSON was incorrect or not encoded as '
                                       'UTF-8.')

    def process_response(self, req, resp, resource):
        if 'result' not in req.context:
            return

        resp.body = json.dumps(req.context['result'])
        
        
#    def AuthTrans(self, req):
#        try:
#            paths = req.path.split('/')
#            methodApi = paths[paths.index('api')+1]
#            if methodApi == 'auth' and req.method == 'GET' :
#                return True
#            return False
#        except Exception as ex:
#            self.logger.error(ex)
#            return False
