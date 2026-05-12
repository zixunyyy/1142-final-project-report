DROP TABLE IF EXISTS records;

CREATE TABLE records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_text TEXT NOT NULL,
    emotion TEXT NOT NULL,
    intensity INTEGER,
    suggestion TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
