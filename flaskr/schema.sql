
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY  AUTOINCREMENT,                   -- Unique identifier for each user
    username VARCHAR(255)  UNIQUE NOT NULL,                 -- Unique username for the user
    first_name VARCHAR(255) NOT NULL,                       -- First name of the user
    last_name VARCHAR(255) NOT NULL,                        -- Last name of the user
    phone_number VARCHAR(20),                               -- Phone number of the user
    email VARCHAR(255) NOT NULL UNIQUE,                     -- Email address of the user
    password TEXT NOT NULL,                                 -- Hashed password for security
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP          -- Timestamp of when the record was created
);

CREATE TABLE IF NOT EXISTS programmes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    programme_name VARCHAR(255) NOT NULL,
    programme_code VARCHAR(50) NOT NULL UNIQUE,
    programme_length VARCHAR(50),
    programme_stream VARCHAR(100),
    programme_description TEXT,
    qualification_type VARCHAR(50) CHECK (qualification_type IN ('Certificate', 'Degree', 'Diploma')),
    graduate_type VARCHAR(50) CHECK (graduate_type IN ('Undergraduate', 'Postgraduate')),
    study_type VARCHAR(50) CHECK (study_type IN ('Full-Time', 'Part-Time')),
    programme_faculty VARCHAR(100) CHECK (programme_faculty IN ('Commerce', 'Engineering', 'Health', 'Humanities', 'Law', 'Science'))
);

CREATE TABLE IF NOT EXISTS news_posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,        -- Unique ID for each news post
    headline VARCHAR(255) NOT NULL,          -- Headline of the news post
    sub_headline VARCHAR(255),               -- Optional subheadline
    author VARCHAR(255),                     -- Author of the news post
    introduction TEXT NOT NULL,             -- Introduction/Lead
    paragraph_one TEXT NOT NULL,
    paragraph_two TEXT NOT NULL, 
    paragraph_three TEXT NOT NULL, 
    paragraph_four TEXT NOT NULL,                -- Main body of the news post
    quotes TEXT,                            -- Optional quotes
    tags VARCHAR(255),                      -- Tags for the news post
    file BLOB,                              -- URL or path to the uploaded file (thumbnail)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Timestamp of when the post was created
);