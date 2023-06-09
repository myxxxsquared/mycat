
import time

import tornado.ioloop
import tornado.web
import tornado.websocket


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.redirect("/static/index.html")

active_clients = set()
last_send_time = None

class WsHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        global active_clients
        active_clients.add(self)

    def on_message(self, _):
        global last_send_time
        current_time = time.time()
        if last_send_time is None or last_send_time < current_time:
            for client in active_clients:
                client.write_message('mo')
            last_send_time = current_time + 3



    def on_close(self):
        global active_clients
        active_clients.remove(self)

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/ws", WsHandler),
        (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': "./static"})
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(7789)
    tornado.ioloop.IOLoop.current().start()
