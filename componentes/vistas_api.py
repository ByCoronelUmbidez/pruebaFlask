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
        datos = request.json.get("datos")  # Obtén los datos correctamente del JSON
        if datos:
            correo = datos.get('correo')
            cuenta = Cuenta.obtener('correo', correo)
            
            if cuenta:
                perfil = Usuario.obtener('id_cuenta', cuenta.id)
                if not perfil:
                    # Crear un nuevo usuario si no existe perfil asociado a esta cuenta
                    nuevo_usuario = Usuario(
                        cuenta.id,
                        datos['username'],
                        datos['nombre'],
                        datos['email']
                    )
                    nuevo_usuario.guardar_db()
                    respuesta = {'mensaje': 'Usuario creado exitosamente.'}
                else:
                    # Modificar el usuario existente
                    datos_modificados = {
                        'id': cuenta.id,
                        'username': datos['username'],
                        'nombre': datos['nombre'],
                        'email': datos['email']
                    }
                    Usuario.modificar(datos_modificados)
                    respuesta = {'mensaje': 'Usuario modificado exitosamente.'}
            else:
                respuesta = {'mensaje': 'No se encontró una cuenta asociada al correo proporcionado.'}
        else:
            respuesta = {'mensaje': 'No se recibieron datos válidos.'}
    else:
        respuesta = {'mensaje': 'Solicitud no permitida.'}

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
    
    if usuario:
        print(f"Contraseña almacenada en la base de datos: {usuario.password}")  # PARA DEPURAR
        
        # Verificar la contraseña ingresada usando bcrypt
        contrasena_ingresada = password.encode('utf-8')  # CODIFICAR LA CONTRASEÑA INGRESADA
        
        if bcrypt.checkpw(contrasena_ingresada, usuario.password.encode('utf-8')):
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