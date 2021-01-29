import datetime
import mysql.connector

class ConnectionMySQL:
  
  def __init__(self):
    self.connect()

  def connect(self):
    self.cnx = mysql.connector.connect(user='root', 
                                password='apple2020', 
                                database='lab5_EstateAgent_db', 
                                auth_plugin='mysql_native_password')
    self.cursor = self.cnx.cursor()

  def close(self):
    self.cursor.close()
    self.cnx.close()
    

  
connection = ConnectionMySQL()

cursor = connection.cursor

query = ("select fname, salary from staff")

cursor.execute(query)

for (fname, salary) in cursor:
  print("name; {} - salary: {}  ".format(fname, salary))

connection.close()