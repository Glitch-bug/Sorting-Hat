import sqlite3 as sql
import os
from random import randint

class datamanager():
    #Core functions
    def __init__(self, db):
        self.database = db
        self.con = sql.connect(self.database)
        self.cur = self.con.cursor()

    def create_tables(self, houses, chat_id):
        self.houses = houses
        Members = f'"Members_{chat_id}"'
        Houses = f'"Houses_{chat_id}"'
        try:
            self.con_houses = self.cur.execute("""
            CREATE TABLE {} (id integer primary key autoincrement, house_name text, house_score integer
            )""".format(Houses))
            self.members = self.cur.execute('CREATE TABLE {} (id INTEGER PRIMARY KEY AUTOINCREMENT, chat_id integer, username text, house_id integer, status text, score integer, user_id integer )'.format(Members))
            self.add_houses_info(houses, chat_id)
            return True
        except sql.OperationalError as sO:
            print(sO)
            return False
    
    
    # House related functions
    def add_houses_info(self, houses, chat_id):
        Houses = f'"Houses_{chat_id}"'
        for house in houses:
            self.cur.execute("INSERT INTO {}(house_name) VALUES(?)".format(Houses), [house])
        self.con.commit()
    
    def house_info(self, chat_id, id=None):
        house_info = None
        Houses = f'"Houses_{chat_id}"'
        if id == None:
            house_info = self.cur.execute("SELECT * FROM {}".format(Houses))
        else:
            house_info = self.cur.execute("SELECT * FROM {} WHERE id = ?".format(Houses),[id])
        return house_info


    def update_house_score(self, id, points, chat_id):
        """A updates a house's score by the specified amount"""
        Houses = f'"Houses_{chat_id}"'
        house_score = self.cur.execute("SELECT house_score FROM {} WHERE id = ?".format(Houses),[id]).fetchone()[0]
        if house_score == None:
            house_score =  int(points)
        else:
            house_score += int(points)
        self.cur.execute("UPDATE {} SET house_score = ? WHERE id = ?".format(Houses),[house_score, id])
        self.con.commit()
        return house_score

    #Member related functions
    def update_member_status(self, chat_id, id, status):
        Members = f'"Members_{chat_id}"'
        self.cur.execute("UPDATE {} SET status = ? WHERE user_id = ?".format(Members), [status, id])
        self.con.commit()

    # def get_admin_list(self, chat_id):
    #     Members = f'"Members_{chat_id}"'
    #     try:
    #         admins = self.cur.execute("SELECT * FROM {} WHERE status = ? OR status = ?".format(Members), ['creator', 'adminsitrator'])
    #         return admins
    #     except sql.OperationalError as sO:
    #         print(sO)
    #         return False
            
    def member_info(self, chat_id, username=None):
        member_info = None
        Members = f'"Members_{chat_id}"'
        print(Members)
        if username == None:
            member_info = self.cur.execute(
                "SELECT * FROM {}".format(Members)
            ).fetchall()
        else:
            member_info = self.cur.execute(
                "SELECT * FROM {} where username = ?".format(Houses),[username]
            ).fetchone()
        return member_info

    def sort_member(self):
        id = randint(1,4)
        return id

    def check_member(self, chat_id, user_id):
        check = self.cur.execute("SELECT house_id FROM {} where user_id= ?".format(chat_id),[user_id]).fetchone()
        return check

    def check_admin(self, chat_id, user_id):
        Members = f'"Members_{chat_id}"'
        check = self.cur.execute("SELECT status FROM {} where user_id= ?".format(Members),[user_id]).fetchone()
        print(check)
        if check == None:
            statement = 'not sorted'
            return statement
        if check[0] == 'student':
            return False
        else:
            return True
        
    def add_member_info(self, username, chat_id, user_id):
        Members = f'"Members_{chat_id}"'
        print(Members)
        user_id = user_id
        check = self.check_member(Members, user_id)
        if  check == None:
            id = self.sort_member()
            self.cur.execute("""
            INSERT INTO {} (chat_id, username, house_id, status, user_id) VALUES(?, ?, ?, ?, ?)""".format(Members),[chat_id, username, id, 'student', user_id])
            self.con.commit()
            return (id, True)
        else:
            return (check, None)