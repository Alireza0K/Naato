from Models import *
import time

class Controller:
    
    def __init__(self, command):
        
        self.command = command
        
        self.control(self.command)
    
    def Start(self):
        
        group = model.GroupCreation() # First step Create Groups 
        
        for i in range(0,6):
            
            user = self.GetUserInformation(group) # Get name and username for add theos to group 
            
        model.ChangeUserNickname(group, "narrator") # choose a narrator
            
        print("first user that enter his name is Narrator")
        
        naato = model.ChooseNaato(group)
        
        users = model.GetUsersByGroup(group)
        
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
                
                time.sleep(3) # if you want make the game for Naato easier increase this
            
            time.sleep(2)
            
            os.system("clear")
        
        return True
    
    def GetUserInformation(self, groupID):
        
        name = input("name: ") 
            
        name = fake.name()
            
        username = input("username: ")
            
        username = fake.user_name()
        
        user = model.UserCreation(name, username, groupID) 
        
        return user
    
    def GetFactsFromEachUser(self, user):
        
        for x in range(0,5):
        
            fact = input(str(x+1) + ". enter the fact: ")
                        
            fact = fake.paragraph()
                
            model.GetFacts(user, fact)
        
        return True
    
    def control(self, command):
        
        if command == "/start":
            
            self.Start()
        
        return True
    
control = Controller("/start")