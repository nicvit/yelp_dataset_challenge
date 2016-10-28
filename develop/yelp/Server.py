__author__ = 'Adisorn'
import tornado.ioloop
import tornado.web
import tornado.websocket
import socket
import urlparse
import os
import json

from Logger import LogBroadcaster
from FileExporter import *
from alchemy.nlp import NLPHandler

broadcaster = LogBroadcaster()
nlp_handler = NLPHandler()
nlp_handler.set_broadcaster(broadcaster)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'text/html')
        hostname = urlparse.urlparse("%s://%s"%(self.request.protocol, self.request.host)).hostname
        ip_address = socket.gethostbyname(hostname)
        print(ip_address)

        self.render('index.html', SERVER_NAME=ip_address, SERVER_PORT='8888', HTTPS='off')

"""
    VISUALISATION MESSAGE:

        {
            MSG_TYPE: 'visualise',
            count: n,
            items: [ Array of Dictionary ImageBase64 objects ]
        }

"""

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket opened")
        broadcaster.add_subscriber(self)

    def on_message(self, message):
        #self.write_message(u"You said: " + message)
        #broadcaster.broadcast_message(u"You said: " + message)
        content = json.loads(message)
        msg_type = content['MSG_TYPE']
        if msg_type == 'import':
            pass
            #print("do import")
        elif msg_type == 'nlp':
            pass
            #print("do nlp")
        elif msg_type == 'visualise':
            #print("do visualisation")
            image_message = self.create_image_export_message()
            self.write_message(image_message)

    def on_close(self):
        print("WebSocket closed")
        broadcaster.remove_subscriber(self)

    def create_image_export_message(self):
        json_str = ""
        message_dct = {}
        file_explorer = ImageExporter()
        image_contents = file_explorer.convert_images_to_base64()
        message_dct['MSG_TYPE'] = 'visualise'
        message_dct['count'] = len(image_contents)
        contents = []
        for image_base64 in image_contents:
            contents.append(image_base64.to_dict())

        message_dct['items'] = contents
        json_str = json.dumps(message_dct)

        return json_str


def make_app():
    settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "cookie_secret": "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
        "login_url": "/login",
        "xsrf_cookies": True,
    }
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/ws", WebSocketHandler),
        (r"/(.*)", tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
    ], **settings)


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
