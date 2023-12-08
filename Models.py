import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456789"
)

mycursor = mydb.cursor()
    
def DB_Check(Connection):
    
    global check
    
    Connection.execute("SHOW DATABASES")
    
    for database in Connection:
    
        check = False
        
        database = database[0]
        
        if database != "Naato":
            
            check = False
            
        elif database == "Naato":
            
            check = True
            
            break
    
    if check == True:   

        print("Naato DataBase founded.")
        
        mydb._database = "Naato"
    
    elif check != True:
        
        Connection.execute("CREATE DATABASE Naato")
        
        mydb._database = "Naato"
        
        print("Database is Created.")


DB_Check(mycursor)

