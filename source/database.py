import sqlite3
import os

class Database:
    def __init__(self):
        self.updatelevel = "update levels set lastlevel=%s where id = 1"
        self.cur = None
        self.con = None
        self.levelunlocked = -1
        if not os.path.isfile("../db"):
            self.con = sqlite3.connect("../db")
            self.cur = self.con.cursor()
            self.dataexists = False
            self.createtablecommand = "create table levels(id int primary key," \
                                      "lastlevel int);"
            self.cur.execute(self.createtablecommand)
            self.cur.execute("insert into levels(id,lastlevel) values(?,?)",(1,1))
            j = self.cur.execute("select * from levels")
            self.con.commit()

            self.levelunlocked = 1
        else:
            self.con = sqlite3.connect("../db")
            self.cur = self.con.cursor()
            self.dataexists = True
            j = self.cur.execute("select * from levels")
            j = self.cur.fetchall()
            self.levelunlocked = j[0][1]

    def insert(self):
        self.cur.execute("insert into levels(id,lastlevel) values(?,?)", (1, 1))
        self.cur.execute("select * from levels")


    def updateLevel(self,i):
        self.cur.execute("select * from levels")
        k = self.cur.fetchall()[0][1]
        if k < 5:
            self.cur.execute(self.updatelevel%(k+1))
        self.cur.execute("select * from levels")
        self.levelunlocked = self.cur.fetchall()[0][1]
        self.con.commit()




if __name__ == '__main__':
    d = Database()
    d.updateLevel(1)

