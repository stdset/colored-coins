import sqlite3 as lite
import json


class Storage(object):
    
    def __init__(self, iniFname = '../data/db.ini'):
        f = open(iniFname)
        parsedData = json.load(f)
        self.__dbPath = parsedData['path']
        self.__mainTable = parsedData['mainTable']
        self.__con = lite.connect(self.__dbPath)
        statement = "SELECT name FROM sqlite_master WHERE type='table' AND name='{0}';".format(self.__mainTable)
        tables = self.execute(statement).fetchall()
        if (not tables) or (self.__mainTable not in tables[0]):
            statement = "CREATE TABLE {0} (color_id INTEGER, txhash TEXT, outindex INTEGER, value REAL, label TEXT);".format(self.__mainTable)
            self.execute(statement)
            statement = "CREATE UNIQUE INDEX data_idx on {0}(color_id, txhash, outindex);".format(self.__mainTable)
            self.execute(statement)
        
    def __enter__(self):
        return self
    
    def __exit__(self, typ, value, traceback):
        if self.__con:
            self.__con.close()
    
    def __del__(self):
        if self.__con:
            self.__con.close()
    
    def execute(self, statement):
        cur = self.__con.cursor()
        cur.execute(statement)
        self.__con.commit()
        return cur
    
    def add(self, color_id, txhash, outindex, value, label):
        substatement = "({0}, \'{1}\', {2}, {3}, \'{4}\')".format(color_id, txhash, outindex, value, label)
        statement = "INSERT OR REPLACE INTO {0} VALUES {1};".format(self.__mainTable, substatement) 
        self.execute(statement)
    
    def remove(self, color_id, txhash, outindex):
        statement = "DELETE FROM {0} WHERE color_id = {1} AND txhash = \'{2}\' AND outindex =  {3};".format(self.__mainTable,
                    color_id, txhash, outindex)
        self.execute(statement)

    def get(self, color_id, txhash, outindex):
        statement = "SELECT value, label FROM {0} WHERE color_id = {1} AND txhash = \'{2}\' AND outindex =  {3};".format(self.__mainTable,
                    color_id, txhash, outindex)
        return self.execute(statement).fetchall()
        
    def get_any(self, txhash, outindex):
        statement = "SELECT color_id, value, label FROM {0} WHERE txhash = \'{1}\' AND outindex =  {2};".format(self.__mainTable,
                    txhash, outindex)
        return self.execute(statement).fetchall()

    def get_all(self, color_id):
        statement = "SELECT txhash, outindex, value, label FROM {0} WHERE color_id = {1};".format(self.__mainTable, color_id)
        return self.execute(statement).fetchall()
