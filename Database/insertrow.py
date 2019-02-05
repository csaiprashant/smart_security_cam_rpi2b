import sqlite3

def create_connection(db_file):
        conn = sqlite3.connect(db_file)
        return conn

def create_project(conn, project):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO whitelist(Distance, Name)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    return cur.lastrowid

def main():
    database = "/home/pi/IOT/Database/iotproject.db"
 
    # create a database connection
    conn = create_connection(database)
    with conn:
        # create a new entry
        project = ("85", "Prashant");
        project_id = create_project(conn, project)

if __name__ == '__main__':
    main()        
