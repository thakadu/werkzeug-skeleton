import re
import bsddb

from os import path
#from urllib2 import Request
#from urllib2 import urlopen

from jinja2 import Environment, FileSystemLoader
from werkzeug.local import Local, LocalManager
from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Response
from simplejson import loads

from settings import BDB_FILENAME


local = Local()
local_manager = LocalManager([local])
application = local('application')

url_map = Map()

TEMPLATE_PATH = path.join(path.dirname(__file__), 'templates')
jinja_env = Environment(loader=FileSystemLoader(TEMPLATE_PATH))


def url_for(endpoint, _external=False, **values):
    return local.url_adapter.build(endpoint, values, force_external=_external)

jinja_env.globals['url_for'] = url_for


def render_template(template, **context):
    return Response(
        jinja_env.get_template(template).render(**context),
        mimetype='text/html')


def expose(rule, **kw):

    def decorate(f):
        kw['endpoint'] = f.__name__
        url_map.add(Rule(rule, **kw))
        return f
    return decorate


