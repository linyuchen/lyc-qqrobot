#coding:UTF8

"""
sqlite thread
oprate by socket
one database one thread
"""

import socket
import sqlite3
import threading
import Queue
import traceback
import json

class SqliteThread(threading.Thread):

    def __init__(self, db_path, port):

        super(SqliteThread, self).__init__()

        self.header_size = 8
        self.header = "%%0%dd" % (self.header_size)
        self.sqlite_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sqlite_sock.bind(("127.0.0.1", port))
        self.sqlite_sock.listen(100)
        self.sqlite = Sqlite(db_path)
        self.running = True

    def run_cmd(self, cmd):

        cmd = cmd.decode("u8")
        cmd = eval(cmd)
        sqls = cmd["sql_string"]
        escapev = cmd["escape_value"]
        cmd = cmd["cmd"]
#        print cmd
        try:
            if cmd == "query":
                return self.sqlite.query(sqls, escapev)  

            elif cmd == "non_query":
                self.sqlite.non_query(sqls, escapev)
        except:
            traceback.print_exc()
            return "error"

    def run(self):

        while self.running:
            try:
                client_sock = self.sqlite_sock.accept()[0]
#                print client_sock
                cmd = ""
                header = client_sock.recv(self.header_size)
                data_length = int(header)
                while 1:
                    data = client_sock.recv(data_length)
                    cmd += data
                    if len(cmd) == data_length:
                        break
#                print cmd
                run_result = self.run_cmd(cmd)
                run_result = unicode({"result":run_result})
                header = self.header % len(run_result)

                client_sock.sendall(header + run_result)

            except:
                traceback.print_exc()


class SqliteWorker:

    def __init__(self, work):

        self.has_result = False
        self.work_result = None
        self.work = work


class Sqlite:

    def __init__(self,db_path):

        self.sqlite = sqlite3.connect(db_path,check_same_thread = False)

        self.cursor = self.sqlite.cursor()

    def query(self,sql_string,escape_value=None):

#        self.cursor = self.sqlite.cursor()
        if not escape_value:
            return self.cursor.execute(sql_string).fetchall()
        else:
            return self.cursor.execute(sql_string,escape_value).fetchall()

    def non_query(self,sql_string,escape_value=None):

#        self.cursor = self.sqlite.cursor()
        if not escape_value:
            self.cursor.execute(sql_string)
        else:
            self.cursor.execute(sql_string,escape_value)
        self.sqlite.commit()

    def close(self):
        self.sqlite.close()

import os
db_path = "./group/groupplugins/qqgroup.db"
db_path = "qqgroup.db"
port = 8880
groupDbTh = SqliteThread(db_path, port)
groupDbTh.start()
db_path = "./group/groupplugins/rpggame/rpgdata.db"
"""
db_path = "./rpggame/rpgdata.db"
port = 8881
rpgDbTh = SqliteThread(db_path, port)
rpgDbTh.start()
"""
os.system("title db thread")
