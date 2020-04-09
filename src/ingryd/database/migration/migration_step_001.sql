ALTER TABLE users
    ADD COLUMN test varchar;

INSERT INTO users (id, fname, lname) VALUES
    ('00000000-0000-0000-0000-000000000001'::uuid, 'Rick', 'Sanchez'),
    ('00000000-0000-0000-0000-000000000002'::uuid, 'Morty', 'Smith');

-- Migration Step 001
-- Changes:
-- JUST TESTING! REMOVE CONTENTS
