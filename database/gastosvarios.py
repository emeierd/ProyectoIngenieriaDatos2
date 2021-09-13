import pyodbc

conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                      "Server=localhost,1433;"
                      "Database=ProyectoIngenieriaDatos2;"
                      "uid=sa;"
                      "pwd=myPass123word")

cursor = conn.cursor()   

query1 = "INSERT INTO d_gastos values ('Gastos Comunes',50000);"
query2 = "INSERT INTO d_gastos values ('Servicios Básicos',50000);"
query3 = "INSERT INTO d_gastos values ('Transporte',40000);"
query4 = "INSERT INTO d_gastos values ('Comida',300000);"
query5 = "INSERT INTO d_gastos values ('Internet',15000);"
query6 = "INSERT INTO d_gastos values ('Telefonía',15000);"
query7 = "INSERT INTO d_gastos values ('TV Cable',20000);"

cursor.execute(query1)
cursor.execute(query2)
cursor.execute(query3)
cursor.execute(query4)
cursor.execute(query5)
cursor.execute(query6)
cursor.execute(query7)

conn.commit()