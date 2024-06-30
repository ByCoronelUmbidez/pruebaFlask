from componentes.conexion_db import conexion


def obtener_datos():
        # Por defecto MySQL -> timeOut = 300seg. entonces la voy a contener con una excepción
    con = conexion
        
    try:
        print('BBDD conectada')
        cursor = con.cursor(dictionary=True)
    except Exception as e:
        print('BBDD reconectada')
        con.connect()
        cursor = con.cursor()
    
    consulta = 'SELECT * FROM profesionales;'
    cursor.execute(consulta)
    datos = cursor.fetchall()
    con.close()
    
    return datos