DROP TABLE IF EXISTS links;

CREATE TABLE links (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    short_url TEXT,
    long_url TEXT,
    clicks INTEGER DEFAULT 0
);