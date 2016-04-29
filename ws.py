import tornado.ioloop
import tornado.websocket
from lib.mylib_cls import Json

debug = True
def debug(mes):
    if debug: print(mes)

class WebSocket(tornado.websocket.WebSocketHandler):
    # URL = r"/$"

    def check_origin(self, origin):
        debug(origin)
        self.username, self.secret = WebSocket.get_account(self.request.headers)
        return True

    def open(self):
        self.client_type = self.request.headers.get("Type")
        self.client_type = self.client_type if self.client_type else "sender"
        debug("connect: " + self.username +" type: "+ self.client_type)
        if self.client_type == "receiver":
            self.__class__.add_client(self)
            debug("websocket opened: " +self.username)
            self.__class__.send_message(self, Json(
                username="system",
                message="Hello, " + self.username,
                ))
        debug("{0} : {1}".format(self.__class__, self.clients))


    def on_close(self):
        if self.client_type == "receiver":
            self.__class__.del_client(self)
            debug("websocket closed: " +self.request.headers["User"])
        self.close()
        debug(self.clients)

    @classmethod
    def send_message(cls, target, message):
        for client in cls.clients[target.username]:
            client.write_message(str(message))

    @classmethod
    def all_send_message(cls, message):
        for client in cls.clients.values():
            for ws in client:
                ws.write_message(str(message))

    def other_send_message(self, message):
        selfclient = self.__class__.clients[self.username]
        for client in WebSocket.clients.values():
            if client != selfclient:
                for ws in client:
                    ws.write_message(str(message))

    @classmethod
    def add_client(cls, ws):
        if not ws.username in cls.clients:
            cls.clients[ws.username] = []
        cls.clients[ws.username].append(ws)

    @classmethod
    def del_client(cls, ws):
        cls.clients[ws.username].remove(ws)
        if not cls.clients[ws.username]:
            del cls.clients[ws.username]

    @staticmethod
    def get_account(data):
        return data.get("User"), data.get("Secret")


if __name__ == "__main__":
    import settings
    from importlib import import_module
    wsservers = []
    for appname in settings.APPLICATIONS:
        mod = import_module("{name}.ws".format(name=appname))
        mod.WebSocket.clients = {}
        wsservers.append((mod.WebSocket.URL, mod.WebSocket))
    print("runserver port: {}".format(settings.PORT))
    print("run apps:\n - {}".format("\n - ".join(settings.APPLICATIONS)))

    application = tornado.web.Application(wsservers)
    application.listen(settings.PORT)
    tornado.ioloop.IOLoop.instance().start()
