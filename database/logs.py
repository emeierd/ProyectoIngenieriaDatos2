import pyodbc

conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                      "Server=localhost,1433;"
                      "Database=ProyectoIngenieriaDatos2;"
                      "uid=sa;"
                      "pwd=myPass123word")

cursor = conn.cursor()   

query1 = "CREATE TABLE logs_arriendo (id int IDENTITY(1,1) PRIMARY KEY, fuente varchar(50), fechaInicio datetime, fechaFin datetime, mensaje varchar(255));"
query2 = "CREATE TABLE logs_consulta (id int IDENTITY(1,1) PRIMARY KEY, fuente varchar(50), fechaInicio datetime, fechaFin datetime, mensaje varchar(255));"

cursor.execute(query1)
cursor.execute(query2)

conn.commit()