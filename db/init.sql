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

CREATE TABLE citas (
    id_paciente INTEGER NOT NULL,
    id_doctor INTEGER NOT NULL,
    nombre_doctor VARCHAR(255) NOT NULL,
    nombre_paciente VARCHAR(255) NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_cita bigint GENERATED ALWAYS AS IDENTITY,
    FOREIGN KEY (id_paciente) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_doctor) REFERENCES usuarios(id_usuario)
);

CREATE TABLE inventario_farmaceutico (
    id_medicamento SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    cantidad_disponible INTEGER NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    informacion VARCHAR(255) NOT NULL
);

CREATE TABLE prescripcion(
    id_prescripcion SERIAL PRIMARY KEY,
    id_medicamento INTEGER NOT NULL,
    id_paciente INTEGER NOT NULL,
    nombre_doctor VARCHAR(255) NOT NULL,
    nombre_paciente VARCHAR(255) NOT NULL,
    id_doctor INTEGER NOT NULL,
    instrucciones VARCHAR(255) NOT NULL,
    nombre_medicamento VARCHAR(255) NOT  NULL
);


INSERT INTO inventario_farmaceutico (nombre, cantidad_disponible, precio, informacion)
VALUES
    ('Paracetamol 500mg', 100, 1500, 'Analgésico y antipirético usado para aliviar dolores leves y reducir la fiebre.'),
    ('Ibuprofeno 200mg', 200, 2500, 'Antiinflamatorio no esteroideo usado para tratar dolor e inflamación.');

