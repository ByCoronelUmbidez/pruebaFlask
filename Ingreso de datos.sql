-- Inserción de datos de profesionales
INSERT INTO profesionales (nombre, especialidad, horario)
VALUES ('Dr. Juan Pérez', 'Cardiología', 'Lunes y Miércoles, 9:00-12:00'),
       ('Dra. María García', 'Odontología', 'Martes y Jueves, 10:00-14:00'),
       ('Dr. Roberto Martínez', 'Pediatría', 'Lunes y Viernes, 8:00-13:00'),
       ('Dra. Laura Rodríguez', 'Dermatología', 'Miércoles y Viernes, 14:00-18:00'),
       ('Dr. Carlos Sánchez', 'Ginecología', 'Martes y Jueves, 8:00-12:00'),
       ('Dra. Ana López', 'Oftalmología', 'Lunes y Miércoles, 10:00-15:00'),
       ('Dr. Manuel González', 'Ortopedia', 'Martes y Jueves, 9:00-13:00'),
       ('Dra. Marta Díaz', 'Psicología', 'Miércoles y Viernes, 10:00-16:00'),
       ('Dr. Javier Ruiz', 'Urología', 'Lunes y Jueves, 8:00-12:00'),
       ('Dra. Patricia Fernández', 'Endocrinología', 'Martes y Viernes, 9:00-14:00');
       
-- Inserción de datos de sedes
INSERT INTO sedes (nombre, direccion, telefono, horario_atencion) 
VALUES ('Sede Central', 'Calle Principal 123', '(123) 456-7890', ''),
       ('Sucursal Norte', 'Avenida Norte 456', '(987) 654-3210', '');
