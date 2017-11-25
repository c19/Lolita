# -*- coding: utf-8 -*-
import json
import hashlib
import hmac
import traceback
from tornado.websocket import WebSocketHandler
from tornado.options import options
from base import do, date_handler, update, ensure_utf8
from users import Users

class AuthFailed(Exception):
    pass

class WebSocketServer(WebSocketHandler):
    def __init__(self, *arg, **kwarg):
        handlers = {}
        open_handlers = set()
        super(WebSocketServer, self).__init__(*arg, **kwarg)

    def write_message(self, msg):
        super(WebSocketServer, self).write_message(
                msg if isinstance(msg, str) else json.dumps(msg, default=date_handler))

    def handle(self, message):
        params = json.loads(message)
        protocol = params.get('protocol')
        ret = params.get('ret')
        action = params.get('action')

        def checkauth(handle):
            if handle and handle not in self.open_handlers:
                username, sign = params.get('user', ''), params.get('sign', '')
                user = Users.get(username)
                if not user:
                    raise AuthFailed('帐号或密码错误')
                content = message[:-(len(username) + len(sign) + 21)] + '}'
                if not all([user.secret_key, sign,
                            sign == hmac.new(user.secret_key, ensure_utf8(content), hashlib.sha256).hexdigest()]):
                    raise AuthFailed('帐号或密码错误')
                if not user.able_to(protocol):
                    raise AuthFailed('没有权限')
            return handle

        def errorwrap(handle):
            def add_ret(dic):
                if ret:
                    dic["ret"] = ret
                return dic

            def deal():
                if not handle:
                    return add_ret({"status": "error", "msg": "unkown protocol: {0}".format(protocol)})
                else:
                    return add_ret({"status": "ok", "result": handle(params)})

            if options.debug:
                return deal()
            else:
                try:
                    return deal()
                except Exception as e:
                    traceback.print_exc()
                    return add_ret({"status": "error", "msg": str(e)})

        try:
            do(protocol,
               self.handlers.get,
               checkauth,
               errorwrap,
               lambda dic: update(dic, {"protocol": protocol}) if dic else None,
               lambda result: App.broadcast(result) if params.get('broadcast') else self.write_message(
                       result) if result else None,
               )
        except AuthFailed as e:
            self.write_message(
                    {"protocol": "/login", "status": "ok", "result": {"status": "AuthFailed", "msg": str(e)}})

    def on_message(self, message):
        self.handle(message)
