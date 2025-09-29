-- migrate:up
CREATE TABLE IF NOT EXISTS comments (
  id BIGSERIAL PRIMARY KEY,
  mod_id BIGINT NOT NULL,
  author_id BIGINT NOT NULL,
  text TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  edited_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_comments_mod_id ON comments (mod_id);

-- migrate:down
DROP TABLE IF EXISTS comments;

