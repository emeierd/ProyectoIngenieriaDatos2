import pyodbc

conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                      "Server=localhost,1433;"
                      "Database=ProyectoIngenieriaDatos2;"
                      "uid=sa;"
                      "pwd=myPass123word")

cursor = conn.cursor()   

for i in range(5):
    año = 2021 + i
    query1 = f"INSERT INTO d_mes values (1,'Enero',{año},1);"
    query2 = f"INSERT INTO d_mes values (2,'Febrero',{año},1);"
    query3 = f"INSERT INTO d_mes values (3,'Marzo',{año},1);"
    query4 = f"INSERT INTO d_mes values (4,'Abril',{año},2);"
    query5 = f"INSERT INTO d_mes values (5,'Mayo',{año},2);"
    query6 = f"INSERT INTO d_mes values (6,'Junio',{año},2);"
    query7 = f"INSERT INTO d_mes values (7,'Julio',{año},3);"
    query8 = f"INSERT INTO d_mes values (8,'Agosto',{año},3);"
    query9 = f"INSERT INTO d_mes values (9,'Septiembre',{año},3);"
    query10 = f"INSERT INTO d_mes values (10,'Octubre',{año},4);"
    query11 = f"INSERT INTO d_mes values (11,'Noviembre',{año},4);"
    query12 = f"INSERT INTO d_mes values (12,'Diciembre',{año},4);"

    cursor.execute(query1)
    cursor.execute(query2)
    cursor.execute(query3)
    cursor.execute(query4)
    cursor.execute(query5)
    cursor.execute(query6)
    cursor.execute(query7)
    cursor.execute(query8)
    cursor.execute(query9)
    cursor.execute(query10)
    cursor.execute(query11)
    cursor.execute(query12)

conn.commit()