-- Activar l’extensió pgvector
CREATE EXTENSION IF NOT EXISTS vector;

-- Taula d’actors
CREATE TABLE IF NOT EXISTS actors (
  id SERIAL PRIMARY KEY,
  name VARCHAR(200) NOT NULL,
  tmdb_id INTEGER UNIQUE,
  imdb_id VARCHAR(32),
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Taula d’embeddings facials
CREATE TABLE IF NOT EXISTS actor_embeddings (
  id SERIAL PRIMARY KEY,
  actor_id INTEGER NOT NULL REFERENCES actors(id) ON DELETE CASCADE,
  embedding VECTOR(128), -- vector de 128 dimensions
  source_url TEXT,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Index vectorial per cerques ràpides amb distància cosinus
CREATE INDEX IF NOT EXISTS idx_embeddings_cosine
ON actor_embeddings USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);
