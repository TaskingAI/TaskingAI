CREATE EXTENSION IF NOT EXISTS vector;

-- Create stats table
CREATE TABLE IF NOT EXISTS stats (
    num_collections INTEGER NOT NULL DEFAULT 0
);

INSERT INTO stats (num_collections) VALUES (0);

-- Create collection table
CREATE TABLE IF NOT EXISTS collection (

    collection_id VARCHAR(256) PRIMARY KEY,
    project_id VARCHAR(256) NOT NULL,

    num_chunks INTEGER NOT NULL DEFAULT 0,
    num_records INTEGER NOT NULL DEFAULT 0,
    text_bytes BIGINT NOT NULL DEFAULT 0,
    embedding_bytes BIGINT NOT NULL DEFAULT 0,

    capacity INTEGER NOT NULL,
    indexed BOOLEAN NOT NULL DEFAULT FALSE,

    embedding_size INTEGER NOT NULL,

    configs JSONB, -- store collection configs

    created_timestamp BIGINT NOT NULL,
    updated_timestamp BIGINT NOT NULL
);


-- future: partition on project_id

CREATE TABLE IF NOT EXISTS record (
    record_id VARCHAR(30) NOT NULL PRIMARY KEY,
    collection_id VARCHAR(30) NOT NULL REFERENCES collection (collection_id) ON DELETE CASCADE,
    project_id CHAR(8) NOT NULL,

    status INTEGER NOT NULL, -- processing, ready, failed
    status_message VARCHAR(512) DEFAULT '',
    num_chunks INTEGER NOT NULL DEFAULT 0,

    text_bytes INT NOT NULL DEFAULT 0,
    embedding_bytes INT NOT NULL DEFAULT 0,

    type INTEGER NOT NULL,
    content JSONB NOT NULL,

    metadata JSONB NOT NULL DEFAULT '{}',

    updated_timestamp BIGINT NOT NULL,
    created_timestamp BIGINT NOT NULL,
    retry_count INTEGER NOT NULL DEFAULT 0
);

-- Create record collection_id created_timestamp index
CREATE INDEX IF NOT EXISTS record_collection_id_created_timestamp_idx ON record (collection_id, created_timestamp);
-- create partial index on status and updated_timestamp
CREATE INDEX IF NOT EXISTS record_status_updated_timestamp_idx ON record (status, updated_timestamp)
WHERE status = 1 OR status = 3;

-- future: partition on collection_id
