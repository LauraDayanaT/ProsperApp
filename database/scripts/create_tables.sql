CREATE TABLE USUARIO (
    id_usuario     SERIAL PRIMARY KEY,
    nombre         VARCHAR(100) NOT NULL,
    email          VARCHAR(150) NOT NULL UNIQUE,
    contraseña     VARCHAR(255) NOT NULL,
    fecha_registro DATE NOT NULL DEFAULT CURRENT_DATE
);
CREATE TABLE PROYECTO (
    id_proyecto    SERIAL PRIMARY KEY,
    nombre         VARCHAR(150) NOT NULL,
    descripcion    TEXT,
    fecha_creacion DATE NOT NULL DEFAULT CURRENT_DATE,
    estado         VARCHAR(50) NOT NULL DEFAULT 'activo',
    id_usuario     INTEGER NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES USUARIO(id_usuario)
);
CREATE TABLE SECCION (
    id_seccion  SERIAL PRIMARY KEY,
    nombre      VARCHAR(100) NOT NULL,
    posicion    INTEGER NOT NULL,
    id_proyecto INTEGER NOT NULL,
    FOREIGN KEY (id_proyecto) REFERENCES PROYECTO(id_proyecto)
);
CREATE TABLE FUNCIONALIDAD (
    id_funcionalidad SERIAL PRIMARY KEY,
    titulo           VARCHAR(200) NOT NULL,
    historia_usuario TEXT,
    notas_diseño     TEXT,
    fragmento_codigo TEXT,
    decision_tecnica TEXT,
    fecha_creacion   DATE NOT NULL DEFAULT CURRENT_DATE,
    id_seccion       INTEGER NOT NULL,
    FOREIGN KEY (id_seccion) REFERENCES SECCION(id_seccion)
);
CREATE TABLE SUBTAREA (
    id_subtarea      SERIAL PRIMARY KEY,
    descripcion      TEXT NOT NULL,
    completada       BOOLEAN NOT NULL DEFAULT FALSE,
    id_funcionalidad INTEGER NOT NULL,
    FOREIGN KEY (id_funcionalidad) REFERENCES FUNCIONALIDAD(id_funcionalidad)
);