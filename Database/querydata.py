import sqlite3

def create_connection(db_file):
        conn = sqlite3.connect(db_file)
        return conn

def select_all(conn):
    """
    Query all rows in the table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM whitelist")
 
    rows = cur.fetchall()
 
    for row in rows:
        print(row)

def main():
    database = "/home/pi/IOT/Database/iotproject.db"
 
    # create a database connection
    conn = create_connection(database)
    with conn: 
        print("2. Query all tasks")
        select_all(conn)
 
 
if __name__ == '__main__':
    main()
