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
    encrypted_apikey TEXT NOT NULL UNIQUE,
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
    created_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT,
    updated_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT
);
CREATE INDEX IF NOT EXISTS model_created_timestamp_idx ON model (created_timestamp);
CREATE INDEX IF NOT EXISTS model_name_idx ON model (name);

CREATE TABLE IF NOT EXISTS action (
    action_id CHAR(24) NOT NULL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    openapi_schema JSONB NOT NULL,
    authentication JSONB NOT NULL DEFAULT '{}',
    extra jsonb NOT NULL DEFAULT '{}',
    metadata JSONB NOT NULL DEFAULT '{}',
    created_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT,
    updated_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT
);
CREATE INDEX IF NOT EXISTS action_created_timestamp_idx ON action (created_timestamp);
CREATE INDEX IF NOT EXISTS action_name_idx ON action (name);


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
    extra jsonb NOT NULL DEFAULT '{}',
    metadata JSONB NOT NULL DEFAULT '{}',
    created_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT,
    updated_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT
);
CREATE INDEX IF NOT EXISTS collection_created_timestamp_idx ON collection (created_timestamp);
CREATE INDEX IF NOT EXISTS collection_name_idx ON collection (name);


CREATE TABLE IF NOT EXISTS record (
    collection_id CHAR(24) NOT NULL REFERENCES collection (collection_id) ON DELETE CASCADE,
    record_id CHAR(24) NOT NULL ,
    num_chunks INTEGER NOT NULL DEFAULT 0,
    title TEXT NOT NULL,
    type TEXT NOT NULL,
    content TEXT NOT NULL,
    status TEXT NOT NULL,
    extra jsonb NOT NULL DEFAULT '{}',
    metadata JSONB NOT NULL DEFAULT '{}',
    created_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT,
    updated_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT,
    PRIMARY KEY (collection_id, record_id)
);
CREATE INDEX IF NOT EXISTS record_collection_id_created_timestamp_idx ON record (collection_id, created_timestamp);


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

    num_chats INTEGER NOT NULL DEFAULT 0,
    memory JSONB NOT NULL DEFAULT '{}',
    extra jsonb NOT NULL DEFAULT '{}',
    metadata JSONB NOT NULL DEFAULT '{}',

    created_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT,
    updated_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT
);
CREATE INDEX IF NOT EXISTS assistant_created_timestamp_idx ON assistant (created_timestamp);
CREATE INDEX IF NOT EXISTS assistant_name_idx ON assistant (name);


CREATE TABLE IF NOT EXISTS chat (
    assistant_id CHAR(24) NOT NULL,
    chat_id CHAR(24) NOT NULL,
    memory JSONB NOT NULL DEFAULT '{}',
    num_messages INTEGER NOT NULL DEFAULT 0,
    extra jsonb NOT NULL DEFAULT '{}',
    metadata JSONB NOT NULL DEFAULT '{}',
    created_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT,
    updated_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT,
    PRIMARY KEY (assistant_id, chat_id)
);
CREATE INDEX IF NOT EXISTS chat_assistant_id_created_timestamp_idx ON chat (assistant_id, created_timestamp);

CREATE TABLE IF NOT EXISTS message (
    message_id CHAR(24) NOT NULL,
    chat_id CHAR(24) NOT NULL,
    assistant_id CHAR(24) NOT NULL,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    num_tokens INTEGER NOT NULL DEFAULT 0,
    extra jsonb NOT NULL DEFAULT '{}',
    metadata JSONB NOT NULL DEFAULT '{}',
    created_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT,
    updated_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT,
    PRIMARY KEY (assistant_id, chat_id, message_id)
);
