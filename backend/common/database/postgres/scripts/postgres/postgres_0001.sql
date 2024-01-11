CREATE TABLE IF NOT EXISTS project (
    project_id CHAR(8) NOT NULL PRIMARY KEY,
    num_functions INTEGER NOT NULL DEFAULT 0,
    num_actions INTEGER NOT NULL DEFAULT 0,
    delete_flag BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS function (
    function_id CHAR(24) NOT NULL,
    project_id CHAR(8) NOT NULL REFERENCES project(project_id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    parameters JSONB NOT NULL,
    created_timestamp bigint NOT NULL,
    updated_timestamp bigint NOT NULL,
    PRIMARY KEY (project_id, function_id)
);

-- Create function project_id created_timestamp index
CREATE INDEX IF NOT EXISTS function_project_id_created_timestamp_idx ON function (project_id, created_timestamp);


CREATE TABLE IF NOT EXISTS action (
    action_id CHAR(24) NOT NULL,
    project_id CHAR(8) NOT NULL REFERENCES project(project_id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    api_schema JSONB NOT NULL, -- schema is a reserved word so we use api_schema instead
    authentication JSONB NOT NULL DEFAULT '{}',
    created_timestamp bigint NOT NULL,
    updated_timestamp bigint NOT NULL,
    PRIMARY KEY (project_id, action_id)
);
