import sqlite3 as sl3
def create_new_base():
    connection = sl3.connect("base_test.sql")
    cur = connection.cursor()
    cur.execute("DROP TABLE IF EXISTS users")
    cur.execute("CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass varchar(50), role integer)")



    connection.commit()
    cur.close()
    connection.close()

if __name__ == "__main__":
    create_new_base()