CREATE TABLE prefixes (
    server_id INTEGER NOT NULL,
    prefix TEXT NOT NULL,
    PRIMARY KEY (server_id, prefix)
);

INSERT INTO prefixes VALUES (0, '!gbf ');