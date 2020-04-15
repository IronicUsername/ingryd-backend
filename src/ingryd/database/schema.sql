-- SQL Schema for the ingryd Postgres DB

-- Table Definitions:
-- Table 'production_db_version'
CREATE TABLE IF NOT EXISTS production_db_version (
  version int PRIMARY KEY CHECK (version >= 0) DEFAULT 0
);

-- Inserting default records:
-- Table `production_db_version`
INSERT INTO production_db_version (version) VALUES (0);
