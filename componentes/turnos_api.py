from flask import Flask, request, jsonify
from flask_cors import CORS
from base_db import config_db
from componentes.modelos import Profesional, Sede, Turno, ProfesionalSede

app = Flask(__name__)
CORS(app)

@app.route('/api/buscar_turnos', methods=['POST'])
def buscar_turnos():
    data = request.json
    especialidad = data.get('especialidad')
    sede = data.get('sede')

    try:
        # Consulta utilizando los modelos de SQLAlchemy
        turnos = (
            Turno.query
            .join(Profesional)
            .join(Sede)
            .filter(Profesional.especialidad == especialidad,
                    Sede.nombre == sede,
                    Turno.disponible == True)
            .all()
        )

        # Formateo de los resultados a JSON
        resultados = [
            {
                'id': turno.id,
                'fecha_hora': turno.fecha_hora.strftime('%Y-%m-%d %H:%M:%S'),
                'profesional': turno.profesional.nombre,
                'sede': turno.sede.nombre
            }
            for turno in turnos
        ]

        return jsonify(resultados)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()