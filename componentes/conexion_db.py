import mysql.connector

# Pasos:
# 1)Conecto, 2) Consulto, 3) Desempaqueto y 4)Muestro lo que ejecuto

config_dev = {
    'user': 'root', 
    'password': '',
    'host': '127.0.0.1',
    'database':'turnos_medicos'
}

config_prod = {} # proximamente, despliegue

conexion = mysql.connector.connect(**config_dev)

# Establezco la conexión
# cnx = mysql.connector.connect(user='root', 
#                               password='',
#                               host='127.0.0.1',
#                               database='turnos_medicos')
# Generar las consultas
# me tengo que crear un cursos que va a venir de la conexion
#cursor = cnx.cursor() # devuelve tuplas
# cursor = cnx.cursor(dictionary=True) # Me devuelve una lista de diccionarios key=columna value=valor
# y creo la consulta sql como una cadena
# consulta = "SELECT * FROM  profesionales;" # lenguaje SQL
# # Ejecuto la consulta
# cursor.execute(consulta)
# Voy a desempaquetar lo que me trae la consulta (se puede hacer una sola linea)
# datos = cursor.fetchall() # del cursor traeme todo 
# print(datos) # Me devolvió una lista de tuplas si no tengo el (dictionary=True)
# # for dato in datos:
# #     print(dato)
# #     print(type(dato))

# Como me devuelve una lista de diccionarios ya tiene mas el formato de Json, solo que para ser Json deben ser comillas dobles " y no '

#Ahora ya puedo trabajar con los datos de la DB

'''
Por un lado vamos a crear una API que devuelva datos para que consuma el FRONT --> API REST
API al FRONT
API al BACK
Se conectan mandando datos
'''


# SIEMPRE CIERRO LA CONEXIÓN!!!!
# cnx.close()