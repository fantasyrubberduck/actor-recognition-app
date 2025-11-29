# Actor Recognition App 🎭

![CI + Docker](https://github.com/fantasyrubberduck/actor-recognition-app/actions/workflows/ci.yml/badge.svg)

Aplicació backend amb **FastAPI** i **PostgreSQL + pgvector** per identificar actors a partir d’imatges facials.  
Inclou integració amb **TMDb API** per enriquir els resultats amb biografia i imatge oficial.

---

## 🚀 Requisits

- Docker i Docker Compose instal·lats
- Clau d’API de [TMDb](https://www.themoviedb.org/documentation/api)

---

## 📂 Estructura del projecte

```
actor-recognition-app/
│
├── backend/
│   ├── main.py              # Backend FastAPI
│   ├── requirements.txt     # Dependències Python
│   └── seeder.py            # Script per generar embeddings inicials
├── docker-entrypoint-initdb.d/
│   ├── init.sql             # Creació de taules + extensió pgvector
│   └── seeder.sql           # Inserció inicial d’actors (Penélope Cruz, Javier Bardem)
├── Dockerfile               # Imatge backend
├── docker-compose.yml       # Orquestració backend + BD
└── .env                     # Variables d’entorn
```

---

## ⚙️ Configuració `.env`

Crea un fitxer `.env` amb les credencials:

```env
DB_NAME=actorsdb
DB_USER=postgres
DB_PASSWORD=supersecret
DB_HOST=db
DB_PORT=5432

TMDB_API_KEY=xxxxxxxxxxxxxxxx
```

> ⚠️ No oblidis afegir `.env` al `.gitignore`.

---

## 🐳 Desplegament amb Docker Compose

```bash
docker-compose up --build
```

- **db**: PostgreSQL amb pgvector (`ankane/pgvector:latest`)
- **backend**: FastAPI al port `8000`

---

## 📥 Inicialització automàtica

Quan el contenidor de PostgreSQL s’inicia per primera vegada:
- Executa `init.sql` → crea taules i indexos vectorials
- Executa `seeder.sql` → insereix Penélope Cruz i Javier Bardem

Després pots executar el seeder Python per generar embeddings:

```bash
docker-compose exec backend python seeder.py
```

---

## 🔑 Endpoints principals

- **POST `/identify`** → identifica actor a partir d’una imatge (base64)  
- **POST `/actors`** → crea un actor nou (amb opcional `image_url` per generar embedding)  
- **POST `/actors/{actor_id}/add_embedding`** → afegeix embeddings nous des d’una URL  
- **GET `/actors`** → llista tots els actors registrats  
- **GET `/actors/{actor_id}`** → detalls d’un actor concret (incloent embeddings)  

---

## 🎯 Exemple de crida

```bash
curl -X POST http://localhost:8000/identify \
  -H "Content-Type: application/json" \
  -d '{"image": "data:image/jpeg;base64,/9j/4AAQSk..."}'
```

Resposta esperada:
```json
{
  "actor_name": "Penélope Cruz",
  "confidence": 0.82,
  "tmdb_id": 194,
  "details": {
    "name": "Penélope Cruz",
    "biography": "...",
    "image_url": "https://image.tmdb.org/t/p/w500/xxxx.jpg"
  }
}
```

---

## 📌 Notes

- Les imatges originals **no es guarden** a la BD, només els embeddings i la URL de la font.  
- Fonts recomanades: **Wikimedia Commons** (llicència lliure) o **TMDb API**.  
- Ajusta el llindar de similitud (`THRESHOLD`) segons els teus tests.  

---

## 🧩 Properes millores

- Endpoint per eliminar actors/embeddings  
- Autenticació JWT per protegir l’API  
- Frontend senzill per provar identificacions
