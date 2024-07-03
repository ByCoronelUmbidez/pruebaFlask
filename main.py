from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
app.json.ensure_ascii = False
CORS(app) 
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5500"}})


# Importar las vistas
from componentes.vistas_api import *
# from componentes.vistas_web import *

# Lo siguiente sólo en desarrollo, no en producción
if __name__ == '__main__':
    app.run(debug=True, port=5001)