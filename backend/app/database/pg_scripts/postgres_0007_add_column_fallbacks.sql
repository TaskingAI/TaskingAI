-- add column to model: fallbacks
ALTER TABLE model
ADD COLUMN fallbacks TEXT NOT NULL DEFAULT '{}';
