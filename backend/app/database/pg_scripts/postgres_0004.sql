CREATE TABLE IF NOT EXISTS bundle_instance (

    -- primary key
    bundle_instance_id TEXT NOT NULL PRIMARY KEY,

    -- info
    name TEXT NOT NULL DEFAULT '',
    encrypted_credentials JSONB NOT NULL DEFAULT '{}',
    display_credentials JSONB NOT NULL DEFAULT '{}',
    bundle_id VARCHAR(127) NOT NULL,

    -- data
    metadata JSONB NOT NULL DEFAULT '{}',
    extra JSONB NOT NULL DEFAULT '{}',

    -- logical delete
    delete_flag BOOLEAN NOT NULL DEFAULT FALSE,

    -- timestamps
    created_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT,
    updated_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT
);

CREATE INDEX IF NOT EXISTS bundle_instance_created_timestamp_idx ON bundle_instance (created_timestamp);
CREATE INDEX IF NOT EXISTS bundle_instance_name_idx ON bundle_instance (name);
