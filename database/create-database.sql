CREATE DATABASE ProyectoIngenieriaDatos2;
GO
USE ProyectoIngenieriaDatos2;
GO
CREATE TABLE d_comuna (comuna_id varchar(50) PRIMARY KEY, sector varchar(50), arriendo_promedio float);
GO
CREATE TABLE d_fecha (fecha date PRIMARY KEY, mes_id int NOT NULL, año int NOT NULL);
GO
CREATE TABLE d_mes (mes_id int IDENTITY(1,1) PRIMARY KEY, numero int NOT NULL, nombre varchar(50), año int NOT NULL, cuatrimestre int NOT NULL);
GO
CREATE TABLE d_gastos (gasto_id int IDENTITY(1,1) PRIMARY KEY, nombre varchar(50), valor int NOT NULL);
GO
CREATE TABLE d_departamento (departamento_id int PRIMARY KEY, dormitorios int NOT NULL, baños int NOT NULL, estacionamiento varchar(2), bodega varchar(2));
GO
CREATE TABLE f_arriendo (arriendo_id int IDENTITY(1,1) PRIMARY KEY, url varchar(255) NOT NULL UNIQUE, comuna_id varchar(50) NOT NULL, valor int NOT NULL, fecha_id date NOT NULL, departamento_id int NOT NULL);
GO
CREATE TABLE f_consulta (consulta_id int IDENTITY(1,1) PRIMARY KEY, fecha_id date NOT NULL, comuna_id int NOT NULL, departamento_id INT NOT NULL, valor int NOT NULL, gasto_1 int, gasto_2 int, gasto_3 int, gasto_4 int, gasto_5 int);
GO
