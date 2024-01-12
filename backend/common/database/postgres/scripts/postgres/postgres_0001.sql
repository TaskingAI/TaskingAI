CREATE TABLE IF NOT EXISTS app_admin (
    admin_id CHAR(16) PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    salt VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL ,
    token VARCHAR(255),
    created_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT,
    updated_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT
);


CREATE TABLE IF NOT EXISTS apikey (
    apikey_id CHAR(8) PRIMARY KEY,
    apikey VARCHAR(255) NOT NULL UNIQUE, -- todo: secret apikey
    name VARCHAR(255) NOT NULL,
    created_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT,
    updated_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT
);


CREATE TABLE IF NOT EXISTS model (
    model_id CHAR(8) NOT NULL PRIMARY KEY,
    model_schema_id VARCHAR(50) NOT NULL,
    provider_id VARCHAR(50) NOT NULL,
    provider_model_id VARCHAR(50) NOT NULL,
    name VARCHAR(255) NOT NULL,
    encrypted_credentials JSONB NOT NULL,
    display_credentials JSONB NOT NULL,
    created_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT,
    updated_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT
);
