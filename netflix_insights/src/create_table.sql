CREATE TABLE IF NOT EXISTS netflix_titles (
    show_id VARCHAR(15) PRIMARY KEY,
    type VARCHAR(20),
    title VARCHAR(255),
    director VARCHAR(255),
    cast VARCHAR(1000),
    country VARCHAR(255),
    date_added DATE,
    release_year INT,
    rating VARCHAR(10),
    duration VARCHAR(20),
    listed_in VARCHAR(500),
    description VARCHAR(1000)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
