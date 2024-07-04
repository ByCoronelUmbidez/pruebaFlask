from flask import jsonify
from main import app
from componentes.modelos import Profesional
from componentes.modelos import Sede
from componentes.modelos import ProfesionalSede
from componentes.modelos import Cuenta
from componentes.modelos import Usuario
from componentes.modelos import con
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
import bcrypt


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

@app.route('/api/profesionales_sedes', methods=['GET'])
def mostrar_profesionales_sedes():
    profesionales_sedes = ProfesionalSede.obtener()
    datos = [ps.__dict__ for ps in profesionales_sedes]
    return jsonify(datos)

@app.route("/api/perfil", methods=['POST'])
def buscar_turno():
    
    if request.method == 'POST':
        datos = request.json["datos"]
        cuenta = Cuenta.obtener('correo', datos['correo'])
        perfil = Usuario.obtener('id_cuenta', cuenta.id)
    
        if not perfil:
            turno_nuevo = Usuario(
                cuenta.id,
                datos['username'],
                datos['nombre'],
                datos['email'],
            )
            turno_nuevo = turno_nuevo.guardar_db()
            respuesta = {'mensaje': turno_nuevo}
        else:
            del datos['lenguajes']
            del datos['correo']
            datos['id'] = cuenta.id
            Usuario_modif = Usuario.modificar(datos)
            respuesta = {'mensaje': Usuario_modif}
    else:
        respuesta = {'mensaje': 'no se recibieron datos.'}

    return jsonify(respuesta)


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
    
    
@app.route('/eliminar_usuario/<int:id>', methods=['POST'])
def eliminar_usuario(id):
    resultado = Usuario.eliminar(id)
    if resultado == 'Eliminación exitosa.':
        return redirect(url_for('listar_usuarios'))
    else:
        return 'No se pudo eliminar el registro.'

@app.route('/api/listar_usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = Usuario.obtener_todos()  # Método hipotético para obtener todos los usuarios

    # Convertir los objetos de usuarios a una lista de diccionarios
    usuarios_serializados = [usuario.to_dict() for usuario in usuarios]

    return jsonify(usuarios_serializados)