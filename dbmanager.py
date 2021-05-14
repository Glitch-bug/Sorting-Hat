import sqlite3 as sql

class datamanager():
    def __init__(self, db):
        self.database = db
        self.con = sql.connect(self.database)
        self.cur = self.con.cursor()

    def create_tables(self, houses):
        self.houses = houses
        try:
            self.members = self.cur.execute("""
            CREATE TABLE Members (id INTEGER PRIMARY KEY AUTOINCREMENT, 
            chat_id integer, username text, house_id integer, status text, score integer)""")
            self.con_houses = self.cur.execute("""
            CREATE TABLE Houses (id integer primary key autoincrement, house_name text, house_score integer
            )""")
            self.add_houses_info(houses)
            return True
        except sql.OperationalError:
            print(sql.OperationalError)
            return False
    
    def add_member_info(self):
        pass
    
    def add_houses_info(self, houses):
        for house in houses:
            self.cur.execute(f"""
            INSERT INTO Houses(house_name) VALUES('{house}')""")
        self.con.commit()
    
    def house_info(self, id=None):
        house_info = None
        if id == None:
            house_info = self.cur.execute("SELECT * FROM Houses")
        else:
            house_info = self.cur.execute(f"SELECT * FROM Houses WHERE id = {id}")
        return house_info
    
    def update_house_score(self, id, points):
        house_score = self.cur.execute(f"SELECT house_score FROM Houses WHERE id = {id}")
        for score in house_score:
            if score[0] == None:
                new_score = 0 + int(points)
                house_score = self.cur.execute(f"SELECT house_score FROM Houses WHERE id = {id}")
            else:
                new_score = score[0] + int(points)
                house_score = self.cur.execute(f"SELECT house_score FROM Houses WHERE id = {id}")
                print(score[0])
                print(score[0].type)
        self.cur.execute(f"UPDATE Houses SET house_score = {new_score} WHERE id = {id}")
        return new_score

    