from flask import jsonify
from app import app
from componentes.modelos import Profesional
from componentes.modelos import Sede
from componentes.modelos import Usuario
from componentes.modelos import Turno
from componentes.modelos import con
from flask import request
import bcrypt
from flask_login import login_user
from flask_login import login_required
from flask_login import logout_user
from flask_login import current_user



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
    
    if usuario:
        print(f"Contraseña almacenada en la base de datos: {usuario.password}")  # Se imprime la contraseña almacenada (hash) para fines de debug (no se debe mostrar en producción)

        # **Revisar la implementación de bcrypt.checkpw()**

        # 1. Codificar las contraseñas a utf-8
        # contrasena_ingresada_bytes = password.encode('utf-8')
        # print(contrasena_ingresada_bytes)
        # contrasena_almacenada_bytes = usuario.password.encode('utf-8')
        # print(contrasena_almacenada_bytes)

        # 2. Verificar los argumentos de bcrypt.checkpw()
        es_valida = usuario.password == password

        # 3. Revisar errores de sintaxis o lógica
        if es_valida:
            return jsonify({'mensaje': 'Inicio de sesión exitoso'}), 200
        else:
            return jsonify({'mensaje': 'Credenciales inválidas'}), 401
    else:
        return jsonify({'mensaje': 'Credenciales inválidas'}), 401
    
    
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
    usuario = current_user
    turnos = Turno.obtener_por_usuario(usuario.id)
    return jsonify({
        'id': usuario.id,
        'username': usuario.username,
        'nombre': usuario.nombre,
        'email': usuario.email,
        'turnos': turnos
    })

@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'mensaje': 'Sesión cerrada'})


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


@app.route('/api/horarios/<especialidad>', methods=['GET'])
def api_horarios_por_profesional(especialidad):
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
            'horario': profesional.horario,
            # Agrega otros campos necesarios
        }
        profesionales_json.append(profesional_json)

    # Convertir a formato JSON y devolver
    return jsonify(profesionales_json)    
    

@app.route('/api/sedes', methods=['GET'])
def api_sedes():
    sedes = Sede.obtener_sedes()
    return jsonify(sedes)

@app.route('/api/guardar_turno', methods=['POST'])
def guardar_turno():
    data = request.get_json()

    # Aquí debes validar y guardar los datos en la tabla 'turnos'
    especialidad = data.get('especialidad')
    profesional = data.get('profesional')
    horario = data.get('horario')
    sede = data.get('sede')

    # Ejemplo básico de guardar en la base de datos
    # Puedes adaptar esto a tu implementación con MySQL
    # Guardar en la tabla 'turnos'
    # Insertar los datos en tu base de datos

    # Ejemplo de respuesta
    response = {
        'message': 'Turno guardado exitosamente',
        'turno': {
            'especialidad': especialidad,
            'profesional': profesional,
            'horario': horario,
            'sede': sede
            # Puedes agregar más campos según tu estructura de base de datos
        }
    }
    return jsonify(response), 200