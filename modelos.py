# Clases

import config_db

class Tabla:
    pass

class Profesional: 
    tabla = 'profesionales'
    campos = ('id', 'nombre', 'especialidad', 'horario')
    conexion = config_db.conexion
    
    # Método constructor (o iniciador)
    def __init__(self, *args, id=None):
        # Atributos de la instancia
        # self.nombre = nombre
        # self.especialidad = especialidad
        # self.horario = horario
        if id:
            for campo, valor in zip(self.campos, args[0]):
                setattr(self, campo, valor)
        else:
            for campo, valor in zip(self.campos[1:], args):
                setattr(self, campo, valor)        
    
    def saludar(self):
        return f"Hola, soy {self.nombre}"
    
    def guardar_db(self):
        self.conexion.connect()
        cursor = self.conexion.cursor()
        # En la consulta no me dejaba poner comillas dobles, entonces tuve que usar triples.
        consulta = f"""INSERT INTO {self.tabla} {str(self.campos[1:]).replace("'", "`")} VALUES (%s, %s, %s);"""
        datos = (self.nombre, self.especialidad, self.horario)
        cursor.execute(consulta, datos) #Primer parametro la query, el segundo los datos(valores) en una tupla siempre
        self.conexion.commit()
        self.conexion.close()
        
        #con esto ya puedo crear los registros(cada fila con valores) en la base de datos
        
    def modificar():
        pass
    def eliminar():
        pass    
    
    @classmethod
    def obtener_todos(cls):
        f"SELECT * FROM {cls.tabla}"
        pass

    @classmethod
    def obtener_profesional(cls, id):
        cls.conexion.connect()
        cursor = cls.conexion.cursor()
        # En la consulta no me dejaba poner comillas dobles, entonces tuve que usar triples.
        consulta = f"SELECT * FROM {cls.tabla} WHERE id = %s;"
        datos = (id,)
        cursor.execute(consulta, datos) #Primer parametro la query, el segundo los datos(valores) en una tupla siempre
        datos = cursor.fetchone()
        cls.conexion.close()  
        #return datos # retorné una tupla, pero me gustaria obtener un objeto para tener los metodos de Profesional
        return(Profesional(datos, id=id))