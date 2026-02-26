-- Crear base de datos si no existe
CREATE DATABASE IF NOT EXISTS student_hours;
USE student_hours;

-- Tabla de actividades
CREATE TABLE IF NOT EXISTS actividades (
    id_actividad INT AUTO_INCREMENT PRIMARY KEY,
    nombre_actividad VARCHAR(150) NOT NULL
);

-- Tabla de estudiantes
CREATE TABLE IF NOT EXISTS estudiantes (
    numero_control VARCHAR(20) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) UNIQUE,
    telefono VARCHAR(15)
);

-- Tabla de registro de actividades
CREATE TABLE IF NOT EXISTS registro_actividades (
    id_registro INT AUTO_INCREMENT PRIMARY KEY,
    numero_control VARCHAR(20),
    id_actividad INT,
    fecha DATE NOT NULL,
    horas INT NOT NULL,
    FOREIGN KEY (numero_control) REFERENCES estudiantes(numero_control),
    FOREIGN KEY (id_actividad) REFERENCES actividades(id_actividad)
);