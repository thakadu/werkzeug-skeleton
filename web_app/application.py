# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from werkzeug.wrappers import Request
from werkzeug.wsgi import ClosingIterator
from werkzeug.exceptions import HTTPException

from web_app.utils import local, local_manager, url_map

app = None


def get_app():
    global app
    if app is None:
        app = App()
    return app


class AppRequest(Request):

    def log(self, msg, *args):
        try:
            print >> self.environ['wsgi.errors'], msg % args
        except Exception:
            print >> self.environ['wsgi.errors'], 'Failed to convert msg', msg


class App(object):
    def __init__(self):
        local.application = self

    def __call__(self, environ, start_response):
        from web_app import views
        #local.application = self
        request = AppRequest(environ)
        local.url_adapter = adapter = url_map.bind_to_environ(environ)
        try:
            endpoint, values = adapter.match()
            handler = getattr(views, endpoint)
            response = handler(request, **values)
        except HTTPException, e:
            response = e
        return ClosingIterator(response(environ, start_response),
                               [local_manager.cleanup])
