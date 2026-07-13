INSERT INTO USUARIO (nombre, email, contraseña, fecha_registro) VALUES
('Laura Dayana', 'laura@email.com', '1234', '2026-01-10'),
('Ceir Enrique', 'enrique@email.com', '1234', '2026-01-15'),
('Geraldin Nazly', 'geraldin@email.com', '1234', '2026-02-01');

INSERT INTO PROYECTO (nombre, descripcion, fecha_creacion, estado, id_usuario) VALUES
('MoodTracker', 'App para registrar tu estado de ánimo diario con estadísticas', '2026-01-11', 'activo', 1),
('PixelDungeon AI', 'Videojuego de mazmorras generadas con inteligencia artificial', '2026-01-20', 'activo', 2),
('StudyFlow', 'Herramienta tipo Pomodoro para estudiantes universitarios', '2026-02-05', 'pausado', 3);

INSERT INTO SECCION (nombre, posicion, id_proyecto) VALUES
('backlog', 1, 1),
('doing', 2, 1),
('completed', 3, 1),
('backlog', 1, 2),
('doing', 2, 2),
('backlog', 1, 3);

INSERT INTO FUNCIONALIDAD (titulo, historia_usuario, notas_diseño, fecha_creacion, id_seccion) VALUES
('Registro de humor diario', 'Como usuario quiero registrar cómo me siento cada día', 'Usar emojis como selector de humor', '2026-01-12', 1),
('Gráfica de progreso emocional', 'Como usuario quiero ver mi historial de emociones', 'Gráfica de línea por semana', '2026-01-12', 2),
('Notificaciones diarias', 'Como usuario quiero que me recuerde registrar mi humor', 'Notificación a las 8pm', '2026-01-13', 1),
('Generador de mazmorras', 'Como jugador quiero que cada partida sea diferente', 'Algoritmo procedural con semillas', '2026-01-21', 4),
('Sistema de combate', 'Como jugador quiero pelear contra enemigos', 'Turnos con dados virtuales', '2026-01-22', 5),
('Temporizador Pomodoro', 'Como estudiante quiero sesiones de 25 minutos', 'Círculo animado con cuenta regresiva', '2026-02-06', 6);

INSERT INTO SUBTAREA (descripcion, completada, id_funcionalidad) VALUES
('Diseñar pantalla de registro de humor', TRUE, 1),
('Guardar registros en la base de datos', FALSE, 1),
('Validar que solo se registre una vez al día', FALSE, 1),
('Conectar datos con librería de gráficas', TRUE, 2),
('Filtrar por semana y mes', FALSE, 2),
('Configurar sistema de notificaciones', FALSE, 3),
('Diseñar algoritmo de generación', TRUE, 4),
('Probar con 10 semillas diferentes', FALSE, 4),
('Crear clases de enemigos básicos', TRUE, 5),
('Implementar lógica de turnos', FALSE, 5),
('Diseñar interfaz del temporizador', FALSE, 6),
('Agregar sonido al terminar sesión', FALSE, 6);