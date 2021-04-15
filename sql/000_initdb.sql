-- sqlite
CREATE TABLE alt_names (
    server_id INTEGER NOT NULL,
    alt_name TEXT NOT NULL,
    char_name TEXT NOT NULL,
    PRIMARY KEY (server_id, alt_name)
);

CREATE TABLE aliases (
    server_id INTEGER NOT NULL,
    alias_name TEXT NOT NULL,
    char_name TEXT NOT NULL,
    char_version TEXT NOT NULL,
    PRIMARY KEY (server_id, alias_name)
);

CREATE TABLE feedback (
    id INTEGER NOT NULL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    feedback TEXT NOT NULL
);

CREATE TABLE errors (
    id INTEGER NOT NULL PRIMARY KEY,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    stacktrace TEXT NOT NULL,
    command TEXT NOT NULL
);