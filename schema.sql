CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    language TEXT NOT NULL CHECK (language IN ('java', 'python')),
    source_code TEXT NOT NULL,
    quality_score INTEGER NOT NULL CHECK (quality_score BETWEEN 0 AND 100),
    issues_json TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_reviews_created_at
ON reviews(created_at);
