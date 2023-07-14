import psycopg2

class DatabaseConnector:
    def __init__(self):
        self.url = 'postgres://root:B6sFCAbNTvrgqvzna8FCXFMOHz2KIkid@dpg-ci6jam18g3nfucbk7b10-a.singapore-postgres.render.com/vahdb'

    def connect(self):
        conn = psycopg2.connect(self.url)
        return conn