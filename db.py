import sqlite3 as sql

con = sql.connect('gestion_des_taches.db')
cur = con.cursor()
cur.execute(''' CREATE TABLE projects (PID INTEGER PRIMARY KEY AUTOINCREMENT,
                                        PNAME TEXT NOT NULL)''')
cur.execute(''' CREATE TABLE tasks (TID INTEGER PRIMARY KEY AUTOINCREMENT,
                                        TNAME TEXT NOT NULL ,
                                        DESC TEXT NOT NULL ,
                                        PID INTEGER,
                                        FOREIGN KEY (PID) REFERENCES projects (PID))''')

# cur.execute('''DROP TABLE projects''')
# cur.execute('DROP TABLE tasks')
con.commit()
con.close()