import pyodbc
conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                      "Server=localhost,1433;"
                      "Database=test;"
                      "uid=sa;"
                      "pwd=myPass123word")

query = "INSERT INTO d_comuna values('temuco','23',100)"
query2 = "INSERT INTO d_comuna values('padre las casas','24',200)"
    #print(query)
cursor = conn.cursor()
try:
    cursor.execute(query)
except:
    print("Duplicado")    


try:
    cursor.execute(query2)
except:
    print("Duplicado")  

# Esta es la forma de correrlos, en un try o sino tira error para todo el commit
conn.commit()                          