
CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE IF NOT EXISTS chunks (
  id BIGSERIAL PRIMARY KEY,
  repo TEXT NOT NULL,
  path TEXT NOT NULL,
  lang TEXT NOT NULL,
  type TEXT NOT NULL,
  symbol TEXT,
  line_start INT,
  line_end INT,
  sha TEXT,
  meta JSONB,
  embedding vector(768)
);
CREATE INDEX IF NOT EXISTS idx_chunks_embedding ON chunks USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
CREATE TABLE IF NOT EXISTS graphs_edges (
  src_id BIGINT,
  dst_id BIGINT,
  edge_type TEXT,
  weight REAL DEFAULT 1.0
);
