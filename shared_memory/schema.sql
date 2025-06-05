CREATE TABLE IF NOT EXISTS memory (
    id TEXT PRIMARY KEY,
    timestamp TEXT,
    input_source TEXT,
    format TEXT,
    intent TEXT,
    extracted_fields TEXT,
    action_triggered TEXT,
    trace TEXT
);