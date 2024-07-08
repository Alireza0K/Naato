import numpy as np

from faker import Faker

fake = Faker()

def ChekUserNameNotEmpty(username):
    
    if username == None:
        
        username = fake.user_name()
        
        print(username)
        
    else:
        
        username = username
        
    return username