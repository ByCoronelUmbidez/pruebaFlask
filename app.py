from flask import Flask
from flask import jsonify
from componentes.datos import obtener_datos

app = Flask(__name__) #cuando llame a flask va ir a buscar la instancia name

# Cree una VISTA --> funciones que devuelven info al front
@app.route('/') # http://127.0.0.1:5000/
def inicio():
    return "Bienvenidos a Flask!"

# @app.route toma la ruta, la función y la devuelve en la direción asignada
@app.route('/api/profesionales') # http://127.0.0.1:5000/api/profesionales
def mostrar_datos():
    return jsonify(obtener_datos())
    

if __name__ == '__main__':
    app.run()