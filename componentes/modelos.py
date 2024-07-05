# Importar las clases necesarias de SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify


# Instancia de SQLAlchemy
db = SQLAlchemy()

# Modelos SQLAlchemy

class Profesional(db.Model):
    __tablename__ = 'profesionales'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    especialidad = db.Column(db.String(100), nullable=False)
    horario = db.Column(db.String(100), nullable=True)

    # Relación con Turno (uno a muchos)
    turnos = db.relationship('Turno', backref='profesional', lazy=True)

    def __init__(self, nombre, especialidad, horario=None):
        self.nombre = nombre
        self.especialidad = especialidad
        self.horario = horario

class Sede(db.Model):
    __tablename__ = 'sedes'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    horario_atencion = db.Column(db.String(100), nullable=True)
    telefono = db.Column(db.String(20), nullable=True)

    # Relación con Turno (uno a muchos)
    turnos = db.relationship('Turno', backref='sede', lazy=True)

    def __init__(self, nombre, direccion, horario_atencion=None, telefono=None):
        self.nombre = nombre
        self.direccion = direccion
        self.horario_atencion = horario_atencion
        self.telefono = telefono

class Turno(db.Model):
    __tablename__ = 'turnos'

    id = db.Column(db.Integer, primary_key=True)
    fecha_hora = db.Column(db.DateTime, nullable=False)
    id_profesional = db.Column(db.Integer, db.ForeignKey('profesionales.id'), nullable=False)
    id_sede = db.Column(db.Integer, db.ForeignKey('sedes.id'), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    disponible = db.Column(db.Boolean, default=True, nullable=False)

    def __init__(self, fecha_hora, id_profesional, id_sede, id_usuario=None, disponible=True):
        self.fecha_hora = fecha_hora
        self.id_profesional = id_profesional
        self.id_sede = id_sede
        self.id_usuario = id_usuario
        self.disponible = disponible

# Asegura que la conexión de la aplicación Flask esté configurada correctamente
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'  # Reemplaza con tus datos
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa la extensión SQLAlchemy con la aplicación Flask
db.init_app(app)

# Rutas y lógica de tu aplicación Flask
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

