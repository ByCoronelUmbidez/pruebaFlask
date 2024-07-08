# Clases que corresponden a entidades en la BBDD

from base_db.dml import Tabla
from base_db.config_db import conexion as con 
from auxiliares.cifrado import encriptar
import hashlib
import bcrypt
from flask_login import UserMixin
from werkzeug.security import check_password_hash

class Profesional(Tabla):
    tabla = 'profesionales'
    campos = ('id', 'nombre', 'especialidad', 'horario')
    conexion = con
    
    def __init__(self, *args, de_bbdd=False):
        super().crear(args, de_bbdd) # --> no tiene que ser False, queda para que despues tome los datos
        
    @classmethod
    def obtener_especialidades(cls):
        try:
            consulta = "SELECT DISTINCT especialidad FROM profesionales;"
            resultados = cls._conectar(consulta)
            
            especialidades = [resultado[0] for resultado in resultados]
            
            return especialidades
        except Exception as e:
            print(f"Error al obtener especialidades: {e}")
            return []
            

    @classmethod
    def obtener_profesionales(cls):
        try:
            consulta = "SELECT * FROM profesionales;"
            resultados = cls._conectar(consulta)
            
            profesionales = [resultado[0] and resultado[1] for resultado in resultados]
            
            return profesionales
        except Exception as e:
            print(f"Error al obtener profesionales: {e}")
            return []

    @classmethod
    def _conectar(cls, consulta, datos=None):
        try:
            cursor = cls.conexion.cursor()
        except Exception as e:
            cls.conexion.connect()
            cursor = cls.conexion.cursor()
        
        try:
            if consulta.startswith('SELECT'):
                if datos:
                    cursor.execute(consulta, datos)
                else:
                    cursor.execute(consulta)
                resultados = cursor.fetchall()
                return resultados
            else:
                if datos:
                    cursor.execute(consulta, datos)
                else:
                    cursor.execute(consulta)
                cls.conexion.commit()
                return True
        except Exception as e:
            cls.conexion.rollback()
            print(f"Error en la consulta: {e}")
            return False
        finally:
            cursor.close()

    @classmethod
    def crear(cls, *valores, de_bbdd=False):
        instancia = cls(*valores, de_bbdd=de_bbdd)  # Crear una instancia de la clase con los valores
        return instancia

    @classmethod
    def obtener_profesionales_por_especialidad(cls, especialidad=None):
        consulta = f"SELECT id, nombre, especialidad, horario FROM {cls.tabla} WHERE especialidad = %s;"
        resultados = cls._conectar(consulta, (especialidad,))
        print(resultados)
        return resultados


    @classmethod
    def obtener_horarios_por_profesional(cls, profesional_id):
        try:
            consulta = "SELECT * FROM profesionales WHERE id = %s;"
            print(consulta)
            return cls._conectar(consulta, (profesional_id,))
        except Exception as e:
            print(f"Error al obtener horarios por profesional: {e}")
            return []       
               
    @classmethod    
    def buscar_por_nombre(cls, nombre):
        try:
            conexion = con  # Aquí asumo que 'con' es tu conexión a la base de datos
            cursor = conexion.cursor()
            consulta = "SELECT * FROM profesionales WHERE LOWER(nombre) LIKE %s"
            cursor.execute(consulta, (f'%{nombre}%',))
            results = cursor.fetchone()
            print(f"Consulta ejecutada: {consulta} con nombre: {nombre}")
            print(f"Resultados encontrados: {results}")
            cursor.close()
            return results
        except Exception as e:
            print(f"Error al buscar profesionales por nombre: {str(e)}")
            return None  # Cambiado de lista vacía a None para reflejar que no se encontraron resultados  
        
        # try:
        #     consulta = "SELECT * FROM profesionales WHERE nombre LIKE %s"
        #     resultado = cls._conectar(consulta, (f'%{nombre}%',))

        #     if resultado:
        #         profesional = Profesional(
        #             id=resultado[0],          # Ajusta los índices según tu estructura de la tabla
        #             nombre=resultado[1],
        #             especialidad=resultado[2],
        #             horario=resultado[3],
        #             # Añade otros campos según sea necesario
        #         )
        #         return [profesional]  # Devolver una lista con el profesional encontrado
        #     else:
        #         return []  # Devolver una lista vacía si no se encontró ningún profesional
        
        # except Exception as e:
        #     print(f"Error al buscar profesionales por nombre: {str(e)}")
        #     return []
        
