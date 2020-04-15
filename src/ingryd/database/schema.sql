-- SQL Schema for the ingryd Postgres DB

-- Table Definitions:
-- Table 'employees'
CREATE TABLE IF NOT EXISTS employees (
  id serial PRIMARY KEY,
  fname varchar(60) NOT NULL,
  lname varchar(60) NOT NULL,
  password varchar(100) NOT NULL,
  email varchar(355) NOT NULL,
  last_login timestamp,
  birthday date,
  status text,
  position_id int,
  address_id int
);

-- Table 'supervisors'
CREATE TABLE IF NOT EXISTS supervisors (
  id serial PRIMARY KEY,
  employee_id int,
  created_at timestamp
);

-- Table 'positions'
CREATE TABLE IF NOT EXISTS positions(
  id serial PRIMARY KEY,
  name varchar(80)
);

-- Table 'teams'
CREATE TABLE IF NOT EXISTS teams (
  id serial PRIMARY KEY,
  name varchar(100),
  supervisor_id int,
  members json,
  created_at timestamp
);

-- Table 'vacation'
CREATE TABLE IF NOT EXISTS vacation (
  id int PRIMARY KEY,
  name varchar(100),
  color varchar(6)
);

-- Table 'production_db_version'
CREATE TABLE IF NOT EXISTS production_db_version (
  version int PRIMARY KEY CHECK (version >= 0) DEFAULT 0
);

-- Inserting default records:
-- Table `production_db_version`
INSERT INTO production_db_version (version) VALUES (0);
