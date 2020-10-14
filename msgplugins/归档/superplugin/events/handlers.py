# -*- coding:utf8 -*-


class EventHandler(object):

    def __init__(self, event):
        self.event = event
        self.stop = False

    def handle(self):
        pass


class HandlerManager(object):

    def __init__(self):
        self.handlers = []

    def handle(self):
        for handler in self.handlers:
            if handler.stop:
                break
            handler.handle()
