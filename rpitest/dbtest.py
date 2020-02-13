import mysql.connector as mariadb
import sys
mariadb_connection = mariadb.connect(user='user', password='pass', database='smart_lock')
cursor = mariadb_connection.cursor()

if mariadb_connection.is_connected():
    print('sdsdf')
    
    cursor.execute(""" SELECT * FROM user """)
    for row in cursor:
        print(row[1])

