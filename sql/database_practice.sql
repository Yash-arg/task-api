-- Week 3 / Day 1: database_practice.sql
-- Type every statement yourself in psql. Do not paste blindly.

-- ---------- 1. CREATE ----------
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ---------- 2. INSERT ----------
INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com');
INSERT INTO users (name, email) VALUES ('Oslo', 'Oslo@example.com');
INSERT INTO users (name, email) VALUES ('Nico', 'Nico@example.com');
INSERT INTO users (name, email) VALUES ('Exie', 'Exie@example.com');
INSERT INTO users (name, email) VALUES ('Peter', 'Peter@example.com');
-- TODO: insert 4 more users

-- ---------- 3. SELECT ----------
SELECT * FROM users;
-- TODO: select only name and email
-- TODO: select one user by email (WHERE)
-- TODO: select users whose id is IN (1, 3)
-- TODO: WHERE ... AND ... / OR ...
-- TODO: ORDER BY created_at DESC
-- TODO: LIMIT 2 OFFSET 2 (why do you need ORDER BY with it?)

-- ---------- 4. UPDATE ----------
-- TODO: change one user's name (WHERE on the primary key)
-- TODO: SELECT after, confirm only one row changed

-- ---------- 5. DELETE ----------
-- TODO: delete one user by id
-- TODO: SELECT to confirm

-- ---------- 6. BREAK IT ON PURPOSE ----------
-- TODO: insert a duplicate email -> read the exact error
-- TODO: insert a row with NULL name -> read the exact error

-- ---------- 7. ANSWER IN WRITING ----------
-- Why is email UNIQUE?
--   >
-- Why is id the PRIMARY KEY?
--   >
-- Why SERIAL instead of picking ids yourself?
--   >