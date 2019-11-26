import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# CREATE SCHEMA

create_schema = "CREATE SCHEMA IF NOT EXISTS sparkify;"
set_pointer = "SET search_path TO sparkify;"

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS events;"
staging_songs_table_drop  = "DROP TABLE IF EXISTS songs;"
songplay_table_drop       = "DROP TABLE IF EXISTS songplay;"
user_table_drop           = "DROP TABLE IF EXISTS users;"
song_table_drop           = "DROP TABLE IF EXISTS songs_table;"
artist_table_drop         = "DROP TABLE IF EXISTS artists;"
time_table_drop           = "DROP TABLE IF EXISTS time_table;"

# CREATE TABLES

staging_events_table_create = ("""
CREATE TABLE events (
    artist         VARCHAR(MAX),
    auth           VARCHAR(MAX),
    firstname      VARCHAR(MAX),
    gender         VARCHAR(MAX),
    iteminsession  INTEGER,
    lastname       VARCHAR(MAX),
    length         DECIMAL(9, 5),
    level          VARCHAR(MAX),
    location       VARCHAR(MAX),
    method         VARCHAR(MAX),
    page           VARCHAR(MAX),
    registration   VARCHAR(MAX),
    sessionid      INTEGER,
    song           VARCHAR(MAX),
    status         INTEGER,
    ts             TIMESTAMP,
    useragent      VARCHAR(MAX),
    userid         INTEGER
)
""")

staging_songs_table_create = ("""
CREATE TABLE songs (
    num_songs         INTEGER,
    artist_id         VARCHAR(MAX),
    artist_latitude   DECIMAL(7, 4),
    artist_longitude  DECIMAL(7, 4),
    artist_location   VARCHAR(MAX),
    artist_name       VARCHAR(MAX),
    song_id           VARCHAR(MAX),
    title             VARCHAR(MAX),
    duration          DECIMAL(9, 5),
    year              INTEGER
)
""")

songplay_table_create = ("""
CREATE TABLE songplay (
    songplay_id  INTEGER IDENTITY(0, 1),
    start_time   TIMESTAMP,
    user_id      VARCHAR(MAX),
    level        VARCHAR(MAX),
    song_id      VARCHAR(MAX),
    artist_id    VARCHAR(MAX),
    session_id   VARCHAR(MAX),
    location     VARCHAR(MAX),
    user_agent   VARCHAR(MAX)
)
""")

user_table_create = ("""
CREATE TABLE users (
    user_id     INTEGER NOT NULL,
    first_name  VARCHAR(MAX),
    last_name   VARCHAR(MAX),
    gender      VARCHAR(MAX),
    level       VARCHAR(MAX)
)
""")

song_table_create = ("""
CREATE TABLE songs_table (
    song_id    VARCHAR(MAX),
    title      VARCHAR(MAX),
    artist_id  VARCHAR(MAX),
    year       INTEGER,
    duration   DECIMAL(9, 5)
)
""")

artist_table_create = ("""
CREATE TABLE artists (
    artist_id  VARCHAR(MAX),
    name       VARCHAR(MAX),
    location   VARCHAR(MAX),
    latitude   DECIMAL(7, 4),
    longitude  DECIMAL(7, 4)
)
""")

time_table_create = ("""
CREATE TABLE time_table (
    start_time  TIMESTAMP,
    hour        INTEGER,
    day         VARCHAR(MAX),
    week        INTEGER,
    month       VARCHAR(MAX),
    year        INTEGER,
    weekday     VARCHAR(MAX)
)
""")

# STAGING TABLES
S3_LOG_DATA_TABLE = config['S3']['LOG_DATA']
S3_SONG_DATA_TABLE = config['S3']['SONG_DATA']
LOG_JSONPATH = config['S3']['LOG_JSONPATH']
IAM_ROLE = config['IAM_ROLE']['ARN']


staging_events_copy = ("""
    COPY events FROM {} 
    CREDENTIALS 'aws_iam_role={}'
    FORMAT AS JSON {} timeformat 'epochmillisecs';
""").format(S3_LOG_DATA_TABLE, IAM_ROLE, LOG_JSONPATH)

staging_songs_copy = ("""
COPY songs from {}
CREDENTIALS 'aws_iam_role={}'
JSON 'auto'
""").format(S3_SONG_DATA_TABLE, IAM_ROLE)

# FINAL TABLES

songplay_table_insert = ("""
INSERT INTO songplay (
  start_time, user_id, level, song_id, artist_id, session_id, location, user_agent
)
SELECT DISTINCT
    e.ts AS start_time,
    e.userid AS user_id,
    e.level AS level,
    s.song_id AS song_id,
    s.artist_id AS artist_id,
    e.sessionid AS session_id,
    e.location AS location,
    e.useragent AS user_agent
FROM sparkify."events" AS e
JOIN sparkify."songs" AS s
ON e.artist = s.artist_name AND e.song = s.title
WHERE e.page = 'NextSong'
""")

user_table_insert = ("""
INSERT INTO users
SELECT DISTINCT
    userid AS user_id,
    firstname AS first_name,
    lastname AS last_name,
    gender,
    level
FROM sparkify."events"
WHERE user_id IS NOT NULL
""")

song_table_insert = ("""
INSERT INTO songs_table
SELECT DISTINCT
    song_id,
    title,
    artist_id,
    year,
    duration
FROM sparkify."songs"
""")

artist_table_insert = ("""
INSERT INTO artists
SELECT DISTINCT
    artist_id,
    artist_name AS name,
    artist_location AS location,
    artist_latitude AS latitude,
    artist_longitude AS longitude
FROM sparkify."songs"
""")

time_table_insert = ("""
INSERT INTO time_table
SELECT
    ts,
    EXTRACT(hour from ts) AS hour,
    EXTRACT(day from ts) AS day,
    EXTRACT(week from ts) AS week,
    EXTRACT(month from ts) AS month,
    EXTRACT(year from ts) AS year,
    EXTRACT(dow from ts) AS weekday
FROM sparkify."events"
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [create_schema, set_pointer, staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [set_pointer, staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
