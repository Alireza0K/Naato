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
    
    def ChooseNaato(self, group):
        
        naato = model.ChooseNaato(group)
        
        return naato
    
    def QandANarator(self,userNickName, groupID, Q, A):
        
        if userNickName == "narrator":
                
            for questions in Q:
                
                question = questions
                    
                qa = model.GetQuestions(groupID, question) 
                
        return qa
    
    def AnswersNarrator(self, question_Hash, answers, check):
        
        model.GetAnswers(question_Hash=question_Hash, answers=answers, check=check)
        
        return True
    
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