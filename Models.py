from dotenv import load_dotenv
from faker import Faker
from faker.providers import lorem
import mysql.connector
import hashlib
import datetime
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
    
    def __init__(self):
        
        self
        
        pass

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
        
        nowDateTime = datetime.datetime.now() 
        
        hashValue = hashlib.md5((groupName + str(nowDateTime)).encode()).hexdigest()
        
        sql = "INSERT INTO `groups` (`ID`, `group_Hash`, `group_name`, `open`) VALUES (NULL, %s, %s, 1);"
        
        values = (hashValue, groupName)     
        
        mycursor.execute(sql, values)   
        
        myDB.commit()
        
        return hashValue
    
    def UserCreation(self, name, username, groupID):
        
        check = self.GetGroupStatus(groupID)
        
        self.TrueStatus(groupID)
        
        if check != True:
            
            return False
        
        sql = "INSERT INTO `users` (`ID`, `name`, `username`, `user_Hash`, `nickname`, `groupID`, `points`) VALUES (NULL, %s, %s, %s, %s, %s, %s);"
        
        points = 15
        
        userHash = hashlib.md5(username.encode()).hexdigest()
        
        values = (name, username, userHash, "", groupID, points)
        
        mycursor.execute(sql, values)
        
        myDB.commit()
        
        return True
    
    def GetGroupStatus(self, groupID):
        
        check = False
        
        value = (groupID)
        
        sql = ("SELECT open FROM `groups` WHERE group_Hash = '%s'" % (value))
        
        mycursor.execute(sql)
        
        result = mycursor.fetchall()
        
        result = [i[0] for i in result]
        
        if result[0] != 1:
            
            check = False
        
        if result[0] == 1:
            
            check = True
        
        return check

    def TrueStatus(self, groupID):
        
        sql = "select name from users where groupID = '%s'" % (groupID)
        
        mycursor.execute(sql)
        
        result = mycursor.fetchall()
        
        lengthOfUsers = len(result)
        
        if lengthOfUsers >= 5:
            
            sql = ("update `groups` set open = 0 where group_Hash = '%s'" % (groupID))
            
            mycursor.execute(sql)
            
            myDB.commit()
        
        return result
    
    def GetUsersByGroup(self, groupID):
        
        sql = "select * from `users` where groupID = '%s'" % (groupID)
        
        mycursor.execute(sql)
        
        result = mycursor.fetchall()
        
        return result
    
    def ChangeUserNickname(self, groupID, nickname):
        
        result = self.GetUsersByGroup(groupID)
        
        firstUser = result[0]
        
        sql = "update `users` set nickname = '%s' where id = %s" % (nickname, firstUser[0])
        
        mycursor.execute(sql)
        
        myDB.commit()
        
        return (firstUser[1], "is narrator")
    
    def GetFacts(self, userID, fact):
        
        sql = "INSERT INTO `facts` (`ID`, `userID`, `text`) VALUES (NULL, '%s', '%s');" % (userID, fact)
        
        mycursor.execute(sql)
        
        myDB.commit()
        
        return True
        
model = Models()