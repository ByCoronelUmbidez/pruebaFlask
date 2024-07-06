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
    """
    Lista todas las rutas disponibles en la API.

    Retorna:
        Un diccionario JSON con las rutas y sus descripciones.
    """
    # URL base de la aplicación (ajustar según tu configuración)
    url_base = "http://localhost:5000"

    rutas = [
        {
            "ruta": "/",
            "descripcion": "Ruta principal de la API.",
            "url": f"{url_base}/",
            "metodos": ["GET"],
        },
        {
            "ruta": "/api/profesionales",
            "descripcion": "Obtiene una lista de profesionales.",
            "url": f"{url_base}/api/profesionales",
            "metodos": ["GET"],
        },
        {
            "ruta": "/api/sedes",
            "descripcion": "Obtiene una lista de sedes.",
            "url": f"{url_base}/api/sedes",
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
            "url": f"{url_base}/api/profesionales/1",  # Ejemplo de especialidad
            "metodos": ["GET"],
        },
        {
            "ruta": "/api/horarios/<especialidad>",
            "descripcion": "Obtiene los horarios disponibles por especialidad.",
            "url": f"{url_base}/api/horarios/1",  # Ejemplo de especialidad
            "metodos": ["GET"],
        },
        {
            "ruta": "/api/guardar_turno",
            "descripcion": "Guarda un nuevo turno.",
            "url": f"{url_base}/api/guardar_turno",
            "metodos": ["POST"],
        },
    ]

    # Crear una respuesta HTML con enlaces clicables
    html_response = '<ul>'
    for ruta in rutas:
        html_response += f'<li><a href="{ruta["url"]}">{ruta["url"]}</a> - {ruta["descripcion"]} (Métodos: {", ".join(ruta["metodos"])})</li>'
    html_response += '</ul>'

    return html_response


@app.route('/api/profesionales', methods=['GET'])
def mostrar_profesionales():
    profesionales = Profesional.obtener()
    dicc_profesionales = [profesional.__dict__ for profesional in profesionales]
    return jsonify(dicc_profesionales)
    
@app.route('/api/sedes', methods=['GET'])
def mostrar_sedes():
    sedes = Sede.obtener()
    dicc_sedes = [sede.__dict__ for sede in sedes]
    return jsonify(dicc_sedes)


@app.route('/api/registro', methods=['POST'])
def registro():
    datos = request.json  # Obtener los datos del cuerpo de la solicitud JSON

    # Validar los datos recibidos
    if not all(key in datos for key in ['username', 'password', 'nombre', 'email']):
        print("Datos incompletos")
        return jsonify({'error': 'Datos incompletos'}), 400

    # Encriptar la contraseña antes de crear el nuevo usuario
    # password_encriptada = Usuario.encriptar(datos['password'])
    # print(password_encriptada)

    # Crear un nuevo usuario en la base de datos
    nuevo_usuario = Usuario(
        username=datos['username'],
        password=datos['password'],
        nombre=datos['nombre'],
        email=datos['email']
    )
    
    print(f"Contraseña encriptada: {nuevo_usuario.password}")
    
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
        return jsonify({'mensaje': 'Falta nombre de usuario o contraseña'}), 400

    usuario = Usuario.obtener_para_login(username)
    print(usuario)
    
    # ingresada_codificada = Usuario.encriptar(password)
    # print(ingresada_codificada)
    
    if usuario and usuario.password == password:
        session['user_id'] = usuario.id  # Guardar el ID del usuario en la sesión
        return jsonify({'message': 'Inicio de sesión exitoso'}), 200

    else:
        return jsonify({'message': 'Credenciales inválidas'}), 401
    
    # if usuario:
    #     print(f"Contraseña almacenada en la base de datos: {usuario.password}")  # Se imprime la contraseña almacenada (hash) para fines de debug (no se debe mostrar en producción)

    
    #     es_valida = usuario.password == password
        
    #     if usuario and Usuario.verify_password(usuario.password, password):
    #         login_user(usuario)
    #         return redirect(url_for('seleccionar_turno'))

    #     # 3. Revisar errores de sintaxis o lógica
    #     if es_valida:
    #         return jsonify({'mensaje': 'Inicio de sesión exitoso'}), 200
    #     else:
    #         return jsonify({'mensaje': 'Credenciales inválidas'}), 401
    # else:
    #     return jsonify({'mensaje': 'Credenciales inválidas'}), 401
    
    
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


@app.route('/api/perfil', methods=['GET'])
@login_required
def perfil():
    user_id = session.get('user_id')
    if user_id:
        usuario = Usuario.buscar_por_id(user_id)
        if usuario:
            return jsonify({
                'id': usuario.id,
                'username': usuario.username,
                'nombre': usuario.nombre,
                'email': usuario.email
            })
    return jsonify({'message': 'Usuario no encontrado'}), 404

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

