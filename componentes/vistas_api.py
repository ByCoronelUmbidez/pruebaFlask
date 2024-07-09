from flask import jsonify
from app import app
from componentes.modelos import Profesional
from componentes.modelos import Sede
from componentes.modelos import Usuario
from componentes.modelos import Turno
from componentes.modelos import con
from flask import request
from flask import session
import bcrypt
from datetime import datetime
from app import login_user
from flask import redirect
from flask import url_for
from app import login_user
from app import current_user
from app import login_required
from app import app



@app.route('/', methods=['GET'])
def listar_rutas():

    # URL base de la aplicación (ajustar según tu configuración)
    url_base = "https://barbycoronelumbidez.pythonanywhere.com/"

    rutas = [
        {
            "ruta": "/",
            "descripcion": "Ruta principal de la API.",
            "url": f"{url_base}/",
            "metodos": ["GET"],
        },
        {
            "ruta": "/api/listar_profesionales",
            "descripcion": "Obtiene una lista de profesionales.",
            "url": f"{url_base}/api/listar_profesionales",
            "metodos": ["GET"],
        },
        {
            "ruta": "/api/listar_sedes",
            "descripcion": "Obtiene una lista de sedes.",
            "url": f"{url_base}/api/listar_sedes",
            "metodos": ["GET"],
        },
        {
            "ruta": "/api/registro",
            "descripcion": "Registra un nuevo usuario.",
            "url": f"{url_base}/api/registro",
            "metodos": ["POST"],
        },
        {
            "ruta": "/api/login",
            "descripcion": "Inicia sesión en un usuario existente.",
            "url": f"{url_base}/api/login",
            "metodos": ["POST"],
        },
        {
            "ruta": "/api/eliminar_usuario/<int:id>",
            "descripcion": "Elimina un usuario por su ID.",
            "url": f"{url_base}/api/eliminar_usuario/1",  # Ejemplo de ID
            "metodos": ["POST"],
        },
        {
            "ruta": "/api/listar_usuarios",
            "descripcion": "Obtiene una lista de todos los usuarios.",
            "url": f"{url_base}/api/listar_usuarios",
            "metodos": ["GET"],
        },
        {
            "ruta": "/api/perfil",
            "descripcion": "Obtiene el perfil del usuario actual.",
            "url": f"{url_base}/api/perfil",
            "metodos": ["GET"],
        },
        {
            "ruta": "/api/logout",
            "descripcion": "Cierra la sesión del usuario actual.",
            "url": f"{url_base}/api/logout",
            "metodos": ["POST"],
        },
        {
            "ruta": "/api/especialidades",
            "descripcion": "Obtiene una lista de todas las especialidades disponibles.",
            "url": f"{url_base}/api/especialidades",
            "metodos": ["GET"],
        },
        {
            "ruta": "/api/profesionales/<especialidad>",
            "descripcion": "Obtiene una lista de profesionales por especialidad.",
            "url": f"{url_base}/api/profesionales/odontología",  # Ejemplo de especialidad
            "metodos": ["GET"],
        },
        {
            "ruta": "/api/horarios/<especialidad>",
            "descripcion": "Obtiene los horarios disponibles por id.",
            "url": f"{url_base}/api/horarios/1",  # Ejemplo de id
            "metodos": ["GET"],
        },
        {
            "ruta": "/api/guardar_turno",
            "descripcion": "Guarda un nuevo turno.",
            "url": f"{url_base}/api/guardar_turno",
            "metodos": ["POST"],
        },        {
            "ruta": "/api/profesionales/nombre/<nombre>",
            "descripcion": "Obtener ID por nombre de profesional.",
            "url": f"{url_base}/api/profesionales/nombre/Dra. María García", # Ejemplo de nombre
            "metodos": ["POST"],
        },
        
    ]

    # Crear una respuesta HTML con enlaces clicables
    html_response = '<ul>'
    for ruta in rutas:
        html_response += f'<li><a href="{ruta["url"]}">{ruta["url"]}</a> - {ruta["descripcion"]} (Métodos: {", ".join(ruta["metodos"])})</li>'
    html_response += '</ul>'

    return html_response

