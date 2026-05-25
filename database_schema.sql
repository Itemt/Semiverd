-- database_schema.sql
-- Esquema de base de datos PostgreSQL para Semiverd MVP
-- Contiene las tablas DDL para usuarios, misiones, progreso, tips y recompensas.

-- 1. Tabla de usuarios (Guardianes Ecológicos)
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100),
    correo VARCHAR(200) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    apodo VARCHAR(50),
    puntos_totales INTEGER DEFAULT 0,
    nivel VARCHAR(50) DEFAULT 'Semilla',
    nivel_arbol INTEGER DEFAULT 1,
    racha_dias INTEGER DEFAULT 0,
    monedas_verdes INTEGER DEFAULT 0,
    foto_perfil TEXT, -- Foto de perfil guardada en Base64 o ruta
    face_encoding TEXT, -- Vector facial de 128 flotantes serializado como JSON
    activo BOOLEAN DEFAULT TRUE,
    fecha_registro TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    ultimo_acceso TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_usuarios_correo ON usuarios(correo);

-- 2. Tabla de Misiones (Retos Ecológicos)
CREATE TABLE misiones (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT NOT NULL,
    descripcion_corta VARCHAR(300),
    nombre_zona VARCHAR(100) NOT NULL, -- Río Caudal, Bosque de Humo, Ciudad Gris, Valle Energético
    guardianes VARCHAR(200) NOT NULL, -- Nombres de los personajes líderes (ej: 'Juliana y Giohan')
    categoria VARCHAR(50) NOT NULL, -- agua, bosque, ciudad, energia
    puntos_recompensa INTEGER DEFAULT 100,
    monedas_recompensa INTEGER DEFAULT 10,
    dificultad INTEGER DEFAULT 1,
    orden INTEGER DEFAULT 1,
    icono_emoji VARCHAR(10) DEFAULT '🌱',
    color_hex VARCHAR(7) DEFAULT '#4CAF50',
    activa BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Tabla de Progreso de Usuario (Relación de misiones y usuarios)
CREATE TABLE progreso_usuario (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    mision_id INTEGER NOT NULL REFERENCES misiones(id) ON DELETE CASCADE,
    estado VARCHAR(20) DEFAULT 'bloqueada', -- bloqueada, disponible, en_progreso, completada
    porcentaje_completado FLOAT DEFAULT 0.0,
    intentos INTEGER DEFAULT 0,
    puntos_ganados INTEGER DEFAULT 0,
    monedas_ganadas INTEGER DEFAULT 0,
    fecha_inicio TIMESTAMP WITH TIME ZONE,
    fecha_completada TIMESTAMP WITH TIME ZONE,
    fecha_actualizacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (usuario_id, mision_id)
);

CREATE INDEX idx_progreso_usuario ON progreso_usuario(usuario_id);
CREATE INDEX idx_progreso_mision ON progreso_usuario(mision_id);

-- 4. Tabla de Tips (Academia de Guardianes)
CREATE TABLE tips (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    contenido TEXT NOT NULL,
    categoria VARCHAR(80),
    icono_emoji VARCHAR(10) DEFAULT '💡',
    guardian_autor VARCHAR(100),
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 5. Tabla de Recompensas (Catálogo de Medallas)
CREATE TABLE recompensas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    icono_emoji VARCHAR(10) DEFAULT '🏅',
    tipo VARCHAR(50) DEFAULT 'medalla', -- medalla, titulo, objeto
    condicion VARCHAR(200),
    puntos_necesarios INTEGER DEFAULT 0
);

-- 6. Tabla de Recompensas de Usuario (Relación intermedia)
CREATE TABLE recompensas_usuario (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    recompensa_id INTEGER NOT NULL REFERENCES recompensas(id) ON DELETE CASCADE,
    fecha_obtenida TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
