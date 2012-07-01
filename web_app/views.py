import urlparse
import os
import simplejson
import logging

from werkzeug.wrappers import Response
from werkzeug import url_encode
from web_app.utils import render_template
from web_app.utils import expose
from web_app.application import get_app
from web_app.settings import BDB_FILENAME

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)


@expose('/')
def home(request):

    return render_template(
        'home.html')