class Sede(Tabla):
    tabla = 'sedes'
    campos = ('id', 'nombre', 'direccion', 'horario_atencion', 'telefono')
    conexion = con
    
    def __init__(self, *args, de_bbdd=False):
        super().crear(args, de_bbdd)
        
    @classmethod
    def obtener_sedes(cls):
        # try:
        #     consulta = "SELECT id, nombre FROM sedes;"
        #     return cls.__conectar(consulta)
        # except Exception as e:
        #     print(f"Error al obtener sedes: {e}")
        #     return []
        
        
        try:
            consulta = "SELECT id, nombre FROM sedes;"
            resultados = cls._conectar(consulta)
            
            sedes = resultados
            
            return sedes
        except Exception as e:
            print(f"Error al obtener especialidades: {e}")
            return [] 
        
    @staticmethod    
    def buscar_por_nombre(nombre):
        try:
            conexion = con
            cursor = conexion.cursor()
            consulta = "SELECT * FROM profesionales WHERE nombre LIKE %s"
            cursor.execute(consulta, (f'%{nombre}%',))
            results = cursor.fetchall()
            cursor.close()
            return results
        except Exception as e:
            print(f"Error al buscar profesionales por nombre: {str(e)}")
            return [] 
        
    @classmethod
    def _conectar(cls, consulta, datos=None):
        try:
            cursor = cls.conexion.cursor()
        except Exception as e:
            cls.conexion.connect()
            cursor = cls.conexion.cursor()
        
        try:
            if consulta.startswith('SELECT'):
                if datos:
                    cursor.execute(consulta, datos)
                else:
                    cursor.execute(consulta)
                resultados = cursor.fetchall()
                return resultados
            else:
                if datos:
                    cursor.execute(consulta, datos)
                else:
                    cursor.execute(consulta)
                cls.conexion.commit()
                return True
        except Exception as e:
            cls.conexion.rollback()
            print(f"Error en la consulta: {e}")
            return False
        finally:
            cursor.close()            
                                   
class Contacto(Tabla):
    tabla = 'contacto'
    campos = ('id', 'nombre', 'email', 'mensaje')
    conexion = con
    
    def __init__(self, *args, de_bbdd=False):
        super().crear(args, de_bbdd)
        
# Clase Usuario
class Usuario(Tabla, UserMixin):
    tabla = 'usuarios'
    conexion = con
    campos = ('id', 'username', 'password', 'nombre', 'email')
    
    def __init__(self, *args, de_bbdd=False):
        super().crear(args, de_bbdd)
 
    @classmethod
    def crear(cls, valores, de_bbdd=False):
        if de_bbdd:
            # del modelo --> args = (valores) # (())
            for campo, valor in zip(cls.campos, *valores):
                setattr(cls, campo, valor)
        else:
            for campo, valor in zip(cls.campos[1:], valores):
                setattr(cls, campo, valor)
    
    # @staticmethod
    # def encriptar(password):
    #     return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # @staticmethod
    # def verificar_password(password_ingresada, password_almacenada):
    #     return bcrypt.checkpw(password_ingresada.encode('utf-8'), password_almacenada.encode('utf-8'))
    
    @classmethod
    def eliminar(cls, id):
        consulta = "DELETE FROM {tabla} WHERE id = %s".format(tabla=cls.tabla)
        rta_db = cls.__conectar(consulta, (id,))
        
        if rta_db:
            return 'Eliminación exitosa.'
            
        return 'No se pudo eliminar el registro.'

    @classmethod        
    def __conectar(cls, consulta, datos=None):
        
        try:
            cursor = cls.conexion.cursor()
        except Exception as e:
            cls.conexion.connect()
            cursor = cls.conexion.cursor()
        
        if consulta.startswith('SELECT'): # si empieza la consulta con SELECT quiere decir que me va a traer algo de la db. Entonces empiezo a analizar si vienen o no datos.
            
            if datos is not None:
                cursor.execute(consulta, datos)
            else:
                cursor.execute(consulta)
                
            rta_db = cursor.fetchall()
            
            if rta_db != []:
                resultado = [cls(registro, de_bbdd=True) for registro in rta_db]
                if len(resultado) == 1:
                    resultado = resultado[0]
            else:
                resultado = False                       
            
            cls.conexion.close()
        
        else: # Si no hago un SELECT ... 
            
            try:
                # Crud-Update-Delete puede salir mal con esto lo contengo, agarro el error
                cursor.execute(consulta, datos)
                cls.conexion.commit()    
                cls.conexion.close()
                resultado = True
            except Exception as e:
                resultado = False
            
        return resultado
    
    @classmethod
    def obtener_todos(cls):
        consulta = f"SELECT * FROM {cls.tabla};"
        resultados = cls.__conectar(consulta)
        return resultados
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'nombre': self.nombre,
            'email': self.email
            # Agrega más campos si es necesario
        }      
        
    @classmethod
    def obtener_usuario(cls, campo=None, valor=None):
        if campo is None or valor is None:
            consulta = f"SELECT * FROM {cls.tabla};"
            resultado = cls._conectar(consulta)
        else:
            consulta = f"SELECT * FROM {cls.tabla} WHERE {campo} = %s;"
            resultado = cls._conectar(consulta, (valor,))

        if resultado:
            return cls(*resultado[0])
        return None
    
    @classmethod
    def obtener_por_username(cls, username):
        consulta = f"SELECT * FROM {cls.tabla} WHERE username = %s;"
        resultado = cls._conectar(consulta, (username,))
        if resultado:
            return cls(*resultado)
        return None

    @staticmethod
    def verify_password(stored_password, provided_password):
        return check_password_hash(stored_password, provided_password)
           

    @classmethod
    def obtener_por_usuario(cls, user_id):
        consulta = f"SELECT * FROM usuarios WHERE id = %s"  # Cambié 'id_usuario' a 'id'
        resultado = cls.__conectar(consulta, (user_id,))
        
        if resultado:
            usuario = {
                'id': resultado.id,
                'username': resultado.username,
                'nombre': resultado.nombre,
                'email': resultado.email,
            }
            return usuario
        else:
            return None  # Retornar None si no hay resultados
    
    
    @staticmethod
    def obtener_usuario_id(user_id):
        usuario = Usuario.obtener_por_usuario(user_id)  # Suponiendo que devuelve un usuario como un diccionario
        print(usuario)
        if usuario and isinstance(usuario, dict):
            usuario_json = {
                'id': usuario.get('id'),
                'username': usuario.get('username'),
                'nombre': usuario.get('nombre'),
                'email': usuario.get('email')
            }
            return usuario_json
        else:
            return None

    @classmethod
    def obtener_para_login(cls, username):
        consulta = f"SELECT * FROM {cls.tabla} WHERE username = %s;"
        usuario = cls.__conectar(consulta, (username,))
        return usuario  # Retornamos directamente el objeto usuario


        
