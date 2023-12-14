from Models import *

class Controller:
    
    def __init__(self, command):
        
        self.command = command
        
        self.control(self.command)
    
    def Start(self):
        
        group = model.GroupCreation()
        
        for i in range(0,6):
            
            name = input("name: ")
            
            name = fake.name()
            
            username = input("username: ")
            
            username = fake.user_name()
        
            model.UserCreation(name, username, group)
            
            
            
        model.ChangeUserNickname(group, "narrator")
        
        print("first user that enter his name is Narrator")
        
        users = model.GetUsersByGroup(group)
        
        for user in users:
            
            for count in range(0,5):
            
                fact = input("enter the fact: ")
                
                fact = fake.paragraph()
                
                model.GetFacts(user[3], fact)
        
        return 
    
    def control(self, command):
        
        if command == "/start":
            
            self.Start()
        
        return True
    
control = Controller("/start")