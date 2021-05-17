-- SQLite
CREATE TABLE feedback2 (
    id INTEGER NOT NULL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    feedback TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO feedback2(id, user_id, feedback) SELECT * FROM feedback;
DROP TABLE feedback;
ALTER TABLE feedback2 RENAME TO feedback;