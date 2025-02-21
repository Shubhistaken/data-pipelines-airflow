class SqlQueries:
    songplay_table_insert = ("""
        INSERT INTO songplays (...)
    """)

    song_table_insert = ("""
        INSERT INTO songs (...)
    """)

    user_table_insert = ("""
        INSERT INTO users (...)
    """)

    artist_table_insert = ("""
        INSERT INTO artists (...)
    """)

    time_table_insert = ("""
        INSERT INTO time (...)
    """)

    all_data_quality_count_checks = [
        {"sql": "SELECT COUNT(*) FROM songplays", "expected_result": 1},
        {"sql": "SELECT COUNT(*) FROM users", "expected_result": 1}
    ]

    all_data_quality_null_checks = [
        {"sql": "SELECT COUNT(*) FROM songplays WHERE songid IS NULL", "expected_result": 0}
    ]
