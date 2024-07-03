# Clases que corresponden a entidades en la BBDD

from base_db.dml import Tabla
from base_db.config_db import conexion as con 
from auxiliares.cifrado import encriptar
import hashlib
import bcrypt

class Profesional(Tabla):
    tabla = 'profesionales'
    campos = ('id', 'nombre', 'especialidad', 'horario')
    conexion = con
    
    def __init__(self, *args, de_bbdd=False):
        super().crear(args, de_bbdd) # --> no tiene que ser False, queda para que despues tome los datos
        
class Sede(Tabla):
    tabla = 'sedes'
    campos = ('id', 'nombre', 'direccion', 'horario_atencion', 'telefono')
    conexion = con
    
    def __init__(self, *args, de_bbdd=False):
        super().crear(args, de_bbdd)
        
class ProfesionalSede(Tabla):
    tabla = 'profesionalsede'
    campos = ('id_profesional', 'id_sede')
    conexion = con
    
    def __init__(self, *args, de_bbdd=False):
        super().crear(args, de_bbdd)     
        
class Contacto(Tabla):
    tabla = 'contacto'
    campos = ('id', 'nombre', 'email', 'mensaje')
    conexion = con
    
    def __init__(self, *args, de_bbdd=False):
        super().crear(args, de_bbdd)
        
class Turno(Tabla):
    tabla = 'turnos'
    campos = ('id', 'fecha_hora', 'id_profesional', 'id_sede', 'id_usuario')
    conexion = con
    
    def __init__(self, *args, de_bbdd=False):
        super().crear(args, de_bbdd)        
        
# Clase Usuario
class Usuario(Tabla):
    tabla = 'usuarios'
    conexion = con
    campos = ('id', 'username', 'password', 'nombre', 'email', 'id_usuario')
    
    def __init__(self, *args, de_bbdd=False, **kwargs):
        if not de_bbdd:
            usuario = {
                'username': kwargs.get('username'),
                'password': self.encriptar(kwargs.get('password')),  # Aquí se encripta la contraseña
                'nombre': kwargs.get('nombre'),
                'email': kwargs.get('email'),
                'id_usuario': kwargs.get('id_usuario', None)  # Opcional
            }
            super().__init__(self.tabla, self.conexion, self.campos)
            self.crear(tuple(usuario.values()), de_bbdd)
        else:
            super().__init__(self.tabla, self.conexion, self.campos)
            self.crear(args, de_bbdd)
    
    @staticmethod
    def encriptar(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def verificar_password(password_ingresada, password_almacenada):
        return bcrypt.checkpw(password_ingresada.encode('utf-8'), password_almacenada.encode('utf-8'))

    # @classmethod
    # def obtener_para_login(cls, username):
    #     consulta = f"SELECT * FROM {cls.tabla} WHERE username = %s"
    #     with cls.conexion.cursor() as cursor:
    #         cursor.execute(consulta, (username,))
    #         resultado = cursor.fetchone()
    #         if resultado:
    #             return cls(*resultado, de_bbdd=True)
    #         return None 

        
        
class Cuenta(Tabla):
    
    tabla = 'cuenta'
    conexion = con
    campos = ('id', 'correo', 'clave')
    
    def __init__(self, *args, de_bbdd=False):
        
        if not de_bbdd:
            cuenta = []
            cuenta.append(args[0])
            cuenta.append(encriptar(args[1]))
            super().crear(tuple(cuenta), de_bbdd)
        else:
            super().crear(args, de_bbdd)                 