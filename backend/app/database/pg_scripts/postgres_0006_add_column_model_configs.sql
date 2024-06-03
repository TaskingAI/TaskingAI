-- add column to model: configs
ALTER TABLE model
ADD COLUMN configs JSONB NOT NULL DEFAULT '{}';
