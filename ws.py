import tornado.ioloop
import tornado.websocket

# import ws_settings


class WebSocket(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        print(origin)
        self.username, self.secret = WebSocket.get_account(self.request.headers)
        return True

    def open(self):
        self.client_type = self.request.headers.get("Type")
        self.client_type = self.client_type if self.client_type else "sender"
        print("connect: " + self.username +" type: "+ self.client_type)
        if self.client_type == "receiver":
            self.__class__.add_client(self)
            print("websocket opened: " +self.username)
        print("{0} : {1}".format(self.__class__, self.clients))
        print(self.client_type)

    def on_close(self):
        if self.client_type == "receiver":
            self.__class__.del_client(self)
            print("websocket closed: " +self.request.headers["User"])
        self.close()
        print(self.clients)

    # @classmethod
    # def send_message(cls, target, message):
    #     print(cls.clients)
    #     for client in cls.get_client(target)[0]:
    #         print("ok : {}".format(cls))
    #         client.write_message(str(message))
    #
    # @classmethod
    # def all_send_message(cls, message):
    #     for clie in cls.clients.values():
    #         for c in clie:
    #             c.write_message(str(message))
    #
    # def other_send_message(self, message):
    #     me = WebSocket.get_client(self)[0]
    #     for clie in WebSocket.clients.values():
    #         if clie != me:
    #             for c in clie:
    #                 c.write_message(str(message))
    #
    # @staticmethod
    # def _extract_user(ws):
    #     return ws.request.headers["User"]
    #
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
    #
    # @classmethod
    # def get_client(cls, ws):
    #     username = WebSocket._extract_user(ws)
    #     return cls.clients[username], username
    #
    @staticmethod
    def get_account(data):
        return data.get("User"), data.get("Secret")


if __name__ == "__main__":
    wsservers = []
    # for i in ws_settings.SERVERS:
    #     mod = __import__(i +".ws")
    #     wsservers.append((mod.ws.SERVER_URL, mod.ws.WebSocket))
    # application = tornado.web.Application(wsservers)
    #
    # application.listen(8000)
    # print("runserver: " + ws_settings.URL)
    # print("run apps:\n - {}".format("\n - ".join(ws_settings.SERVERS)))
    # tornado.ioloop.IOLoop.instance().start()

    WebSocket.clients = {}
    wsservers.append((r"/$", WebSocket))

    import test.ws as sub
    sub.WebSocket.clients = {}
    wsservers.append((r"/sub/$", sub.WebSocket))

    application = tornado.web.Application(wsservers)
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
