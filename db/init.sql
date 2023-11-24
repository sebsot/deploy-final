CREATE DATABASE dbproyecto;
USE dbproyecto;


CREATE TABLE participantes (
  NOMBRE_ALUMNO VARCHAR(50),
  CARRERA VARCHAR(50)
);


INSERT INTO participantes
  (NOMBRE_ALUMNO, CARRERA)
VALUES
  ('Sebastian S. Bertani', 'Ingenieria'),
  ('German A. Lechner', 'Ingenieria');