import _mysql_connector
cnx=_mysql_connector.connect(user="root", 
                             password="",
                             host="127.0.0.1",
                             databases="turnos_medicos")

#generar las consultas
cursor = cnx.cursor()
consulta= "SELECT * FROM contacto;"
cursor.execute(consulta)#ejecuta la consulta
datos = cursor.fetchall() #trae todo
print(datos)

#generar las consultas
cursor = cnx.cursor()
consulta= "SELECT * FROM profesionales;"
cursor.execute(consulta)#ejecuta la consulta
datos = cursor.fetchall() #trae todo
print(datos)

#generar las consultas
cursor = cnx.cursor()
consulta= "SELECT * FROM usuarios;"
cursor.execute(consulta)#ejecuta la consulta
datos = cursor.fetchall() #trae todo
print(datos)

#generar las consultas
cursor = cnx.cursor()
consulta= "SELECT * FROM sedes;"
cursor.execute(consulta)#ejecuta la consulta
datos = cursor.fetchall() #trae todo
print(datos)

#generar las consultas
cursor = cnx.cursor()
consulta= "SELECT * FROM turnos;"
cursor.execute(consulta)#ejecuta la consulta
datos = cursor.fetchall() #trae todo
print(datos)

cnx.close()