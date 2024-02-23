--create table presupuesto(
--	nuevos_gastos int not null,
	--gastos_acumulados int not null,
	--ajuste int not null
--)
--ALTER TABLE presupuesto
--RENAME ajuste TO Monto;
--ALTER TABLE presupuesto
--ADD COLUMN categoria varchar(50);
--ALTER TABLE viajes
--ALTER COLUMN monto TYPE int;
--ALTER TABLE presupuesto
--ALTER COLUMN categoria SET POSITION BEFORE fecha;
--select * from presupuesto;



--CREATE TABLE viajes (
--	 id SERIAL PRIMARY KEY,
 --  usuario VARCHAR(100),
 -- fecha varchar(15),
 -- monto int,
--	categoria varchar(50)
  
--);

-- Tabla para rutinas de ejercicios y metas
--CREATE TABLE Rutinas (
    --rutina_id SERIAL PRIMARY KEY,
  --  nombre_usuario VARCHAR(50),
  --  fecha DATE,
  --  ejercicio VARCHAR(100),
  --  duracion FLOAT,
  --  meta FLOAT,
  --  completada BOOLEAN DEFAULT FALSE
--);

--SELECT * FROM Rutinas

--CREATE TABLE ConsumoAgua (
  --  id SERIAL PRIMARY KEY,
   -- nombre_usuario VARCHAR(50),
   -- fecha DATE,
   -- cantidad FLOAT
--);

-- CREATE TABLE HabitosLectura (
-- id SERIAL PRIMARY KEY,
-- nombre_usuario VARCHAR(50),
-- titulo_libro VARCHAR(255),
-- autor_libro VARCHAR(255),
-- fecha DATE,
-- meta_lectura INT
-- );
-- CREATE TABLE RecomendacionesLibros (
--     id SERIAL PRIMARY KEY,
--     titulo VARCHAR(255),
--     autor VARCHAR(255),
--     genero VARCHAR(100),
--     puntaje FLOAT,
--     popularidad INT
-- );

-- INSERT INTO RecomendacionesLibros (titulo, autor, genero, puntaje, popularidad)
-- VALUES ('El nombre del viento', 'Patrick Rothfuss', 'Fantasía', 4.5, 100),
--        ('1984', 'George Orwell', 'Ciencia ficción', 4.6, 120),
--        ('Orgullo y prejuicio', 'Jane Austen', 'Clásico', 4.4, 90);

-- CREATE TABLE GastosAlimentos (
--     id SERIAL PRIMARY KEY,
--     nombre_usuario VARCHAR(50),
--     fecha DATE,
--     monto DECIMAL,
--     categoria VARCHAR(100),
--     meta_calorias INT,
--     presupuesto DECIMAL
-- );

-- CREATE TABLE ProyectosPersonales (
--     id SERIAL PRIMARY KEY,
--     nombre_usuario VARCHAR(50),
--     tarea VARCHAR(255),
--     fecha_limite DATE,
--     completada BOOLEAN
-- );

CREATE TABLE RegistroSueño (
    id SERIAL PRIMARY KEY,
    nombre_usuario VARCHAR(50),
    fecha DATE,
    horas_sueño INT
);






