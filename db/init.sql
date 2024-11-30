CREATE TYPE rol AS ENUM ('Administrador', 'Doctor', 'Paciente', 'Personal');

CREATE TABLE usuarios (
    id_usuario SERIAL PRIMARY KEY,
    nombre_usuario VARCHAR(255) NOT NULL,
    contrasena VARCHAR(255) NOT NULL,
    nombre_completo VARCHAR(255) NOT NULL,
    rol rol NOT NULL,
    contacto VARCHAR(255) NOT NULL
);
