-- Drop existing tables if they exist
DROP TABLE IF EXISTS staging_events;
DROP TABLE IF EXISTS staging_songs;
DROP TABLE IF EXISTS songplays;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS songs;
DROP TABLE IF EXISTS artists;
DROP TABLE IF EXISTS time;

-- Create staging tables
CREATE TABLE staging_events (
    artist          VARCHAR(255),
    auth            VARCHAR(50),
    firstName       VARCHAR(50),
    gender          CHAR(1),
    itemInSession   INT,
    lastName        VARCHAR(50),
    length          FLOAT,
    level           VARCHAR(10),
    location        VARCHAR(255),
    method          VARCHAR(10),
    page            VARCHAR(50),
    registration    BIGINT,
    sessionId       INT,
    song            VARCHAR(255),
    status          INT,
    ts              BIGINT,
    userAgent       VARCHAR(255),
    userId          INT
);

CREATE TABLE staging_songs (
    num_songs           INT,
    artist_id           VARCHAR(50),
    artist_latitude     FLOAT,
    artist_longitude    FLOAT,
    artist_location     VARCHAR(255),
    artist_name         VARCHAR(255),
    song_id             VARCHAR(50),
    title               VARCHAR(255),
    duration            FLOAT,
    year                INT
);

-- Create fact table (songplays)
CREATE TABLE songplays (
    songplay_id    INT IDENTITY(0,1) PRIMARY KEY,
    start_time     TIMESTAMP NOT NULL,
    user_id        INT NOT NULL,
    level          VARCHAR(10),
    song_id        VARCHAR(50),
    artist_id      VARCHAR(50),
    session_id     INT,
    location       VARCHAR(255),
    user_agent     VARCHAR(255)
);

-- Create dimension tables
CREATE TABLE users (
    user_id        INT PRIMARY KEY,
    first_name     VARCHAR(50),
    last_name      VARCHAR(50),
    gender         CHAR(1),
    level          VARCHAR(10)
);

CREATE TABLE songs (
    song_id       VARCHAR(50) PRIMARY KEY,
    title         VARCHAR(255),
    artist_id     VARCHAR(50) NOT NULL,
    year          INT,
    duration      FLOAT
);

CREATE TABLE artists (
    artist_id     VARCHAR(50) PRIMARY KEY,
    name          VARCHAR(255),
    location      VARCHAR(255),
    latitude      FLOAT,
    longitude     FLOAT
);

CREATE TABLE time (
    start_time    TIMESTAMP PRIMARY KEY,
    hour          INT,
    day           INT,
    week          INT,
    month         INT,
    year          INT,
    weekday       INT
);