@app.route('/api/listar_profesionales', methods=['GET'])
def mostrar_profesionales():
    profesionales = Profesional.listar_profesionales()
    datos = []

    for profesional in profesionales:
        profesional_dict = {
            'id': profesional.id,
            'nombre': profesional.nombre,
            'especialidad': profesional.especialidad,
            'horario': profesional.horario
        }
        datos.append(profesional_dict)

    return jsonify(datos)
    
@app.route('/api/listar_sedes', methods=['GET'])
def mostrar_sedes():
    sedes = Sede.listar_sedes()
    datos = []

    for sede in sedes:
        sede_dict = {
            'id': sede.id,
            'nombre': sede.nombre,
            'direccion': sede.direccion,
            'horario_atencion': sede.horario_atencion,
            'telefono': sede.telefono
        }
        datos.append(sede_dict)

    return jsonify(datos)

@app.route('/api/registro', methods=['POST'])
def registro():
    datos = request.json  # Obtener los datos del cuerpo de la solicitud JSON

    # Validar los datos recibidos
    if not all(key in datos for key in ['username', 'password', 'nombre', 'email']):
        print("Datos incompletos")
        return jsonify({'error': 'Datos incompletos'}), 400

    # Crear un nuevo usuario en la base de datos
    nuevo_usuario = Usuario(
        datos['username'],
        datos['password'],
        datos['nombre'],
        datos['email']
    )
    
    print(nuevo_usuario)
    
    # Guardar el usuario en la base de datos
    resultado = nuevo_usuario.guardar_db()
    print(resultado)

    if resultado == 'Creación exitosa.':
        return jsonify({'mensaje': 'Usuario registrado exitosamente'}), 201
    else:
        return jsonify({'error': 'Error al registrar usuario'}), 500        

