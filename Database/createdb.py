import sqlite3

def create_connection(db_file):
	conn = sqlite3.connect(db_file)
	conn.close()
 
if __name__ == '__main__':
    create_connection("/home/pi/IOT/Database/iotproject.db")
