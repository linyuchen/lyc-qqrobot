#coding: utf-8
import sqlite3


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

    def __make_where_sql(self, kw):

        whereSql = ""
        for k in kw.keys():
            whereSql += " and %s = ?" % k

        return whereSql

    def get_value(self, table_name, key_list, where_kw={}):
        """
        key_list: list
        where_kw: dict
        """
        keySql = ",".join(key_list)
        
        if where_kw:
            param = tuple(where_kw.values())
        else:
            param = None

        if where_kw:
            where_sql = self.__make_where_sql(where_kw)
            sql_string = "SELECT %s FROM %s WHERE 1=1 %s"%(keySql, table_name, where_sql)
        else:
            sql_string = "SELECT %s FROM %s"%(keySql, table_name)
#        print sql_string
#        print param
        result = self.query(sql_string, param)
        return result

    def set_value(self, table_name, set_kw, where_kw):
        """
        set_kw: dict
        where_kw: dict
        """

        set_keys = set_kw.keys()
        values = tuple(set_kw.values())

        #print exists
        if self.get_value(table_name, set_keys, where_kw):
            updateSet = ",".join(["%s=?" % i for i in set_keys])
            where_values = tuple(where_kw.values())
            where_sql = self.__make_where_sql(where_kw)
            sql_str = "UPDATE %s SET %s WHERE 1=1 %s" % (table_name, updateSet, where_sql)
            param = values + where_values
            
            self.non_query(sql_str, param)
        else:
            insertV = ",".join(list("?" * len(set_keys)))
            param = values
            sql_str = "insert into %s(%s) values(%s)" % (table_name, ",".join(set_keys), insertV)
            #print sql_str
            self.non_query(sql_str, param)


class Sqlite_Safe:

    def __init__(self,db_path):

       self.db_path = db_path 

    def query(self,sql_string,escape_value=None):

        sql = Sqlite(self.db_path)
        result = sql.query(sql_string,escape_value)
        sql.close()

        return result

    def non_query(self,sql_string,escape_value=None):

        sql = Sqlite(self.db_path)
        sql.non_query(sql_string,escape_value)
        sql.close()
 

if __name__ == "__main__": 

    test = Sqlite("./sqlite_sserver/rpgdata.db")
    test.set_value("t_person", {"defensive":1000000000000}, {"tag":"499811393"})


#    for i in range(100):
#        threading.Thread(target=func1).start()


            
