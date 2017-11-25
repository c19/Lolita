# -*- coding: utf-8 -*-
from urlparse import urlparse
from websocketserver import WebSocketServer
import config

class Backend(WebSocketServer):
    """handle logic"""
    App = None
    def __init__(self, *arg, **kwarg):
        super(Backend, self).__init__(*arg, **kwarg)
        self.handlers = {
            "/login": lambda kwarg: {"status": "ok"},
            "/get/records/all": lambda kwarg: config.Config['dbs']['Records'].get_records(**kwarg)
            }
        self.open_handlers = set()

    def check_origin(self, origin):
        origin = urlparse(origin).netloc.lower()
        return origin in ('127.0.0.1:9090', self.request.headers.get("Host"))

    def open(self):
        self.set_nodelay(True)
        self.App.sockets.add(self)

    def on_close(self):
        self.App.sockets.remove(self)