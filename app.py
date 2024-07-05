from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from componentes.modelos import Usuario

app = Flask(__name__)
app.json.ensure_ascii = False
CORS(app) 
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
# CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5500"}})

app.secret_key = 'admin'

login_manager = LoginManager()
login_manager.init_app(app)

# Importar las vistas
from componentes.vistas_api import *


# Lo siguiente sólo en desarrollo, no en producción
if __name__ == '__main__':
    app.run()