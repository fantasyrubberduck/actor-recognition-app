# API Reference - Actor Recognition App 🎭

Aquest document descriu els endpoints disponibles al backend, els paràmetres, les respostes i els codis d’error.

---

## 🔑 Autenticació
*(pendent d’implementar JWT en roadmap)*  
Actualment, tots els endpoints són públics.

---

## 📌 Endpoints

### 1. POST `/identify`
Identifica un actor a partir d’una imatge.

- **Request**
  - `file`: imatge en format multipart/form-data
- **Response (200)**
  ```json
  {
    "actor": {
      "id": 1,
      "name": "Javier Bardem",
      "tmdb_id": 878,
      "imdb_id": "nm0000849"
    },
    "confidence": 0.92
  }
  ```
- **Errors**
  - `400 Bad Request`: imatge no vàlida
  - `404 Not Found`: cap actor coincideix

---

### 2. POST `/actors`
Afegeix un nou actor a la base de dades.

- **Request**
  ```json
  {
    "name": "Penélope Cruz",
    "tmdb_id": 1234,
    "imdb_id": "nm0004851"
  }
  ```
- **Response (201)**
  ```json
  {
    "id": 2,
    "name": "Penélope Cruz",
    "tmdb_id": 1234,
    "imdb_id": "nm0004851"
  }
  ```
- **Errors**
  - `400 Bad Request`: dades incompletes
  - `409 Conflict`: actor ja existeix

---

### 3. POST `/actors/{actor_id}/add_embedding`
Afegeix embeddings facials a un actor existent.

- **Request**
  - `file`: imatge en format multipart/form-data
- **Response (200)**
  ```json
  {
    "message": "Embedding afegit correctament",
    "actor_id": 2
  }
  ```
- **Errors**
  - `400 Bad Request`: imatge no vàlida
  - `404 Not Found`: actor no trobat

---

### 4. GET `/actors`
Llista tots els actors registrats.

- **Response (200)**
  ```json
  {
    "actors": [
      {
        "id": 1,
        "name": "Javier Bardem",
        "tmdb_id": 878,
        "imdb_id": "nm0000849"
      },
      {
        "id": 2,
        "name": "Penélope Cruz",
        "tmdb_id": 1234,
        "imdb_id": "nm0004851"
      }
    ]
  }
  ```

---

### 5. GET `/actors/{actor_id}`
Obté informació detallada d’un actor.

- **Response (200)**
  ```json
  {
    "id": 1,
    "name": "Javier Bardem",
    "tmdb_id": 878,
    "imdb_id": "nm0000849",
    "embeddings": [ ... ]
  }
  ```
- **Errors**
  - `404 Not Found`: actor no trobat

---

## 📜 Codis d’error comuns
- `400 Bad Request`: paràmetres incorrectes o imatge no vàlida
- `404 Not Found`: recurs no trobat
- `409 Conflict`: duplicat
- `500 Internal Server Error`: error inesperat al servidor
