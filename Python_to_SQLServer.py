# https://www.youtube.com/watch?v=Vm2fHhP4SVE
import pyodbc

connection_string = 'DRIVER={SQL Server}; SERVER=HQ-GIIOKUS\SQLEXPRESS; Database=PersonalLibrary; UID=HQ-GIIOKUS\Magic; PWD=NULL;'
connex = pyodbc.connect(connection_string)

query = 'This is where an SQL query goes.'

cursor = connex.cursor()
cursor.execute(query)

data = cursor.fetchall()

# print data here

connex.close()
