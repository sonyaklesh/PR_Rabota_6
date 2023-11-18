import sqlite3


class Geography:
    # конструктор класса
    def __init__(self):
        self.con = sqlite3.connect("geography.db")
        self.cur = self.con.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS countries "
            "(ID INTEGER PRIMARY KEY,"
            "name TEXT,"
            "region TEXT,"
            "capital TEXT,"
            "territory_area REAL,"
            "population REAL)"
        )
        self.con.commit()

    def __del__(self):
        self.con.close()

    def view(self):
        self.cur.execute("SELECT * FROM countries")
        rows = self.cur.fetchall()
        return rows

    def insert(self, name, region, capital, territory_area, population):
        self.cur.execute("INSERT INTO countries "
                         "VALUES (NULL, ?, ?, ?, ?, ?)",
              (name, region, capital, territory_area, population,))
        self.con.commit()

    def update(self, id, name, region, capital, territory_area, population):
        self.cur.execute("UPDATE countries SET "
                         "name=?, region=?, capital=?, territory_area=?, population=? "
                         "WHERE ID = ?",
                         (name, region, capital,
                                     territory_area, population, id,))
        self.con.commit()

    def delete(self, id):
        self.cur.execute("DELETE from countries "
                         "WHERE ID=?", (id,))
        self.con.commit()

    def search(self, name):
        self.cur.execute("SELECT name, region, capital, territory_area, population FROM countries "
                         "WHERE name=?", (name,))
        rows = self.cur.fetchall()
        return rows