__author__ = 'Adisorn'

import tornado.websocket
import json

class LogBroadcaster(object):

    def __init__(self):
        super(LogBroadcaster, self).__init__()
        self.__subscribers = []

    def add_subscriber(self, web_socket):
        self.__subscribers.append(web_socket)

    def remove_subscriber(self, web_socket):
        self.__subscribers.remove(web_socket)

    def broadcast_message(self, message):
        message_dct = dict()
        message_dct['MSG_TYPE'] = 'broadcast'
        message_dct['content'] = message
        json_str = json.dumps(message_dct)

        for web_socket in self.subscribers:
            web_socket.write_message(json_str)

    @property
    def subscribers(self):
        return self.__subscribers