class Turno(Tabla):
    tabla = 'turnos'
    campos = ('id', 'fecha_hora', 'id_profesional', 'id_sede', 'id_usuario', 'especialidad')
    conexion = con
    
    def __init__(self, fecha_hora=None, id_profesional=None, id_sede=None, id_usuario=None, especialidad=None):
        self.fecha_hora = fecha_hora
        self.id_profesional = id_profesional
        self.id_sede = id_sede
        self.id_usuario = id_usuario
        self.especialidad = especialidad
        
        super().__init__(self.tabla, self.conexion, self.campos)

    @classmethod
    def guardar_turno(cls, fecha_hora, id_profesional, id_sede, id_usuario, especialidad):
        consulta = f"INSERT INTO {cls.tabla} (fecha_hora, id_profesional, id_sede, id_usuario, especialidad) VALUES (%s, %s, %s, %s, %s)"
        datos = (fecha_hora, id_profesional, id_sede, id_usuario, especialidad)

        try:
            with cls.conexion.cursor() as cursor:
                cursor.execute(consulta, datos)
                cls.conexion.commit()
            return 'Creación exitosa.'
        except Exception as e:
            cls.conexion.rollback()
            return f"Error al guardar en la base de datos: {str(e)}"

    @classmethod
    def obtener_por_usuario(cls, user_id):
        consulta = f"SELECT * FROM {cls.tabla} WHERE id_usuario = %s"

        try:
            resultados = cls._conectar(consulta, (user_id,))
            print("Resultados de la consulta:", resultados)  # Para depuración
            
            resultados.append(turno for turno in resultados)

        except Exception as e:
            print(f"Error al obtener turnos por usuario: {str(e)}")
            return []  # Manejar errores retornando una lista vacía o adecuadamente según tu lógica de manejo de errores

    
    @staticmethod
    def obtener_turnos_usuario(user_id):
        turnos = Turno.obtener_por_usuario(user_id)  # Suponiendo que tienes un método para obtener turnos por usuario
        turnos_json = []
        for turno in turnos:
            turnos_json.append({
                'id': turno.id,
                'fecha': turno.fecha,  # Ajusta según el campo en tu modelo
                'hora': turno.hora,  # Ajusta según el campo en tu modelo
                'especialidad': turno.especialidad,  # Ajusta según el campo en tu modelo
                'doctor': turno.doctor  # Ajusta según el campo en tu modelo
            })
        return turnos_json    
    
    @classmethod        
    def _conectar(cls, consulta, datos=None):
        
        try:
            cursor = cls.conexion.cursor()
        except Exception as e:
            cls.conexion.connect()
            cursor = cls.conexion.cursor()
        
        if consulta.startswith('SELECT'): # si empieza la consulta con SELECT quiere decir que me va a traer algo de la db. Entonces empiezo a analizar si vienen o no datos.
            
            if datos is not None:
                cursor.execute(consulta, datos)
            else:
                cursor.execute(consulta)
                
            rta_db = cursor.fetchall()
            print("Resultados de la consulta:", rta_db)  # Añade esta línea para depurar
            
            if rta_db != []:
                resultado = [cls(registro) for registro in rta_db] # saque ddbb
                if len(resultado) == 1:
                    resultado = resultado[0]
            else:
                resultado = False                       
            
            cls.conexion.close()
        
        else: # Si no hago un SELECT ... 
            
            try:
                # Crud-Update-Delete puede salir mal con esto lo contengo, agarro el error
                cursor.execute(consulta, datos)
                cls.conexion.commit()    
                cls.conexion.close()
                resultado = True
            except Exception as e:
                resultado = False
            
        return resultado       
                                
                     