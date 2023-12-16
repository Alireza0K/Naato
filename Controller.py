from Models import *

class Controller:
    
    def __init__(self, command):
        
        self.command = command
        
        self.control(self.command)
    
    def Start(self):
        
        group = model.GroupCreation() # First step Create Groups 
        
        for i in range(0,6):
            
            user = self.GetUserInformation(group) # Get name and username for add theos to group 
            
            self.GetFactsFromEachUser(user) # get userID and fact from that user to add a fact to facts tabel
            
        model.ChangeUserNickname(group, "narrator") # choose a narrator
            
        print("first user that enter his name is Narrator")

        return
    
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