from dotenv import load_dotenv
from faker import Faker
from faker.providers import lorem
import mysql.connector
import hashlib
import datetime
import random
import os
import time

import mysql.connector.errorcode

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
        
        return [hashValue, groupName]
    
    def UserCreation(self, name, username, groupID):
        
        check = self.GetGroupStatus(groupID)
        
        situation = True
        
        self.TrueStatus(groupID)
        
        if check != True:
            
            return False
        
        sql = "INSERT INTO `users` (`ID`, `name`, `username`, `user_Hash`, `nickname`, `groupID`, `points`) VALUES (NULL, %s, %s, %s, %s, %s, %s);"
        
        points = 15
        
        userHash = hashlib.md5(username.encode()).hexdigest()
        
        values = (name, username, userHash, "", groupID, points)
        
        try:
            
            mycursor.execute(sql, values)
            
            myDB.commit()
            
        except mysql.connector.Error as err:
            
            print(err)
            
            if err.errno == mysql.connector.errorcode.ER_DUP_ENTRY:
                
                situation = False
                
                change = self.ChangeUserGroup(userHash, groupID)
        
        return [userHash, situation]
    
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

    def GetGroupInfo(self, groupID):
        
        check = False
        
        value = (groupID)
        
        sql = ("SELECT * FROM `groups` WHERE group_Hash = '%s'" % (value))
        
        mycursor.execute(sql)
        
        result = mycursor.fetchall()
        
        return [result]

    def TrueStatus(self, groupID):
        
        sql = "select name from users where groupID = '%s'" % (groupID)
        
        mycursor.execute(sql)
        
        result = mycursor.fetchall()
        
        lengthOfUsers = len(result)
        
        if lengthOfUsers >= 6:
            
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
        
        return [firstUser[1], "is", nickname]
    
    def ChangeUserGroup(self, userHash, newGroup):
        
        try:

            sql = "update `users` set groupID = '%s' where user_Hash = '%s'" % (newGroup, userHash)
            
            mycursor.execute(sql)
            
            myDB.commit()
            
        except mysql.connector.Error as err:
            
            print(err)
        
        result = self.GetUserByHash(userHash)
        
        return result
    
    def GetUserByHash(self, userHash):
        
        sql = "select * from `users` where user_Hash = '%s'" % (userHash)
        
        mycursor.execute(sql)
        
        result = mycursor.fetchall()
        
        return result
    
    def GetUserByUsername(self, username):
        
        sql = "select * from `users` where username = '%s'" % (username)
        
        mycursor.execute(sql)
        
        result = mycursor.fetchall()
        
        return result
    
    def ChooseNaato(self, groupID):
        
        sql_select = "SELECT * FROM `users` WHERE groupID = '%s' and nickname <> 'narrator';" % (groupID)
        
        mycursor.execute(sql_select)
        
        result = mycursor.fetchall()
        
        self.CheckNaato(users=result)
        
        usersLen = len(result)
        
        choose = random.randint(0, (usersLen - 1))
        
        user = result[choose][0]
        
        naatoHash = result[choose][3]
        
        sql = "update `users` set nickname = '%s' where id = '%s'" % ("Naato", user)
        
        mycursor.execute(sql)
        
        myDB.commit()        

        return naatoHash
    
    def CheckNaato(self, users):
        
        # for user in users:
            
        #     print(user)
        
        return True
    
    def GetFacts(self, userID, fact):
        
        check = self.CheckFacts(userID)
        
        if check:
        
            sql = "INSERT INTO `facts` (`ID`, `userID`, `text`) VALUES (NULL, '%s', '%s');" % (userID, fact)
            
            mycursor.execute(sql)
            
            myDB.commit()
            
        return check
    
    def CheckFacts(self,userID):
        
        check = True
        
        sql = "select * from facts where userID = '%s'" % (userID)
        
        try:
        
            mycursor.execute(sql)
            
            facts = mycursor.fetchall()
            
        except mysql.connector.Error as err:
            
            print(err)
        
        if len(facts) >= 5:
            
            check = False
            
        return check 
    
    def GetQuestions(self, groupID, question):
        
        check = self.CheckQuestions(groupID=groupID)
        
        question_Hash = None
        
        if check:
            
            question_Hash = hash(question + str(datetime.datetime.now()))
            
            sql = "insert into `questions` (`ID`, `question_Hash`, `groupID`, `text`) values (NULL, %s, '%s', '%s')" % (question_Hash, groupID, question)
            
            mycursor.execute(sql)
            
            myDB.commit()
        
        return [check, question_Hash]
    
    def CheckQuestions(self, groupID):
        
        check = True
        
        sql = "select * from questions where groupID = '%s'" % (groupID)
        
        mycursor.execute(sql)
        
        questions = mycursor.fetchall()
        
        if len(questions) >= 4:
            
            check = False
            
        return check 
    
    def GetAnswers(self, question_Hash, answers, check):
        
        checkA = self.CheckAnswers(question_Hash)
        
        if checkA:
        
            sql = "insert into `Answers` (`ID`, `questionID`, `text`, `check`) values (NULL, '%s', '%s', '%s')" % (question_Hash, answers, check)

            try:
                mycursor.execute(sql)
                
                myDB.commit()
                
            except mysql.connector.Error as err:
                
                print(err)
        
        return checkA
    
    def CheckAnswers(self, question_Hash):
        
        check = True
        
        sql = "select * from Answers where questionID = '%s'" % (question_Hash)
        
        mycursor.execute(sql)
        
        answers = mycursor.fetchall()
        
        if len(answers) >= 4:
            
            check = False
            
        return check 
    
    def ShowQuestionsAndAnswers(self, groupID):
        
        questionsList = []
        
        QandAList = []
        
        sql = "select * from questions where groupID = '%s'" % (groupID)
        
        mycursor.execute(sql)
        
        questions = mycursor.fetchall()
        
        for question in questions:
            
            answersList = []

            questionsList.append(question[3]) 
            
            answers = self.ShowAnswers(question[1])

            for counter in range(0,len(answers)):

                answersList.append(answers[counter][2::])
                
            QandAList.append([question[3],answersList])

        return QandAList
    
    def ShowAnswers(self, questionID):
        
        sql = "select * from `Answers` where questionID = '%s'" % (questionID)
        
        mycursor.execute(sql)
        
        result = mycursor.fetchall()
        
        return result
    
    def Cycle(self, groupID, NaatoID):
        
        self.ScoreScope(groupID)
        
        sql = "select * from questions where groupID = '%s'" % (groupID)
        
        mycursor.execute(sql)
        
        questions = mycursor.fetchall()
        
        cycleCounter = 0
        
        Counter = 0
        
        for question in questions:
            
            cycleCounter += 1
            
            print("\nQuestion is: ▼")
            
            print(question[3], "\n")
            
            answers = self.ShowAnswers(question[1])
            
            count = 0
            
            print("Answer is: ▼")
            
            for answer in answers:
                
                count += 1
                    
                print(str(count)+".", answer[2], "\n")
                    
            userAnswer = int(input("Choose the correct answer: "))
            
            os.system("clear")
            
            if answers[userAnswer-1][3] == 1:
                
                print("Congratulation, You Select Correct Answer")
                
                self.AutoScoreScope(groupID, True)
                
            elif answers[userAnswer-1][3] != 1:
                
                print("You Select Wrong Answer!!!")
                
                self.AutoScoreScope(groupID, False)
                
            if cycleCounter == 2:
                
                self.ShowFacts(Counter, NaatoID)
            
        return True
    
    def ShowFacts(self, Counter, NaatoID):
        
        Counter += 1
                
        print("|****** (Fact) ******|")
                
        sql = "select * from `facts` where userID = '%s'" % (NaatoID)
            
        mycursor.execute(sql)
                        
        facts = mycursor.fetchall()
                        
        print(str(Counter)+".", facts[Counter][2])
                
        time.sleep(5)
                
        os.system("clear")
        
        return facts[Counter][2]
    
    def ScoreScope(self, groupID):
        
        sql = "INSERT INTO `score_scope` (`ID`, `length`, `groupID`) VALUES (NULL, '40', '%s');" % (groupID)
        
        mycursor.execute(sql)
        
        myDB.commit()
        
        return
    
    def AutoScoreScope(self, groupID, command = None):
        
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
    
    def CycleSeter(self, groupID, naatoID):
        
        self.Cycle(groupID, naatoID)
        
        return True
        
model = Models()

fake = Faker()
