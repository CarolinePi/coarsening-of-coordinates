CREATE TABLE IF NOT EXISTS "location" (
    id SERIAL PRIMARY KEY,
    latitude DECIMAL NOT NULL,
    longitude DECIMAL NOT NULL
);

CREATE TABLE IF NOT EXISTS "user" (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(30) NOT NULL,
    location_id INTEGER NOT NULL,
    is_admin BOOLEAN NOT NULL,
    password_hash VARCHAR(255) NOT NULL UNIQUE,

    FOREIGN KEY(location_id) REFERENCES location (id)
);
