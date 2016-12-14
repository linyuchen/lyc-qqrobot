#coding=UTF8

import threading
import time
import traceback
import message

Thread = threading.Thread


class EventListener(Thread):

    def __init__(self, msgs, events, errorHandler, interval, qq_client):

        super(EventListener, self).__init__()

        self.msgs = msgs
        self.events = events
        self.errorHandler = errorHandler
        self.interval = interval
        self.running = True
        self.qq_client = qq_client

    def pause(self):

        self.running = False

    def restore(self):

        self.running = True
    
    def run(self):

        while True:
            """
            if not self.running:
                time.sleep(self.interval)
                continue
            """
            msg = self.msgs.get()
            # print u"收到了消息", msg
            for event in self.events:
                while msg.paused:
                    # print u"等待中"
                    pass
                if msg.isOver:
                    break
                try:
                    # s = time.clock()
                    self.qq_client.putFunc(lambda m=msg, e=event: e.main(m))
                    # print u"处理完了消息", event, time.clock() - s
                except Exception, e:
                    error_msg = traceback.format_exc()
                    self.errorHandler(error_msg)
                    msg.resume()
                    msg.destroy()
            time.sleep(self.interval)

