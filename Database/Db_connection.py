import mysql.connector
from mysql.connector import Error
from config import Config

class DatabaseConnection:
    def __init__(self):
        self.host = Config.MYSQL_HOST
        self.user = Config.MYSQL_USER
        self.password = Config.MYSQL_PASSWORD
        self.database = Config.MYSQL_DATABASE
        self.port = Config.MYSQL_PORT
        self.connection = None
    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
            if self.connection.is_connected():
                print("✅ Successfully connected to MySQL database!")
                return self.connection
        except Error as e:
            print(f"❌ Error connecting to MySQL: {e}")
            return None
    
    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed.")
