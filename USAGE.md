# Guia d'Ús - Actor Recognition App 🎭

Aquest document mostra exemples pràctics de com consumir els endpoints del backend amb `curl` i `httpie`.

---

## 📌 Endpoints disponibles

- `POST /identify` → Identifica un actor a partir d’una imatge
- `POST /actors` → Afegeix un nou actor
- `POST /actors/{actor_id}/add_embedding` → Afegeix embeddings facials a un actor
- `GET /actors` → Llista tots els actors
- `GET /actors/{actor_id}` → Obté informació d’un actor concret

---

## 🚀 Exemples amb `curl`

### 1. Identificar un actor
```bash
curl -X POST http://localhost:8000/identify \
  -F "file=@foto.jpg"
```

### 2. Afegir un nou actor
```bash
curl -X POST http://localhost:8000/actors \
  -H "Content-Type: application/json" \
  -d '{"name":"Penélope Cruz","tmdb_id":1234,"imdb_id":"nm0004851"}'
```

### 3. Afegir embeddings a un actor
```bash
curl -X POST http://localhost:8000/actors/1/add_embedding \
  -F "file=@penelope.jpg"
```

### 4. Llistar actors
```bash
curl http://localhost:8000/actors
```

### 5. Obtenir informació d’un actor
```bash
curl http://localhost:8000/actors/1
```

---

## 🧪 Exemples amb `httpie`

### 1. Identificar un actor
```bash
http -f POST http://localhost:8000/identify file@foto.jpg
```

### 2. Afegir un nou actor
```bash
http POST http://localhost:8000/actors \
  name="Penélope Cruz" tmdb_id=1234 imdb_id="nm0004851"
```

### 3. Afegir embeddings a un actor
```bash
http -f POST http://localhost:8000/actors/1/add_embedding file@penelope.jpg
```

### 4. Llistar actors
```bash
http GET http://localhost:8000/actors
```

### 5. Obtenir informació d’un actor
```bash
http GET http://localhost:8000/actors/1
```

---

## 📜 Notes

- Els endpoints que reben imatges (`/identify`, `/add_embedding`) esperen fitxers en format **multipart/form-data**.  
- Les respostes són en format **JSON**.  
- Pots provar l’API també amb [Swagger UI](http://localhost:8000/docs).  
