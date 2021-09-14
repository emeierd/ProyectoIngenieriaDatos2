import pyodbc
from datetime import datetime

conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                      "Server=localhost,1433;"
                      "Database=ProyectoIngenieriaDatos2;"
                      "uid=sa;"
                      "pwd=myPass123word")

cursor = conn.cursor() 

fechaInicio = datetime.now()
fechaFin = datetime.now()
print(fechaInicio)
e = "xD"
# query = f"INSERT INTO logs_arriendo values ('Yapo',{fechaInicio},{fechaFin},'Error: ');"
# cursor.execute(query)
cursor.execute("insert into logs_arriendo (fuente,fechaInicio,fechaFin,mensaje) values(?,?,?,?)",
               ("Yapo", fechaInicio, fechaFin, f"Exito: {e}"))
conn.commit()