CREATE DATABASE turnos_medicos;
USE turnos_medicos;

-- Creación de la tabla Profesionales
CREATE TABLE Profesionales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    especialidad VARCHAR(100) NOT NULL,
    horario VARCHAR(50) NOT NULL
);

-- Creación de la tabla Sedes
CREATE TABLE Sedes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(255) NOT NULL,
    horario_atencion VARCHAR(50) NOT NULL
);
ALTER TABLE Sedes
ADD COLUMN telefono VARCHAR(20);

-- Creación de la tabla ProfesionalSede para la relación muchos a muchos
CREATE TABLE ProfesionalSede (
    id_profesional INT,
    id_sede INT,
    PRIMARY KEY (id_profesional, id_sede),
    FOREIGN KEY (id_profesional) REFERENCES Profesionales(id),
    FOREIGN KEY (id_sede) REFERENCES Sedes(id)
);

-- Creación de la tabla Turnos
CREATE TABLE Turnos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha_hora DATETIME NOT NULL,
    id_profesional INT,
    id_sede INT,
    FOREIGN KEY (id_profesional) REFERENCES Profesionales(id),
    FOREIGN KEY (id_sede) REFERENCES Sedes(id)
);
-- Agregar columna id_usuario a la tabla Turnos
ALTER TABLE Turnos
ADD COLUMN id_usuario INT,
ADD CONSTRAINT fk_turnos_usuario
FOREIGN KEY (id_usuario) REFERENCES Usuarios(id);

-- Creación de la tabla Contacto
CREATE TABLE Contacto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    mensaje TEXT NOT NULL
);

-- Creación de la tabla Usuarios
CREATE TABLE Usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL
);

-- Modificar la tabla Usuarios para agregar la columna id_usuario
ALTER TABLE Usuarios
ADD COLUMN id_usuario INT,
ADD FOREIGN KEY (id_usuario) REFERENCES Usuarios(id);

SELECT * FROM Usuarios;
-- Añadir claves foráneas a la tabla Turnos
ALTER TABLE Turnos
ADD FOREIGN KEY (id_profesional) REFERENCES Profesionales(id),
ADD FOREIGN KEY (id_sede) REFERENCES Sedes(id),
ADD FOREIGN KEY (id_usuario) REFERENCES Usuarios(id);