import mysql.connector

config_dev = {
    # configuración en desarrollo (local)
    "user": 'root',
    'password': '',
    'host': '127.0.0.1',
    'database': 'turnos_medicos'
}

config_prod = {
    # configuración en producción (despliegue)
    "user": 'BarbyCoronelUmbi',
    'password': 'turnosmedicos',
    'host': 'BarbyCoronelUmbidez.mysql.pythonanywhere-services.com',
    'database': 'BarbyCoronelUmbi$TurnosMedicos'
}

conexion = mysql.connector.connect(**config_dev)