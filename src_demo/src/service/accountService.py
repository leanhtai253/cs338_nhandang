from database.connector import DatabaseConnector
from database.queries import Queries
from model.modelService import ModelService

mydb = DatabaseConnector()
conn = mydb.connect()
query = Queries(conn)
conn.autocommit = True

class AccountService:

    def insertUser(email, password, fullName):
        return query.insertUser(email, password, fullName)

    def checkEmailExist(email):
        userArr = query.getUserByEmail(email)
        return len(userArr) > 0
    
    def authenticateUser(email, password, audio):
        userArr = query.getUserByEmail(email)
        if len(userArr) < 1:
            return 401, "Email does not exist."
        user = userArr[0]
        userPwd = user[2]
        if (password != userPwd):
            return 401, "Invalid credentials."
        return 200, "Success"

