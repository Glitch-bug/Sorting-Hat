import sqlite3 as sql
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
            self.members = self.cur.execute('CREATE TABLE {} (id INTEGER PRIMARY KEY AUTOINCREMENT, chat_id integer, username text, house_id integer, status text, score integer)'.format(Members))
            self.con_houses = self.cur.execute("""
            CREATE TABLE {} (id integer primary key autoincrement, house_name text, house_score integer
            )""".format(Houses))
            self.add_houses_info(houses, chat_id)
            return True
        except sql.OperationalError:
            print(sql.OperationalError)
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

    def member_info(self, chat_id, username=None):
        member_info = None
        Members = f'"Members_{chat_id}'
        if username == None:
            member_info = self.cur.execute(
                "SELECT * FROM {}".format(Members)
            )
        else:
            member_info = self.cur.execute(
                "SELECT * FROM {} where id = ?".format(Houses),[username]
            )
        return member_info

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
    def sort_member(self):
        id = randint(1,4)
        return id

    def add_member_info(self, username, chat_id):
        Members = f'"Members_{chat_id}"'
        print(Members)
        id = self.sort_member()
        self.cur.execute("""
        INSERT INTO {} (chat_id, username, house_id, status) VALUES(?, ?, ?, ?)""".format(Members),[chat_id, username, id, 'student'])
        self.con.commit()
        return id