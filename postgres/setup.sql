-- sudo -u postgres psql -f setup.sql
DROP DATABASE IF EXISTS hothouse;
DROP USER IF EXISTS hotapp;

CREATE DATABASE hothouse;
CREATE USER hotapp WITH ENCRYPTED PASSWORD 'hothouse';
GRANT ALL PRIVILEGES ON DATABASE hothouse TO hotapp;

\c hothouse;

-- i hate postgres
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO hotapp;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE, SELECT ON SEQUENCES TO hotapp;

CREATE TABLE sample(
	id BIGSERIAL PRIMARY KEY,
	sensor_id VARCHAR(30) NOT NULL,
	read_dt TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	data JSONB
);

CREATE TABLE room(
	room_id VARCHAR(30) PRIMARY KEY,
	sensor_id VARCHAR(30) NOT NULL,
	data JSONB
);