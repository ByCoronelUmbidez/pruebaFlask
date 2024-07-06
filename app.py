from flask import Flask
from flask_cors import CORS
from flask import session
from flask import redirect
from flask import url_for
from componentes.modelos import Usuario

app = Flask(__name__)
app.json.ensure_ascii = False
CORS(app) 
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
# CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5500"}})

app.secret_key = 'admin'

# Función para iniciar sesión del usuario
def login_user(usuario):
    session['user_id'] = usuario.id

# Función para obtener el usuario actual desde la sesión
def current_user():
    user_id = session.get('user_id')
    if user_id:
        return Usuario.buscar_por_id(user_id)
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

# Importar las vistas
from componentes.vistas_api import *


# Lo siguiente sólo en desarrollo, no en producción
if __name__ == '__main__':
    app.run()