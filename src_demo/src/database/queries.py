
class Queries:
    def __init__(self, connector):
        self.connector = connector

    def getUserByEmail(self, email):
        query = f"select * from employee where email='{email}'"
        cursor = self.connector.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return data
    
    def insertUser(self, email, password, fullName):
        query = f"insert into employee (email, password, fullname) values ('{email}', '{password}', '{fullName}');"
        cursor = self.connector.cursor()
        cursor.execute(query)
        cursor.close()
        
    
    # def checkUserEmailAndPassword(self, email, raw_password):
        