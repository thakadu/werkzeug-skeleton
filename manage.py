#!/usr/bin/env python
import os
from werkzeug import script
from werkzeug.wsgi import SharedDataMiddleware


def make_app():
    from web_app.application import App
    app = SharedDataMiddleware(
        App(),
        {
            '/static': os.path.join(os.path.dirname(__file__), 'web_app/static'),
        })
    return app


def make_shell():
    from web_app import utils
    application = make_app()
    return locals()

action_runserver = script.make_runserver(make_app,
                                         hostname='0.0.0.0',
                                         port=7777,
                                         use_reloader=False)
action_shell = script.make_shell(make_shell)

if __name__ == '__main__':
    script.run()
