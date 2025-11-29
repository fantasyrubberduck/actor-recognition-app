-- Inserir Penélope Cruz
INSERT INTO actors (name, tmdb_id, imdb_id)
VALUES ('Penélope Cruz', 194, 'nm0001086')
ON CONFLICT (tmdb_id) DO NOTHING;

-- Inserir Javier Bardem
INSERT INTO actors (name, tmdb_id, imdb_id)
VALUES ('Javier Bardem', 878, 'nm0000849')
ON CONFLICT (tmdb_id) DO NOTHING;
