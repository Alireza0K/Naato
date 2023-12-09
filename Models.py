from dotenv import load_dotenv
from faker import Faker
import mysql.connector
import hashlib
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

global mycursor 

mycursor = myDB.cursor()

class Models:
    
    def __init__(self, Connection):
        
        self.Connection = Connection

    def TablesValidation(self):
        
        check = False
        
        mycursor.execute("show tables")
        
        result = mycursor.fetchall()
        
        counter = 0
        
        for table in result:
            
            counter += 1
            
        if counter != 6:
            
            check = False
            
            print("Validation Error!!, please install DataBase again.")
        
        elif counter == 6:
            
            check = True
            
        return check
    
    def GroupCreation(self):
        
        faker = Faker()
        
        groupName = faker.name()
        
        hashValue = hashlib.md5(groupName.encode()).hexdigest()
        
        sql = "INSERT INTO `groups` (`ID`, `group_Hash`, `group_name`) VALUES (NULL, %s, %s);"
        
        values = (hashValue, groupName)     
        
        mycursor.execute(sql, values)   
        
        myDB.commit()
        
        return mycursor

model = Models(mycursor)