from tornado.web import Application, StaticFileHandler, RedirectHandler, HTTPError, RequestHandler
from concurrent import futures
import os
from backend import Backend

class FileHandler(RequestHandler):
    def get(self, filename, downloadname):
        self.set_header('Content-Type', 'text/csv')
        self.set_header('Content-Disposition', 'attachment; filename=' + downloadname)
        self.write(open('/tmp/' + filename, 'r').read())

class App(Application):
    executor = futures.ThreadPoolExecutor(max_workers=4)
    sockets = set()

    def __init__(self):
        handlers = [
            (r"/", RedirectHandler, {"url": "/static/"}),
            (r"/static", RedirectHandler, {"url": "/static/"}),
            (r"/static/(.*)", StaticFileHandler,
             {"path": os.path.join(os.path.dirname(__file__), "static"), "default_filename": "index.html"}),
            (r"/ws", Backend),
            (r"/get/file/([^/]+)/([^/]+)", FileHandler),
        ]
        settings = dict(
                cookie_secret="69b12f2d-a02c-4daa-a562-fb1318c6e4c0",
                static_hash_cache=False,
                xsrf_cookies=True,
        )
        Application.__init__(self, handlers, **settings)

Backend.App = App