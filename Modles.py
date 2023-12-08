import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456789"
)

mycursor = mydb.cursor()

mycursor.execute("SHOW DATABASES")

i = 0

# print(mycursor)

for database in mycursor:
    
    check = False
    
    database = database[0]
    
    if database != "Naato":
        
        check = False
        
    else:
        
        check = True
        
        print("Databese found. \nThat mean you don't need to create Database!!")
        
        break
    
if check != True:
    
    mycursor.execute("CREATE DATABASE Naato")
    
        
        
    

    