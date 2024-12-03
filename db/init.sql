SET timezone = 'UTC-3';
CREATE TYPE rol AS ENUM ('Administrador', 'Doctor', 'Paciente', 'Personal');

CREATE TABLE usuarios (
    id_usuario SERIAL PRIMARY KEY,
    nombre_usuario VARCHAR(255) NOT NULL,
    contrasena VARCHAR(255) NOT NULL,
    nombre_completo VARCHAR(255) NOT NULL,
    rol rol NOT NULL,
    contacto VARCHAR(255) NOT NULL,
    CONSTRAINT unique_nombre_usuario_rol UNIQUE (nombre_usuario, rol)
);

CREATE TABLE historial_medico (
    id_historial SERIAL PRIMARY KEY,
    id_paciente INTEGER NOT NULL,
    id_doctor INTEGER NOT NULL,
    descripcion TEXT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_paciente) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_doctor) REFERENCES usuarios(id_usuario)
);