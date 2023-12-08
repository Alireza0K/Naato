from dotenv import load_dotenv
import mysql.connector
import os

load_dotenv()

DB_info = {
    "host": os.getenv("host"),
    "user": os.getenv("user"),
    "password": os.getenv("password"),
    "database": os.getenv("database")
}

myDB = mysql.connector.connect(
    host = DB_info["host"],
    user = DB_info["user"],
    password = DB_info["password"],
    database = DB_info["database"]
)

mycursor = myDB.cursor()

def TablesValidation(Connection):
    
    check = False
    
    Connection.execute("show tables")
    
    result = Connection.fetchall()
    
    counter = 0
    
    for table in result:
        
        counter += 1
        
    if counter != 6:
        
        check = False
        
        print("Validation Error!!, please install DataBase again.")
    
    elif counter == 6:
        
        check = True
        
    return check
        

TablesValidation(mycursor)