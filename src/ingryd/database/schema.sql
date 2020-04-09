-- SQL Schema for the ingryd Postgres DB

-- Table Definitions:
CREATE TABLE IF NOT EXISTS users (
  id uuid PRIMARY KEY,
  fname varchar(60),
  lname varchar(60)
);

CREATE TABLE IF NOT EXISTS production_db_version (
  version int PRIMARY KEY CHECK (version >= 0) DEFAULT 0
);

-- Inserting default records:
-- Table `users`:
INSERT INTO users (id, fname, lname) VALUES ('00000000-0000-0000-0000-000000000000'::uuid, 'Jerry', 'Smith');

-- Table `production_db_version`
INSERT INTO production_db_version (version) VALUES (0);
