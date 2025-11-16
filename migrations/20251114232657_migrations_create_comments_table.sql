-- +goose Up
-- +goose StatementBegin
CREATE TABLE IF NOT EXISTS comments (
    id BIGSERIAL PRIMARY KEY,
    mod_id BIGINT NOT NULL,
    author_id BIGINT NOT NULL,
    text TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'pending_moderation',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    edited_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_comments_mod_id ON comments(mod_id);
CREATE INDEX idx_comments_author_id ON comments(author_id);
CREATE INDEX idx_comments_status ON comments(status);
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
DROP TABLE IF EXISTS comments CASCADE;
-- +goose StatementEnd