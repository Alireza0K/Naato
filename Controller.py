from Models import *

import Handler

class Controller:
    
    def __init__(self, command):
        
        self.command = command
    
    def Start(self, h, G = None):
        
        if h == 0:
        
            group = model.GroupCreation() # First step Create Groups 
            
            model.ScoreScope(group[0])
            
        elif h == 1:
            
            group = G

        return group
    
    def GetUserInformation(self, groupID, name, username):
        
        handler = Handler.ChekUserNameNotEmpty(username)
        
        username = handler
        
        user = model.UserCreation(name, username, groupID) 
        
        return user
    
    def ChangeGroupID(self, userID, newGroup):
        
        result = model.ChangeUserGroup(userHash=userID, newGroup=newGroup)
        
        return result
    
    def GetUserByUName(self, username):
        
        user = model.GetUserByUsername(username)
        
        return user
    
    def GetGroupInformation(self,GroupID):
        
        if GroupID != None and len(GroupID) > 6:
        
            info = model.GetGroupInfo(GroupID)
            
            return info
        
        else:
            
            return None
    
    def GetFactsFromEachUser(self, user, facts):
        
        check = True
        
        for fact in facts:
                
            check = model.GetFacts(user, fact)
        
        return check
    
    def GetUsersId(self, group):
        
        users = model.GetUsersByGroup(groupID=group)
        
        return [users, len(users)]
    
    def ChooseNarrator(self, group):
        
        check = False
        
        gpInfo = model.GetGroupInfo(group)
        
        if gpInfo[0][0][-1] == 1|0:  
            
            check = True
        
            model.ChangeUserNickname(group, "narrator")
        
        return check
    
    def WhoIsTheNarrator(self, groupID):
        
        narrator = None
        
        users = self.GetUsersId(group=groupID)
        
        for user in users[0]:
            
            if user[4] == "narrator":
                
                narrator = user
        
        return narrator
    
    def ChooseNaato(self, group):
        
        naato = model.ChooseNaato(group)
        
        return naato
    
    def CheckNaatoFacts(self, userID):
        
        check = False
        
        userINFO = self.GetUserByUName(username=userID)
        
        groupUSERS = self.GetUsersId(group=userINFO[0][5])
        
        for user in groupUSERS[0]:
            
            if user[4] == "Naato":
                
                facts = self.ShowFacts(naatoID=user[3]) 
                
                if len(facts) == 5:
                    
                    check = True

        return check
    
    def QandANarator(self,userNickName, groupID, Q, A):
        
        if userNickName == "narrator":
                
            for questions in Q:
                
                question = questions
                    
                qa = model.GetQuestions(groupID, question) 
                
        return qa
    
    def AnswersNarrator(self, question_Hash, answers, check):
        
        check = model.GetAnswers(question_Hash=question_Hash, answers=answers, check=check)
        
        return check
    
    def checkQ(self,groupID):
        
        check = model.CheckQuestions(groupID)
        
        return check
    
    def ShowQandA(self, groupID):
        
        QandA = model.ShowQuestionsAndAnswers(groupID=groupID)
        
        return QandA
    
    def CheckedQ(self, quesionID):
        
        model.QuestionChecked(quesionID)
        
    def CheckTheQuestionChecked(self, quesionID):
        
        check = model.CheckTheQuestionChecked(quesionID)
        
        return check
        
    def ShowQuestion(self, groupID):
        
        question = model.ShowQuestion(groupID)
        
        return question
    
    def ShowAnswers(self, questionID):
        
        answers = model.ShowAnswers(questionID=questionID)
        
        return answers
    
    def ScoreScope(self, groupID, command=True):
        
        result = model.AutoScoreScope(groupID=groupID, command=command)
        
        return result
    
    def ShowScore(self, groupID):
        
        score = model.ShowScore(groupID=groupID)
        
        return score
    
    def ShowFacts(self, naatoID):
        
        facts = model.ShowFacts(naatoID)
        
        return facts
    
    def FactCheck(self, factID):
        
        model.FactChecked(factID)
        
    def points(self,userID):
        
        model.Points(userID=userID)
    
    def Terminator(self, userID):
        
        userT = model.UserTerminator(usersID=userID)
        
        return userT
    
    def AllUsersPoints(self, groupID):

        users = model.FetchTheAllMembersOfGroup(groupID)
        
        usersPoints = []
        
        for user in users:

            usersPoints.append([user[2], user[1], user[4], user[6], None])
            
        return usersPoints
    
    def DeleteGroup(self, userID):
        
        groupID = self.GetUserByUName(username=userID)[0][5]
        
        model.ClearTheNickname(groupID=groupID) # reset the Nickname of user
                
        modify = model.DeleteTheGroup(groupID=groupID)
        
        return modify
    
    def EndTheGame(self, groupID, Naato = None):
        
        if Naato != None:
            
            model.NaatoWon(groupID=groupID) # Give all the points to Naato
        
        else:
            
            model.ToghseThePoint(groupID=groupID) # Share points equally with the team members
        
        UsersPoints = self.AllUsersPoints(groupID=groupID)
        
        model.AliveUsers(groupID=groupID) # Set the check to '1'
        
        model.ClearTheNickname(groupID=groupID) # reset the Nickname of all users in the group
        
        model.ClearTheGroup(groupID=groupID) # Reset the group field
        
        model.DeleteTheGroup(groupID=groupID) # Deleting the Group table will cascade to the deletion of score_scope, questions, and answers tables
        
        return UsersPoints