# Ruta para manejar el login
@app.route('/api/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return '', 200

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    print("Usuario proporcionado:", username)
    print("Contraseña proporcionada:", password)

    if not username or not password:
        return jsonify({'message': 'Falta nombre de usuario o contraseña'}), 400

    usuario = Usuario.obtener_para_login(username)
    print(usuario)

    if usuario:
        print(f"Contraseña almacenada en la base de datos: {usuario.password}")

        if usuario.password == password:  # Comparar contraseñas como texto plano
            login_user(usuario)  # Esto debería establecer la sesión del usuario
            return jsonify({'message': 'Inicio de sesión exitoso'}), 200
        else:
            return jsonify({'message': 'Credenciales inválidas'}), 401
    else:
        return jsonify({'message': 'Credenciales inválidas'}), 401
     
    
@app.route('/api/perfil', methods=['GET'])
@login_required
def perfil():
    user_id = session.get('user_id')  # Obtén el ID de usuario desde la sesión
    print(f"ID de usuario obtenido de la sesión: {user_id}")
    if not user_id:
        return jsonify({'message': 'Usuario no autenticado'}), 401
    
    # Obtener turnos del usuario
    turnos = Turno.obtener_por_usuario(user_id)
    turnos_json = []

    for turno in turnos:
        # Obtener nombre del profesional y sede
        profesional = Profesional.obtener_por_id(turno.id_profesional)
        sede = Sede.obtener_por_id(turno.id_sede)

        turno_dict = {
            'fecha_hora': turno.fecha_hora,
            'profesional': profesional.nombre if profesional else 'Profesional no encontrado',
            'sede': sede.nombre if sede else 'Sede no encontrada',
            'especialidad': turno.especialidad
        }
        turnos_json.append(turno_dict)

    print("Turnos del usuario:", turnos_json)

    # Obtener información del usuario
    usuario = Usuario.obtener_por_usuario(user_id)
    print("Información del usuario:", usuario)
    
    # Prepara la respuesta JSON
    perfil_data = {
        'id': usuario['id'],
        'username': usuario['username'],
        'nombre': usuario['nombre'],
        'email': usuario['email'],
        'turnos': turnos_json  # Agrega los turnos al perfil_data
    }

    return jsonify(perfil_data), 200

@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Sesión cerrada'}), 200

@app.route('/api/test')
@login_required
def test():
    user_id = session.get('user_id')
    return jsonify({'user_id': user_id})


@app.route('/api/eliminar_usuario/<int:id>', methods=['POST'])
def eliminar_usuario(id):
    resultado = Usuario.eliminar(id)
    if resultado == 'Eliminación exitosa.':
        return jsonify({'mensaje': 'Usuario eliminado exitosamente'}), 200
    else:
        return jsonify({'error': 'No se pudo eliminar el usuario'}), 500

@app.route('/api/listar_usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = Usuario.obtener_todos()  # Método hipotético para obtener todos los usuarios

    # Convertir los objetos de usuarios a una lista de diccionarios
    usuarios_serializados = [usuario.to_dict() for usuario in usuarios]

    return jsonify(usuarios_serializados)


# Rutas para obtener datos de la base de datos usando Profesional.obtener
@app.route('/api/especialidades', methods=['GET'])
def api_especialidades():
    try:
        especialidades = Profesional.obtener_especialidades()
        return jsonify(especialidades)
    except Exception as e:
        return jsonify({'error': f"Error al obtener especialidades: {str(e)}"}), 500


@app.route('/api/profesionales/<especialidad>', methods=['GET'])
def api_profesionales_por_especialidad(especialidad):
    try:
        if especialidad.lower() == 'all':
            profesionales = Profesional.obtener_profesionales_por_especialidad()
        else:
            profesionales = Profesional.obtener_profesionales_por_especialidad(especialidad=especialidad)

        profesionales_json = []
        for profesional in profesionales:
            profesional_json = {
                'id': profesional[0],
                'nombre': profesional[1]
            }
            profesionales_json.append(profesional_json)

        return jsonify(profesionales_json)

    except Exception as e:
        return jsonify({'error': f"Error al obtener profesionales por especialidad: {str(e)}"}), 500


@app.route('/api/horarios/<int:profesional_id>', methods=['GET'])
def api_horarios_por_profesional(profesional_id):
    print(f'ID del profesional recibido en la API: {profesional_id}')
    profesionales = Profesional.obtener_horarios_por_profesional(profesional_id)
    print(profesionales)
    profesionales_json = []
    for profesional in profesionales:
        profesional_json = {
            'id': profesional[0],
            'horario': profesional[3]
        }
        profesionales_json.append(profesional_json)

    return jsonify(profesionales_json)


@app.route('/api/sedes', methods=['GET'])
def api_sedes():
    sedes = Sede.obtener_sedes()
    return jsonify(sedes)


@app.route('/api/guardar_turno', methods=['POST'])
@login_required
def guardar_turno():
    datos = request.json  # Obtener los datos del cuerpo de la solicitud JSON
    print('Datos recibidos:', datos)  # Imprimir los datos recibidos para depuración
    
    # Validar los datos recibidos
    if not all(key in datos for key in ['id_profesional', 'id_sede', 'horario', 'especialidad']):
        return jsonify({'error': 'Datos incompletos'}), 400

    # Obtener el id_usuario desde la sesión
    id_usuario = session.get('user_id')
    print(id_usuario)
    
    try:
        resultado = Turno.guardar_turno(
            fecha_hora=datos['horario'],
            id_profesional=int(datos['id_profesional']),
            id_sede=int(datos['id_sede']),
            id_usuario=int(id_usuario),
            especialidad=datos['especialidad']
        )

        if resultado == 'Creación exitosa.':
            return jsonify({'message': 'Turno guardado exitosamente'}), 201
        else:
            return jsonify({'error': resultado}), 500

    except Exception as e:
        print(f"Error al guardar el turno en la base de datos: {str(e)}")
        return jsonify({'error': 'Error interno al guardar el turno'}), 500


@app.route('/api/profesionales/nombre/<nombre>', methods=['GET'])
def buscar_profesionales(nombre):
    if nombre:
        profesionales = Profesional.buscar_por_nombre(nombre)
        return jsonify(profesionales)
    else:
        return jsonify([])  # Retorna una lista vacía si no se proporcionó nombre


@app.route('/api/sedes/nombre/<nombre>', methods=['GET'])
def buscar_sedes():
    nombre = request.args.get('nombre', '')
    if nombre:
        sedes = Sede.buscar_por_nombre(nombre)
        return jsonify(sedes)
    else:
        return jsonify([])  # Retorna una lista vacía si no se proporcionó nombre
    

@app.route('/api/current_user', methods=['GET'])
def get_current_user():
    user_id = session.get('user_id')
    if user_id:
        return jsonify({'id_usuario': user_id}), 200
    else:
        return jsonify({'error': 'Usuario no autenticado'}), 401