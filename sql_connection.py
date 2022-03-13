import mysql.connector
__cnx = None

def get_sql_connection():
    global __cnx
    if __cnx == None:
        __cnx = mysql.connector.connect(host="localhost",username="root",
         password="m2@NfTm2", database="grocery_store")
    return __cnx