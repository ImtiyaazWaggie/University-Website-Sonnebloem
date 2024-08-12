DROP TABLE IF EXISTS user;

CREATE TABLE users (
    id INTEGER PRIMARY KEY  AUTOINCREMENT,                   -- Unique identifier for each user
    username VARCHAR(255)  UNIQUE NOT NULL,                 -- Unique username for the user
    first_name VARCHAR(255) NOT NULL,                       -- First name of the user
    last_name VARCHAR(255) NOT NULL,                        -- Last name of the user
    phone_number VARCHAR(20),                               -- Phone number of the user
    email VARCHAR(255) NOT NULL UNIQUE,                     -- Email address of the user
    password TEXT NOT NULL,                                 -- Hashed password for security
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP          -- Timestamp of when the record was created
);
