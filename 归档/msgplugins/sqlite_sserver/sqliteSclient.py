#coding:UTF8
import json
import sys
import time
import traceback
sys.path.append("../sockpack")
import socketpacket

sockpack = socketpacket.Packet()

class Sqlite:

    def __init__(self, ip, port, db_name, key="nvlike"):

        self.port = port
        self.addr = ip
        self.key = key
        self.db_name = db_name

    def send(self, **args):

        result = "error"
        for i in range(1):
            try:
                result = self.__send(args)
                break
            except:
                traceback.print_exc()

        if result == "error":
            raise Exception("database error", u"try again failed")

        return result


    def __send(self, args):

        #print args

        client_sock = sockpack.create_client_sock(self.addr, self.port)
        args["key"] = self.key
        args["db_name"] = self.db_name
        data = json.dumps(args)
        #print data
        sockpack.send(client_sock, data)
        res_data = sockpack.read(client_sock)
        
        #print res_data
        res_data = json.loads(res_data)
        client_sock.close()
        result = res_data["result"]
        if result == "error":
            raise Exception("database error", data)

        return result

    def query(self,sql_string,escape_value=None):

        return self.send(cmd="query", sql_string=sql_string, escape_value=escape_value)

    def non_query(self, sql_string, escape_value=None):

        return self.send(cmd="non_query", sql_string=sql_string, escape_value=escape_value)

    def get_value(self, table_name, key_list, where_kw={}):

        return self.send(cmd="get_value", table_name=table_name, key_list=key_list, where_kw=where_kw)

    def set_value(self, table_name, set_kw, where_kw):

        self.send(cmd="set_value", table_name=table_name, set_kw=set_kw, where_kw=where_kw)


if __name__ == "__main__":

    from sqlite_db_config import sqlite_server
    from sqlite_db_config import sqlite_port
    from sqlite_db_config import groupmdb_name
    test = Sqlite(sqlite_server, sqlite_port, groupmdb_name)
    import time
    st = time.time()
    print test.get_value("t_point", ["point"], {"member_qq":1412971608})
    #print test.query("select point from t_point where member_qq='1412971608'")
#    test.set_value("t_point", {"point":456})
    print time.time() - st
