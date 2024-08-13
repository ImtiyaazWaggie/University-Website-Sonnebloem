
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

CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    id_number TEXT NOT NULL,
    dob DATE NOT NULL,
    phone_number TEXT NOT NULL,
    email TEXT NOT NULL,
    home_address TEXT NOT NULL,
    city TEXT NOT NULL,
    country TEXT NOT NULL,
    home_state TEXT NOT NULL,
    zipcode TEXT NOT NULL,

    -- Academic details
    subject_one TEXT,
    grade_one REAL,
    subject_two TEXT,
    grade_two REAL,
    subject_three TEXT,
    grade_three REAL,
    subject_four TEXT,
    grade_four REAL,
    subject_five TEXT,
    grade_five REAL,
    subject_six TEXT,
    grade_six REAL,
    subject_seven TEXT,
    grade_seven REAL,

    -- Programmes details
    first_choice TEXT NOT NULL,
    second_choice TEXT NOT NULL,

    -- Additional fields for file upload or other data
    file BLOB
);



CREATE TABLE IF NOT EXISTS events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,          -- Auto-incremented primary key
    event_name VARCHAR(255) NOT NULL,     -- Event name
    event_date DATE NOT NULL,             -- Event date
    start_time TIME NOT NULL,             -- Start time
    end_time TIME NOT NULL,               -- End time
    event_location VARCHAR(255) NOT NULL,       -- Event location
    event_description TEXT NOT NULL,            -- Event description
    event_type VARCHAR(50) NOT NULL,      -- Event type (e.g., Academic, Social)
    organizer_name VARCHAR(255) NOT NULL, -- Organizer's name
    organizer_email VARCHAR(255) NOT NULL UNIQUE, -- Organizer's email (unique constraint)
    organizer_phone VARCHAR(20),          -- Organizer's phone (optional)
    max_attendees INTEGER,                -- Maximum number of attendees (optional)
    file BLOB                     -- Event poster (stored as binary data)
);


CREATE TABLE IF NOT EXISTS bursaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bursary_name VARCHAR(255) NOT NULL,
    end_date DATE NOT NULL,
    bursary_introduction TEXT NOT NULL,
    bursary_provider_description TEXT NOT NULL,
    bursary_description TEXT NOT NULL,
    bursary_fields TEXT NOT NULL,
    bursary_cover TEXT NOT NULL,
    bursary_requirements TEXT NOT NULL,
    bursary_apply TEXT NOT NULL,
    provider_information TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);