# Rutas para obtener datos de la base de datos usando Profesional.obtener
@app.route('/api/especialidades', methods=['GET'])
def api_especialidades():
    profesionales = Profesional.obtener()
    if not profesionales:
        return jsonify([])  # Devolver una lista vacía si no hay profesionales
    especialidades = set()  # Usamos un set para garantizar especialidades únicas
    for profesional in profesionales:
        especialidades.add(profesional.especialidad)

    return jsonify(list(especialidades))


@app.route('/api/profesionales/<especialidad>', methods=['GET'])
def api_profesionales_por_especialidad(especialidad):
    # Obtener todos los profesionales
    profesionales = Profesional.obtener()

    # Filtrar por especialidad si se proporciona una
    if especialidad != 'all':
        profesionales_filtrados = [profesional for profesional in profesionales if profesional.especialidad.lower() == especialidad.lower()]
    else:
        profesionales_filtrados = profesionales

    # Preparar la lista de profesionales en formato JSON
    profesionales_json = []
    for profesional in profesionales_filtrados:
        profesional_json = {
            'nombre': profesional.nombre,
            # Agrega otros campos necesarios
        }
        profesionales_json.append(profesional_json)

    # Convertir a formato JSON y devolver
    return jsonify(profesionales_json)


@app.route('/api/horarios/<int:profesional_id>', methods=['GET'])
def api_horarios_por_profesional(profesional_id):
    print(f'ID del profesional recibido en la API: {profesional_id}')
    profesionales = Profesional.obtener()

    # Filtrar los profesionales por el ID proporcionado
    profesionales_filtrados = [profesional for profesional in profesionales if profesional.id == profesional_id]

    # Preparar la lista de horarios en formato JSON
    horarios_json = []
    for profesional in profesionales_filtrados:
        # Si cada profesional tiene solo un horario, obtener ese horario directamente
            horario_json = {
                'id': profesional.id,
                'horario': profesional.horario,
                # Agrega otros campos necesarios
            }
            horarios_json.append(horario_json)

    print(f'Horarios encontrados para {profesional_id}: {horarios_json}')
    # Convertir a formato JSON y devolver
    return jsonify(horarios_json)


@app.route('/api/sedes', methods=['GET'])
def api_sedes():
    sedes = Sede.obtener_sedes()
    return jsonify(sedes)


@app.route('/api/guardar_turno', methods=['POST'])
@login_required
def guardar_turno():
    id_profesional = request.form.get('id_profesional')
    id_sede = request.form.get('id_sede')
    horario = request.form.get('horario')
    especialidad = request.form.get('especialidad')
    
    # Obtener el id_usuario desde la sesión
    id_usuario = session.get('user_id')

    # Convertir el campo horario a un objeto datetime
    try:
        fecha_hora = datetime.strptime(horario, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return jsonify({'error': 'Formato de fecha y hora no válido'}), 400

    nuevo_turno = Turno(fecha_hora, id_profesional, id_sede, id_usuario, especialidad)
    resultado = nuevo_turno.guardar_db()
    
    if 'Error' in resultado:
        return jsonify({'error': resultado}), 500
    
    return jsonify({'message': 'Turno guardado exitosamente'}), 201

# Ruta para buscar profesionales por nombre
@app.route('/api/profesionales/nombre/<nombre>', methods=['GET'])
def buscar_profesionales(nombre):
    # if nombre:
    #     # Realiza la búsqueda en la base de datos
    #     profesionales = Profesional.buscar_por_nombre(nombre)
    #     # Formatea los resultados como JSON y devuélvelos
    #     return jsonify(profesionales)
    # else:
    #     return jsonify([])  # Retorna una lista vacía si no se proporcionó nombre

    profesionales = Profesional.obtener()

    # Filtrar por especialidad si se proporciona una
    if nombre != 'all':
        profesionales_filtrados = [profesional for profesional in profesionales if profesional.nombre.lower() == nombre.lower()]
    else:
        profesionales_filtrados = profesionales

    # Preparar la lista de profesionales en formato JSON
    profesionales_json = []
    for profesional in profesionales_filtrados:
        profesional_json = {
            'id': profesional.id,
            # Agrega otros campos necesarios
        }
        profesionales_json.append(profesional_json)

    # Convertir a formato JSON y devolver
    return jsonify(profesionales_json)   


# Ruta para buscar sedes por nombre
@app.route('/api/sedes/nombre/<nombre>', methods=['GET'])
def buscar_sedes():
    nombre = request.args.get('nombre', '')
    if nombre:
        # Realiza la búsqueda en la base de datos
        sedes = Sede.buscar_por_nombre(nombre)
        # Formatea los resultados como JSON y devuélvelos
        return jsonify(sedes)
    else:
        return jsonify([])  # Retorna una lista vacía si no se proporcionó nombre