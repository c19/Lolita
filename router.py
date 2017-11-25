import signal
import tornado.ioloop
import ipdb
from concurrent import futures
from tornado.web import Application, StaticFileHandler, RedirectHandler, HTTPError, RequestHandler
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.websocket import WebSocketHandler
from tornado.concurrent import run_on_executor
from app import App
from config import set_config
from datasource.DataSource import get_dbs
import config

define("port", default=9090, help="run on the given port", type=int)
define("debug", default=False, help="pdb.set_trace() when Exception raised", type=bool)
define("config", default="./config/config.json", help="point to config file", type=str)
tornado.options.parse_command_line()

Config = get_dbs(set_config(options.config))
print(Config)
print(config.Config)
def main():
    app = App()
    ioloop = IOLoop.instance()
    app.listen(options.port)

    def shutdown():
        app.shutdown()
        ioloop.stop()

    signal.signal(signal.SIGINT, lambda sig, frame: shutdown())
    print(options.port)
    ioloop.start()


if __name__ == "__main__":
    main()
