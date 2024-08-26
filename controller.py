import sqlite3 as sql
import datetime
import os.path


pathDB = "/home/franyober/Documents/Python/sql-project/Database.db"

def createDB():
    conn = sql.connect(pathDB)
    conn.commit()
    conn.close()

def createTable():
    conn = sql.connect(pathDB)
    cursor = conn.cursor() # objeto de la conexión
    cursor.execute(
        """CREATE TABLE Tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name text,
            Date date,
            hours integer
        )"""
    )
    conn.commit() # realizar los cambios
    conn.close()


def insertRow(name, date, hours):
    conn = sql.connect(pathDB)
    cursor = conn.cursor() # objeto de la conexión
    intruccion = f"INSERT INTO Tasks VALUES (NULL,'{name}','{date}','{hours}')"
    cursor.execute(intruccion)
    conn.commit() # realizar los cambios
    conn.close()

def readRows(): 
    conn = sql.connect(pathDB)
    cursor = conn.cursor() # objeto de la conexión
    intruccion = f"SELECT * FROM Tasks"
    cursor.execute(intruccion)
    datos = cursor.fetchall() # se crea una lista de tuplas, cada tupla es un registro
    conn.commit() # realizar los cambios
    conn.close()
    print(datos)  


def search(name,date):
    conn = sql.connect(pathDB)
    cursor = conn.cursor() # objeto de la conexión
    intruccion = f"SELECT * FROM Tasks WHERE Name='{name}' AND Date='{date}'" 
    cursor.execute(intruccion)
    datos = cursor.fetchall() # se crea una lista de tuplas, cada tupla es un registro
    conn.commit() # realizar los cambios
    conn.close()
    return datos


def update(name, date, hours):
    conn = sql.connect(pathDB)
    cursor = conn.cursor() # objeto de la conexión
    intruccion = f"UPDATE Tasks SET hours=hours+{hours} WHERE name='{name}' AND Date='{date}'" 
    cursor.execute(intruccion)
    conn.commit() # realizar los cambios
    conn.close()

def deleteRow(id):
    conn = sql.connect(pathDB)
    cursor = conn.cursor() # objeto de la conexión
    intruccion = f"DELETE FROM Tasks WHERE id='{id}'"
    cursor.execute(intruccion)
    conn.commit() # realizar los cambios
    conn.close()


def extractDays(date):
    conn = sql.connect(pathDB)
    cursor = conn.cursor() # objeto de la conexión
    seis_dias_antes = datetime.datetime.strptime(date, '%d-%m-%Y') - datetime.timedelta(days=6)
    seis_dias_antes_formateada = seis_dias_antes.strftime('%d-%m-%Y')
    intruccion = f"SELECT * FROM Tasks WHERE Date BETWEEN '{seis_dias_antes_formateada}' AND '{date}'"
    cursor.execute(intruccion)
    datos = cursor.fetchall() # se crea una lista de tuplas, cada tupla es un registro
    conn.commit() # realizar los cambios
    conn.close()
    return datos    


if __name__ == "__main__":
    #createDB() #1
    #createTable() #2
    #insertRow("OTRA","15-08-2024",2) #3
    #readRows() #4
    #search(nombre,fecha)#5
    #update(nombre,fecha,2)#6
    print(os.path.exists(pathDB))


