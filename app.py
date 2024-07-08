from flask import Flask
from flask_cors import CORS
from flask import session
from flask import redirect
from flask import url_for
from componentes.modelos import Usuario

app = Flask(__name__)
app.json.ensure_ascii = False
cors = CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
# CORS(app) 
# # CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5500/"}})
# Configuración CORS para permitir todas las solicitudes desde el origen de tu frontend
# CORS(app, origins=['http://127.0.0.1:5500'], supports_credentials=True)

app.secret_key = 'admin'

# Función para iniciar sesión del usuario
def login_user(usuario):
    session['user_id'] = usuario.id

# Función para obtener el usuario actual desde la sesión
def current_user():
    user_id = session.get('user_id')
    if user_id:
        return Usuario.obtener_usuario_id(user_id)
    return None

# Decorador para requerir inicio de sesión
def login_required(f):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'message': 'Usuario no autenticado'}), 401
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

def admin_required(f):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'message': 'Usuario no autenticado'}), 401
        user = Usuario.buscar_por_id(session['user_id'])
        if not user or not user.es_admin:
            return jsonify({'message': 'Acceso denegado. Se requieren permisos de administrador'}), 403
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Sesión cerrada'}), 200


# Importar las vistas
from componentes.vistas_api import *


# Lo siguiente sólo en desarrollo, no en producción
if __name__ == '__main__':
    app.run()