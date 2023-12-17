from dotenv import load_dotenv
from faker import Faker
from faker.providers import lorem
import mysql.connector
import hashlib
import datetime
import random
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
        
        self.TablesValidation()

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
        
        sql = "INSERT INTO `groups` (`ID`, `group_Hash`, `group_name`, `group_question_Hash`, `open`) VALUES (NULL, %s, %s, %s, '1');"
        
        values = (hashValue, groupName, hashValue)     
        
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
        
        return userHash
    
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
        
        return (firstUser[1], "is", nickname)
    
    def ChooseNaato(self, groupID):
        
        sql_select = "SELECT * FROM `users` WHERE groupID = '%s' and nickname <> 'narrator';" % (groupID)
        
        mycursor.execute(sql_select)
        
        result = mycursor.fetchall()
        
        usersLen = len(result)
        
        choose = random.randint(0, (usersLen - 1))
        
        user = result[choose][0]
        
        sql = "update `users` set nickname = '%s' where id = %s" % ("Naato", user)
        
        mycursor.execute(sql)
        
        myDB.commit()        

        return user
    
    def GetFacts(self, userID, fact):
        
        sql = "INSERT INTO `facts` (`ID`, `userID`, `text`) VALUES (NULL, '%s', '%s');" % (userID, fact)
        
        mycursor.execute(sql)
        
        myDB.commit()
        
        return True
    
    def GetQuestions(self, groupID, question):
        
        question_Hash = hash(question + str(datetime.datetime.now()))
        
        sql = "insert into `questions` (`ID`, `question_Hash`, `groupID`, `text`) values (NULL, %s, '%s', '%s')" % (question_Hash, groupID, question)
        
        mycursor.execute(sql)
        
        myDB.commit()
        
        for count in range(0,4):
            
            answer = input(str(count+1) + ". enter answer: ")
        
            answer = fake.sentence()
            
            check = input("if its true enter 1 or not 0:")
            
            check = 0
            
            if count == 3:
                
                check = 1
            
            self.GetAnswers(question_Hash, answer, check)
        
        return True
    
    def GetAnswers(self, question_Hash, answers, check):
        
        sql = "insert into `Answers` (`ID`, `questionID`, `text`, `check`) values (NULL, '%s', '%s', '%s')" % (question_Hash, answers, check)
        
        mycursor.execute(sql)
        
        myDB.commit()
        
        return True
    
    def ShowQuestionsAndAnswers(self, groupID):
        
        sql = "select * from questions where groupID = '%s'" % (groupID)
        
        mycursor.execute(sql)
        
        questions = mycursor.fetchall()
        
        for question in questions:
            
            print("\nQuestion is: ▼")
            
            print(question[3], "\n")
            
            answers = self.ShowAnswers(question[1])
            
            print("Answer is: ▼")
            
            for answer in answers:
                if answer[3] == 1:
                    
                    print(answer[2], "! ✅ !", "\n")
                    
                else:
                    
                    print(answer[2], "\n")
                    
        
        return True
    
    def ShowAnswers(self, questionID):
        
        sql = "select * from `Answers` where questionID = '%s'" % (questionID)
        
        mycursor.execute(sql)
        
        result = mycursor.fetchall()
        
        return result
    
    def ScoreScope(self, groupID, command = None):
        
        sql = "select * from `score_scope` where groupID = '%s'" % (groupID)
        
        mycursor.execute(sql)
        
        result = mycursor.fetchall()
        
        score = result[0][1]
        
        if command == True:
            
            score = self.IncreaseScore(groupID, score)
            
        if command == False:
            
            score = self.DecreaseScore(groupID, score)
        
        return score
    
    def IncreaseScore(self, groupID, score):
        
        sql = "update `score_scope` set length = '%s' where groupID = '%s'" % (score + 5,groupID)
        
        mycursor.execute(sql)
        
        myDB.commit()
        
        return score
    
    def DecreaseScore(self, groupID, score):
        
        sql = "update `score_scope` set length = '%s' where groupID = '%s'" % (score - 5,groupID)
        
        mycursor.execute(sql)
        
        myDB.commit()
        
        return score
        
model = Models()

fake = Faker()