import psycopg2

class DatabaseConnector:
    def __init__(self):
        self.url = ''

    def connect(self):
        conn = psycopg2.connect(self.url)
        return conn