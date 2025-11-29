# Esquema de Base de Dades - Actor Recognition App 🎭

Aquest document descriu l’estructura de la base de dades PostgreSQL amb l’extensió pgvector.

---

## 🗄️ Taules principals

### 1. `actors`
Emmagatzema informació bàsica dels actors.

 Camp         Tipus         Descripció                          
----------------------------------------------------------------
 id           SERIAL PK     Identificador únic                  
 name         TEXT          Nom complet de l’actor              
 tmdb_id      INTEGER       ID de l’actor a TMDb                
 imdb_id      TEXT          ID de l’actor a IMDb                
 created_at   TIMESTAMP     Data de creació                     

---

### 2. `embeddings`
Emmagatzema els vectors facials associats a cada actor.

 Camp         Tipus         Descripció                          
----------------------------------------------------------------
 id           SERIAL PK     Identificador únic                  
 actor_id     INTEGER FK    Referència a `actors.id`            
 vector       VECTOR(128)   Embedding facial (128 dimensions)   
 created_at   TIMESTAMP     Data de creació                     

---

## 🔗 Relacions

- `actors` 1N `embeddings`  
  Cada actor pot tenir múltiples embeddings facials associats.

---

## 📊 Índexos

- Índex vectorial sobre `embeddings.vector` per accelerar la cerca semàntica
  ```sql
  CREATE INDEX ON embeddings USING ivfflat (vector vector_l2_ops) WITH (lists = 100);
  ```

- Índex únic sobre `actors.tmdb_id` per evitar duplicats
  ```sql
  CREATE UNIQUE INDEX actors_tmdb_idx ON actors (tmdb_id);
  ```

---

## 📜 Notes

- Els embeddings es guarden amb `pgvector` per permetre comparacions de similitud.  
- Les claus externes asseguren integritat referencial entre `actors` i `embeddings`.  
- Els índexos milloren el rendiment en consultes de similitud i en la gestió d’actors.  
