from dotenv import load_dotenv
from faker import Faker
from faker.providers import lorem
import mysql.connector
import hashlib
import datetime
import random
import os
import time
import inspect
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
        
        checkUser = self.CheckUser(userID=username)
        
        self.TrueStatus(groupID)
        
        if check != True:
            
            return False
        
        elif checkUser == False:
            
            sql = "INSERT INTO `users` (`ID`, `name`, `username`, `user_Hash`, `nickname`, `groupID`, `points`,`check`, `last-active`) VALUES (NULL, %s, %s, %s, %s, %s, %s,1,CURRENT_TIMESTAMP);"
            
            points = 0
            
            userHash = hashlib.md5(str(username).encode()).hexdigest()
            
            values = (name, username, userHash, "", groupID, points)
                
            mycursor.execute(sql, values)
                
            myDB.commit()
            
        elif checkUser == True:
            
            situation = False
            
            self.ChangeUserGroup(userHash=username, newGroup=groupID)
            
            self.ChangeUserLastActive(userHash=username)
        
        return [situation]
    
    def CheckUser(self, userID):
        
        check = False
        
        sql = "SELECT * FROM `users` WHERE username = %s" % (userID)
        
        mycursor.execute(sql)
        
        result = mycursor.fetchall()
        
        if len(result) != 0:
            
            check = True

        return check
        
    def UserTerminator(self, usersID):
        
        try:
        
            sql = "update `users` set `check` = 0 where `username` = %s" % (usersID)
            
            mycursor.execute(sql)
            
            myDB.commit()
            
            return True
            
        except mysql.connector.Error as err:
            
            return err
    
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
        
        value = str(groupID)
        
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
        
        sql = "select * from `users` where groupID = '%s' and `check` = 1" % (groupID)
        
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
        
        check = False
        
        try:

            sql = "update `users` set groupID = '%s' where username = '%s'" % (newGroup, userHash)
            
            mycursor.execute(sql)
            
            myDB.commit()
            
            check = True
            
        except mysql.connector.Error as err:
            
            print(err)
        
        result = self.GetUserByHash(userHash)
        
        return check
    
    def ChangeUserLastActive(self, userHash):
        
        check = False
        
        try:

            sql = "update `users` set `last-active` = CURRENT_TIMESTAMP where username = '%s'" % (userHash)
            
            mycursor.execute(sql)
            
            myDB.commit()
            
            check = True
            
        except mysql.connector.Error as err:
            
            print(err)
        
        result = self.GetUserByHash(userHash)
        
        return check
    
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
        
        check = self.CheckNaato(users=result)
        
        if check:
        
            usersLen = len(result)
            
            choose = random.randint(0, (usersLen - 1))
            
            user = result[choose][0]
            
            naatoHash = result[choose][3]
            
            sql = "update `users` set nickname = '%s' where id = '%s'" % ("Naato", user)
            
            mycursor.execute(sql)
            
            myDB.commit()        

            return naatoHash
        
        else:
            
            return check
    
    def CheckNaato(self, users):
        
        check = True
        
        for user in users:
            
            if user[4] == "Naato":
            
                check = False
        
        print("from -", inspect.stack()[0][3])
        
        return check
    
    def GetFacts(self, userID, fact):
        
        check = self.CheckFacts(userID)
        
        if check:
        
            sql = "INSERT INTO `facts` (`ID`, `userID`, `text`, `check`) VALUES (NULL, '%s', '%s', 1);" % (userID, fact)
            
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
            
            sql = "insert into `questions` (`ID`, `question_Hash`, `groupID`, `text`, `check`) values (NULL, %s, '%s', '%s', 1)" % (question_Hash, groupID, question)
            
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
    
    def QuestionChecked(self, QuestionID):
        
        sql = "update `questions` set `check` = 0 where question_Hash  = '%s'" % (QuestionID)
        
        mycursor.execute(sql)
        
        myDB.commit()
        
        return True
    
    def CheckTheQuestionChecked(self, QuestionID):
        
        check = True
        
        sql = "select * from questions where question_Hash = '%s'" % (QuestionID)
        
        mycursor.execute(sql)
        
        question = mycursor.fetchall()
        
        if question[0][4] == 0:
            
            check = False
            
        return check    
    
    def GetAnswers(self, question_Hash, answers, check):
        
        checkA = self.CheckAnswers(question_Hash)
        
        if checkA[0]:
        
            sql = "insert into `Answers` (`ID`, `questionID`, `text`, `check`) values (NULL, '%s', '%s', '%s')" % (question_Hash, answers, check)

            try:
                mycursor.execute(sql)
                
                myDB.commit()
                
            except mysql.connector.Error as err:
                
                print(err)
        
        return checkA
    
    def CheckAnswers(self, question_Hash):
        
        check = True
        
        lenght = 0
        
        sql = "select * from Answers where questionID = '%s'" % (question_Hash)
        
        mycursor.execute(sql)
        
        answers = mycursor.fetchall()
        
        if len(answers) >= 4:
            
            check = False
            
            lenght = len(answers)
            
        return [check, lenght] 
    
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
    
    def ShowQuestion(self, groupID):
        
        sql = "select * from questions where groupID = '%s' and `check` = 1" % (groupID)
        
        mycursor.execute(sql)
        
        questions = mycursor.fetchall()
        
        return questions[0]
    
    def ShowAnswers(self, questionID):
        
        sql = "select * from `Answers` where questionID = '%s'" % (questionID)
        
        mycursor.execute(sql)
        
        result = mycursor.fetchall()
        
        return result
    
    def ShowFacts(self, NaatoID):
                
        sql = "select * from `facts` where userID = '%s' AND `check` = 1" % (NaatoID)
            
        mycursor.execute(sql)
                        
        facts = mycursor.fetchall()

        return facts
    
    def FactChecked(self,factID):
        
        sql = "update `facts` set `check` = 0 where ID  = '%s'" % (factID)
        
        mycursor.execute(sql)
        
        myDB.commit()
        
        return True
    
    def ScoreScope(self, groupID):
        
        sql = "INSERT INTO `score_scope` (`ID`, `length`, `groupID`) VALUES (NULL, '40', '%s');" % (groupID)
        
        mycursor.execute(sql)
        
        myDB.commit()
        
        return True
    
    def AutoScoreScope(self, groupID, command = None):
        
        check = None
        
        sql = "select * from `score_scope` where groupID = '%s'" % (groupID)
        
        mycursor.execute(sql)
        
        result = mycursor.fetchall()
        
        score = result[0][1]
        
        if command == True:
            
            score = self.IncreaseScore(groupID, score)
            
            check = True
            
        if command == False:
            
            score = self.DecreaseScore(groupID, score)
            
            check = False
        
        return [score, check]
    
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

    def ShowScore(self, groupID):
        
        sql = "select * from `score_scope` where groupID = '%s'" % (groupID)
        
        mycursor.execute(sql)
        
        result = mycursor.fetchall()
        
        return result
    
    def CycleSeter(self, groupID, naatoID):
        
        self.Cycle(groupID, naatoID)
        
        return True
    
    def Points(self, userID):
        
        user = self.GetUserByUsername(userID)
        
        point = user[0][6]
        
        sql = "update `users` set points = '%s' where username = '%s'" % (point + 5, userID)
        
        mycursor.execute(sql)
        
        myDB.commit()
        
    def FetchTheAllMembersOfGroup(self, groupID):
        
        sql = "select * from `users` where groupID = '%s'" % (groupID)
        
        mycursor.execute(sql)
        
        users = mycursor.fetchall()
        
        return users
    
    def AliveUsers(self, groupID): # This Must be Complete
        
        try:
        
            sql = "update `users` set `check` = 1 where `groupID` = '%s'" % (groupID)
            
            mycursor.execute(sql)
            
            myDB.commit()
            
            return True
            
        except mysql.connector.Error as err:
            
            return err
        
    def ClearTheNickname(self, groupID): # also This Must be Complete
        
        sql = "update `users` set `nickname` = '' where `groupID` = '%s'" % (groupID)
        
        mycursor.execute(sql)
        
        myDB.commit()

    def ClearTheGroup(self, groupID):
        
        users = self.FetchTheAllMembersOfGroup(groupID=groupID)
        
        for userID in users:
        
            sql = "UPDATE `users` SET `groupID` = NULL where username = '%s'" % (userID[2])
            
            mycursor.execute(sql)
            
            myDB.commit()
            
    def DeleteTheGroup(self, groupID):
        
        sql = "DELETE FROM `groups` WHERE group_Hash = '%s';" % (groupID)
        
        mycursor.execute(sql)
            
        myDB.commit()     
            
    def ToghseThePoint(self, groupID):

        users = self.FetchTheAllMembersOfGroup(groupID=groupID)
        
        pointScope = self.ShowScore(groupID=groupID)
        
        Toghse = round(pointScope[0][1] / len(users))
        
        for userID in users:
            
            sql = "update `users` set points = '%s' where username = '%s'" % (userID[6] + Toghse, userID[2])
            
            mycursor.execute(sql)
            
            myDB.commit() 
            
    def NaatoWon(self, groupID):
    
        users = self.FetchTheAllMembersOfGroup(groupID=groupID)
        
        pointScope = self.ShowScore(groupID=groupID)
        
        for user in users:
            
            if user[4] == "Naato":

                sql = "update `users` set points = '%s' where username = '%s'" % (user[6] + pointScope[0][1], user[2])
                
                mycursor.execute(sql)
                
                myDB.commit() 
                
model = Models()

fake = Faker()
