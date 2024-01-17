CREATE EXTENSION IF NOT EXISTS vector;


CREATE TABLE IF NOT EXISTS app_admin (
    admin_id CHAR(16) PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    salt TEXT NOT NULL,
    password_hash TEXT NOT NULL ,
    token TEXT,
    created_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT,
    updated_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT
);


CREATE TABLE IF NOT EXISTS apikey (
    apikey_id CHAR(8) PRIMARY KEY,
    apikey TEXT NOT NULL UNIQUE, -- todo: secret apikey
    name TEXT NOT NULL,
    created_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT,
    updated_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT
);


CREATE TABLE IF NOT EXISTS model (
    model_id CHAR(8) NOT NULL PRIMARY KEY,
    model_schema_id TEXT NOT NULL,
    provider_id TEXT NOT NULL,
    provider_model_id TEXT NOT NULL,
    type TEXT NOT NULL,
    name TEXT NOT NULL,
    encrypted_credentials JSONB NOT NULL,
    display_credentials JSONB NOT NULL,
    -- todo: add metadata
    created_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT,
    updated_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT
);


CREATE TABLE IF NOT EXISTS action (
    action_id CHAR(24) NOT NULL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    openapi_schema JSONB NOT NULL,
    authentication JSONB NOT NULL DEFAULT '{}',
    -- todo: add metadata
    created_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT,
    updated_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT
);


CREATE TABLE IF NOT EXISTS collection (
    collection_id CHAR(24) PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    num_chunks INTEGER NOT NULL DEFAULT 0,
    num_records INTEGER NOT NULL DEFAULT 0,
    capacity INTEGER NOT NULL,
    embedding_model_id CHAR(8) NOT NULL,
    embedding_size INTEGER NOT NULL,
    status TEXT NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}',
    created_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT,
    updated_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT
);


CREATE TABLE IF NOT EXISTS record (
    collection_id CHAR(24) NOT NULL REFERENCES collection (collection_id) ON DELETE CASCADE,
    record_id CHAR(24) NOT NULL ,
    num_chunks INTEGER NOT NULL DEFAULT 0,
    title TEXT NOT NULL,
    type TEXT NOT NULL,
    content TEXT NOT NULL,
    status TEXT NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}',
    created_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT,
    updated_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT,
    PRIMARY KEY (collection_id, record_id)
);


CREATE TABLE IF NOT EXISTS assistant (
    assistant_id CHAR(24) NOT NULL PRIMARY KEY,
    model_id CHAR(8) NOT NULL,

    name VARCHAR(256) NOT NULL  DEFAULT '',
    description VARCHAR(512) NOT NULL DEFAULT '',
    system_prompt_template JSONB NOT NULL DEFAULT '[]',

    tools JSONB DEFAULT '[]',
    tool_configs JSONB DEFAULT '{}',
    retrievals JSONB DEFAULT '[]',
    retrieval_configs JSONB DEFAULT '{}',

    memory JSONB NOT NULL DEFAULT '{}',
    metadata JSONB NOT NULL DEFAULT '{}',

    created_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT,
    updated_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT
);


CREATE TABLE IF NOT EXISTS chat (
    assistant_id CHAR(24) NOT NULL,
    chat_id CHAR(24) NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}',
    memory JSONB NOT NULL DEFAULT '{}',
    created_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT,
    updated_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT,
    PRIMARY KEY (assistant_id, chat_id)
);


CREATE TABLE IF NOT EXISTS message (
    message_id CHAR(24) NOT NULL,
    chat_id CHAR(24) NOT NULL,
    assistant_id CHAR(24) NOT NULL,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}',
    created_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT,
    updated_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT,
    PRIMARY KEY (assistant_id, chat_id, message_id)
);


--todo: index on created_timestamp and name for each table
