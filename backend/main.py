from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64, io, os, requests
from PIL import Image
import numpy as np
import face_recognition
import psycopg2
import psycopg2.extras

# Carregar variables d’entorn
DB_NAME = os.environ["DB_NAME"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]

TMDB_API_KEY = os.environ.get("TMDB_API_KEY")
TMDB_BASE = "https://api.themoviedb.org/3"

app = FastAPI()

# Configuració CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_conn():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

# ---------------------------
# Models Pydantic
# ---------------------------

class ImageData(BaseModel):
    image: str  # data URL base64

class EmbeddingRequest(BaseModel):
    image_url: str

class ActorCreate(BaseModel):
    name: str
    tmdb_id: int | None = None
    imdb_id: str | None = None
    image_url: str | None = None  # opcional per generar embedding

# ---------------------------
# Funcions auxiliars
# ---------------------------

def get_tmdb_details(tmdb_id: int):
    if not TMDB_API_KEY:
        return None
    r = requests.get(
        f"{TMDB_BASE}/person/{tmdb_id}",
        params={"api_key": TMDB_API_KEY, "language": "es-ES"}
    )
    if r.status_code != 200:
        return None
    data = r.json()
    profile_path = data.get("profile_path")
    image_url = f"https://image.tmdb.org/t/p/w500{profile_path}" if profile_path else None
    return {
        "name": data.get("name"),
        "biography": data.get("biography"),
        "known_for_department": data.get("known_for_department"),
        "birthday": data.get("birthday"),
        "place_of_birth": data.get("place_of_birth"),
        "image_url": image_url
    }

# ---------------------------
# Endpoints
# ---------------------------

@app.post("/identify")
def identify(data: ImageData):
    # Decodificar imatge
    try:
        image_bytes = base64.b64decode(data.image.split(",")[1])
    except Exception:
        raise HTTPException(400, "Format d’imatge invàlid")

    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    np_img = np.array(img)

    encodings = face_recognition.face_encodings(np_img)
    if not encodings:
        return {"actor_name": "Desconegut", "confidence": 0.0}

    query_vec = encodings[0].tolist()

    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute("""
        SELECT a.id, a.name, a.tmdb_id, ae.embedding <=> %s::vector AS distance
        FROM actor_embeddings ae
        JOIN actors a ON ae.actor_id = a.id
        ORDER BY distance ASC
        LIMIT 1;
    """, (query_vec,))
    row = cur.fetchone()
    conn.close()

    if not row:
        return {"actor_name": "Desconegut", "confidence": 0.0}

    confidence = max(0.0, 1.0 - float(row["distance"]))
    THRESHOLD = 0.65

    if confidence < THRESHOLD or not row["tmdb_id"]:
        return {"actor_name": "Desconegut", "confidence": confidence}

    details = get_tmdb_details(row["tmdb_id"])
    return {
        "actor_name": row["name"],
        "confidence": confidence,
        "tmdb_id": row["tmdb_id"],
        "details": details
    }

@app.post("/actors/{actor_id}/add_embedding")
def add_embedding(actor_id: int, payload: EmbeddingRequest):
    try:
        resp = requests.get(payload.image_url, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        raise HTTPException(400, f"No s'ha pogut descarregar la imatge: {str(e)}")

    img = Image.open(BytesIO(resp.content)).convert("RGB")
    np_img = np.array(img)

    encodings = face_recognition.face_encodings(np_img)
    if not encodings:
        raise HTTPException(400, "No s'ha detectat cap cara a la imatge")

    vec = encodings[0]

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO actor_embeddings (actor_id, embedding, source_url) VALUES (%s, %s, %s)",
        (actor_id, vec.tolist(), payload.image_url)
    )
    conn.commit()
    cur.close()
    conn.close()

    return {"actor_id": actor_id, "status": "embedding afegit correctament"}

@app.post("/actors")
def create_actor(payload: ActorCreate):
    conn = get_conn()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO actors (name, tmdb_id, imdb_id) VALUES (%s, %s, %s) RETURNING id",
            (payload.name, payload.tmdb_id, payload.imdb_id)
        )
        actor_id = cur.fetchone()[0]
        conn.commit()
    except Exception as e:
        conn.rollback()
        cur.close()
        conn.close()
        raise HTTPException(400, f"No s'ha pogut crear l'actor: {str(e)}")

    if payload.image_url:
        try:
            resp = requests.get(payload.image_url, timeout=10)
            resp.raise_for_status()
            img = Image.open(BytesIO(resp.content)).convert("RGB")
            np_img = np.array(img)
            encodings = face_recognition.face_encodings(np_img)
            if not encodings:
                raise HTTPException(400, "No s'ha detectat cap cara a la imatge")
            vec = encodings[0]
            cur.execute(
                "INSERT INTO actor_embeddings (actor_id, embedding, source_url) VALUES (%s, %s, %s)",
                (actor_id, vec.tolist(), payload.image_url)
            )
            conn.commit()
        except Exception as e:
            conn.rollback()
            cur.close()
            conn.close()
            raise HTTPException(400, f"No s'ha pogut generar l'embedding: {str(e)}")

    cur.close()
    conn.close()
    return {"actor_id": actor_id, "status": "actor creat correctament"}

@app.get("/actors")
def list_actors():
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cur.execute("SELECT id, name, tmdb_id, imdb_id FROM actors ORDER BY name ASC;")
        rows = cur.fetchall()
    except Exception as e:
        cur.close()
        conn.close()
        raise HTTPException(500, f"Error consultant actors: {str(e)}")

    cur.close()
    conn.close()

    actors = [
        {
            "id": row["id"],
            "name": row["name"],
            "tmdb_id": row["tmdb_id"],
            "imdb_id": row["imdb_id"]
        }
        for row in rows
    ]
    return {"actors": actors}

@app.get("/actors/{actor_id}")
def actor_details(actor_id: int):
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cur.execute("SELECT id, name, tmdb_id, imdb_id FROM actors WHERE id = %s;", (actor_id,))
        actor = cur.fetchone()
        if not actor:
            raise HTTPException(404, "Actor no trobat")

        cur.execute("SELECT id, source_url FROM actor_embeddings WHERE actor_id = %s;", (actor_id,))
        embeddings = cur.fetchall()
    except Exception as e:
        cur.close()
        conn.close()
        raise HTTPException(500, f"Error consultant actor: {str(e)}")

    cur.close()
    conn.close()

    return {
        "id": actor["id"],
        "name": actor["name"],
        "tmdb_id": actor["tmdb_id"],
        "imdb_id": actor["imdb_id"],
        "embeddings": [{"id": e["id"], "source_url": e["source_url"]} for e in embeddings]
    }
