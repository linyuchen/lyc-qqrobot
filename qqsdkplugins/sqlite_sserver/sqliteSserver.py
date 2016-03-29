#coding:UTF8

"""
sqlite thread
oprate by socket
one database one thread
"""

import threading
import Queue
import traceback
import sys
import json
sys.path.append("..")

import socketpacket
import sqliteclient
sockpack = socketpacket.Packet()

class SqliteSServer(threading.Thread):

    def __init__(self, ip, port, key="nvlike"):

        super(SqliteSServer, self).__init__()

        self.server_sock = sockpack.create_server_sock(ip, port)
        self.key = key
        self.dbs = {} # key db_name, value SqliteWorkerThread
        self.running = True
        

    def add_db(self, db_name, db_path):

        th =SqliteWorkerThread(sqliteclient.Sqlite(db_path))
        th.start()
        self.dbs[db_name] = th



    def run(self):

        while self.running:
            try:
                client_sock = self.server_sock.accept()[0]
                #print client_sock
                cmd = sockpack.read(client_sock)
                cmd = json.loads(cmd)
                #print "cmd", cmd
                if self.key != cmd["key"]:
                    client_sock.close()
                    continue
                cmd["sock"] = client_sock
                db_name = cmd["db_name"]
                self.dbs[db_name].add_cmd(cmd)
            except:
                traceback.print_exc()


class SqliteWorkerThread(threading.Thread):

    def __init__(self, sql_con):

        super(SqliteWorkerThread, self).__init__()
        self.sql_con = sql_con
        self.cmdQueue = Queue.Queue()
        self.running = True

    def handle_cmd(self):

        cmd = self.cmdQueue.get()
        try:
            cmd_type = cmd["cmd"]
            sock = cmd["sock"]
            if cmd_type == "query":
                sqls = cmd["sql_string"]
                escapev = cmd["escape_value"]
                result = self.sql_con.query(sqls, escapev)  

            elif cmd_type == "non_query":
                sqls = cmd["sql_string"]
                escapev = cmd["escape_value"]
                self.sql_con.non_query(sqls, escapev)
                result = "ok"

            elif cmd_type == "get_value":
                table_name = cmd["table_name"]
                key_list = cmd["key_list"]
                where_kw = cmd["where_kw"]
                result = self.sql_con.get_value(table_name, key_list, where_kw)

            elif cmd_type == "set_value":
                table_name = cmd["table_name"]
                set_kw = cmd["set_kw"]
                where_kw = cmd["where_kw"]
                self.sql_con.set_value(table_name, set_kw, where_kw)
                result = "ok"

        except:
            traceback.print_exc()
            result = "error"

        try:
            result = {"result":result}
            result = json.dumps(result)
            sockpack.send(sock, result)
            #sock.close()
        except:
            traceback.print_exc()

    def run(self):

        while self.running:
            self.handle_cmd()
        #print cmd


    def add_cmd(self, cmd):

        self.cmdQueue.put(cmd)




if __name__ == "__main__":

    import os
    import sqlite_db_config
    ip = sqlite_db_config.sqlite_server
    #ip = "127.0.0.1"
    port = sqlite_db_config.sqlite_port
    test = SqliteSServer(ip, port)
    #groupdb_name = sqlite_db_config.groupdb_name
    #groupdb_path = sqlite_db_config.groupdb_path
    test.add_db(sqlite_db_config.rpgdb_name, sqlite_db_config.rpgdb_path)
    test.add_db(sqlite_db_config.groupmdb_name, sqlite_db_config.groupmdb_path)
    test.start()

    # os.system("title db thread")

