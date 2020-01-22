
import sqlite3
from sqlite3 import Error
import csv

def create_shows(conn, task):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """
 
    sql = ''' INSERT INTO shows(name,location,rating)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    
    conn.commit()
    return cur.lastrowid

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        conn.commit()
    except Error as e:
        print(e)
        
        
def main():
    database = r"/home/pragati/Downloads/Final project/self-healing-loadbalancer-master/self_healing.db"
 
    sql_create_shows_table = """ CREATE TABLE IF NOT EXISTS shows (
                                        name text PRIMARY KEY,
                                        location text(500),
                                        rating integer
                                    ); """
 
    sql_create_user_table = """CREATE TABLE IF NOT EXISTS user (
                                    username varchar(30) PRIMARY KEY,
                                    password varchar(30)
                                );"""
    sql_create_review_table="""CREATE TABLE IF NOT EXISTS review(
                                    id integer PRIMARY KEY,
                                    name varchar(30) NOT NULL,
                                    show varchar(30),
                                    review text,
                                    upvote integer,
                                    downvote integer,
                                    FOREIGN KEY (name) REFERENCES user(username)
                                );"""
 
    # create a database connection
    conn = create_connection(database)
 
    # create tables
    if conn is not None:
        # create shows table
        create_table(conn, sql_create_shows_table)
 
        # create users table
        create_table(conn, sql_create_user_table)
        
        #create review table
        create_table(conn,sql_create_review_table)
    else:
        print("Error! cannot create the database connection.")
        
    listing=[]
    i=0
    with open("dataset.csv","r", encoding="latin-1") as csv_file:
        rows=csv.reader(csv_file,delimiter=",")
        next(rows,None)
        for row in rows:
            i=i+1
            listing.append(row[0])
            if(i==10):
                print(i,"\n")
                break
    for i in range(10):
        show=(listing[i],"/home/pragati/Downloads/Final project/self-healing-loadbalancer-master/images/"+listing[i]+"/*.jpg",0)
        create_shows(conn,show)
        
 
if __name__ == '__main__':
    main()
