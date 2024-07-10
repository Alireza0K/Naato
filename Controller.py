from Models import *

import Handler

class Controller:
    
    def __init__(self, command):
        
        self.command = command
    
    def Start(self, h, G = None):
        
        if h == 0:
        
            group = model.GroupCreation() # First step Create Groups 
            
        elif h == 1:
            
            group = G
        
        # for i in range(0,6):
            
        #     user = self.GetUserInformation(group[0]) # Get name and username for add theos to group 
            
        # model.ChangeUserNickname(group[0], "narrator") # choose a narrator
            
        # print("first user that enter his name is Narrator")
        
        # naato = model.ChooseNaato(group[0])
        
        # users = model.GetUsersByGroup(group[0])
        
        # self.GameFirstSection(users, group) # this is the first section of the game for *Choosing* Naato and *Narrator*
        
        # model.CycleSeter(group, naato)
        
        return group
    
    def GetUserInformation(self, groupID, name, username):
        
        handler = Handler.ChekUserNameNotEmpty(username)
        
        username = handler
        
        user = model.UserCreation(name, username, groupID) 
        
        return user
    
    def GetGroupInformation(self,GroupID):
        
        print(len(GroupID))
        
        if GroupID != None and len(GroupID) > 6:
        
            info = model.GetGroupInfo(GroupID)
            
            print("from Controller")
            
            return info
        
        else:
            
            print(GroupID)
            
            return None
    
    def GetFactsFromEachUser(self, user):
        
        for x in range(0,5):
        
            fact = input(str(x+1) + ". enter the fact: ")
                        
            fact = fake.paragraph()
                
            model.GetFacts(user, fact)
        
        return True
    
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
    
    def GameFirstSection(self, users, group):
        
        for user in users:
            
            if user[4] == "narrator":
                
                print("please Write the questions and answers.")
                
                for x in range(0,4):
                
                    question = input(str(x+1)+". question: ")
                    
                    question = fake.sentence()
                    
                    model.GetQuestions(group, question) # this is for get questions from Narrator and put it in questions tabel
            
            if user[4] != "narrator":
                
                print(user[1], "Come in and write your facts!!")
            
                self.GetFactsFromEachUser(user[3]) # get userID and fact from each user to add a fact to facts tabel
            
            if user[4] == "Naato":
                
                print("You are Naato, attention!!\nPay close attention to the questions and answers and keep them in your mind")
                
                model.ShowQuestionsAndAnswers(group)
                
                time.sleep(5) # if you want make the game for Naato easier increase this
            
            time.sleep(2)
            
            os.system("clear")
        
        return True