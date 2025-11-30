import io
import os
from typing import List, Optional

from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from PIL import Image
import numpy as np
import face_recognition

from sqlalchemy import (
    create_engine, Column, Integer, Text, TIMESTAMP, ForeignKey, func, text, UniqueConstraint
)
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session
from pgvector.sqlalchemy import Vector

# -----------------------------------------------------------------------------
# Configuració
# -----------------------------------------------------------------------------
DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "actorsdb")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "supersecret")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

CORS_ORIGINS = [
    os.getenv("CORS_ORIGIN_1", "http://localhost:3000"),
    os.getenv("CORS_ORIGIN_2", "http://127.0.0.1:3000"),
    os.getenv("CORS_ORIGIN_3", "http://localhost:5173"),
]

# -----------------------------------------------------------------------------
# SQLAlchemy i models
# -----------------------------------------------------------------------------
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Actor(Base):
    __tablename__ = "actors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    tmdb_id = Column(Integer, unique=True, nullable=True)
    imdb_id = Column(Text, unique=True, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    embeddings = relationship("Embedding", back_populates="actor", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("tmdb_id", name="actors_tmdb_uid"),
        UniqueConstraint("imdb_id", name="actors_imdb_uid"),
    )


class Embedding(Base):
    __tablename__ = "embeddings"

    id = Column(Integer, primary_key=True, index=True)
    actor_id = Column(Integer, ForeignKey("actors.id", ondelete="CASCADE"), nullable=False, index=True)
    vector = Column(Vector(128), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    actor = relationship("Actor", back_populates="embeddings")


# -----------------------------------------------------------------------------
# App i CORS
# -----------------------------------------------------------------------------
app = FastAPI(title="Actor Recognition App")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def ensure_db_objects():
    # Assegura l’extensió pgvector i les taules
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
    Base.metadata.create_all(bind=engine)
    # Índex vectorial per rendiment (si no existeix)
    with engine.connect() as conn:
        conn.execute(
            text(
                "CREATE INDEX IF NOT EXISTS embeddings_vector_idx "
                "ON embeddings USING ivfflat (vector vector_l2_ops) WITH (lists = 100);"
            )
        )


@app.on_event("startup")
def on_startup():
    ensure_db_objects()


def read_image_from_upload(file: UploadFile) -> Image.Image:
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Només s’accepten fitxers d’imatge")
    image_bytes = file.file.read() if hasattr(file, "file") else None
    if not image_bytes:
        image_bytes = None
    if image_bytes is None or len(image_bytes) == 0:
        # fallback per a UploadFile async
        image_bytes = file.file.read() if hasattr(file, "file") else None
    if image_bytes is None or len(image_bytes) == 0:
        # si encara és buit, fem read async
        image_bytes = None

    if image_bytes is None or len(image_bytes) == 0:
        # últim intent: await no disponible aquí; gestionem a endpoint amb await file.read()
        raise HTTPException(status_code=400, detail="Fitxer d’imatge buit o no vàlid")

    try:
        return Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error obrint la imatge: {str(e)}")


async def image_to_embedding(file: UploadFile) -> List[float]:
    # Llegim bytes des d’UploadFile de forma segura
    image_bytes = await file.read()
    if not image_bytes or len(image_bytes) == 0:
        raise HTTPException(status_code=400, detail="Fitxer d’imatge buit o no vàlid")

    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error obrint la imatge: {str(e)}")

    img_array = np.array(img)
    face_locations = face_recognition.face_locations(img_array)
    if not face_locations:
        raise HTTPException(status_code=404, detail="No s’ha detectat cap cara")

    encodings = face_recognition.face_encodings(img_array, face_locations)
    if not encodings:
        raise HTTPException(status_code=404, detail="No s’ha pogut obtenir l’embedding facial")

    # Agafem el primer rostre detectat
    return encodings[0].tolist()


def distance_to_confidence(distance: float) -> float:
    # Conversió simple: confiança = max(0, 1 - min(distància, 1.0))
    conf = max(0.0, 1.0 - min(distance, 1.0))
    return round(conf, 2)


# -----------------------------------------------------------------------------
# Endpoints
# -----------------------------------------------------------------------------
@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/actors")
def list_actors(db: Session = Depends(get_db)) -> dict:
    try:
        actors = db.query(Actor).order_by(Actor.name.asc()).all()
        return {
            "actors": [
                {"id": a.id, "name": a.name, "tmdb_id": a.tmdb_id, "imdb_id": a.imdb_id}
                for a in actors
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error consultant actors: {str(e)}")


@app.post("/actors", status_code=201)
def create_actor(payload: dict, db: Session = Depends(get_db)) -> dict:
    name = payload.get("name")
    tmdb_id = payload.get("tmdb_id")
    imdb_id = payload.get("imdb_id")

    if not name:
        raise HTTPException(status_code=400, detail="El camp 'name' és obligatori")

    actor = Actor(name=name, tmdb_id=tmdb_id, imdb_id=imdb_id)
    try:
        db.add(actor)
        db.commit()
        db.refresh(actor)
        return {"id": actor.id, "name": actor.name, "tmdb_id": actor.tmdb_id, "imdb_id": actor.imdb_id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=409, detail=f"No s’ha pogut crear l’actor (potser duplicat): {str(e)}")


@app.post("/actors/{actor_id}/add_embedding")
async def add_embedding(actor_id: int, file: UploadFile, db: Session = Depends(get_db)) -> dict:
    # Validació MIME
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Només s’accepten fitxers d’imatge")

    actor = db.query(Actor).filter(Actor.id == actor_id).first()
    if not actor:
        raise HTTPException(status_code=404, detail="Actor no trobat")

    embedding_vec = await image_to_embedding(file)

    try:
        emb = Embedding(actor_id=actor.id, vector=embedding_vec)
        db.add(emb)
        db.commit()
        db.refresh(emb)
        return {"message": "Embedding afegit correctament", "actor_id": actor.id, "embedding_id": emb.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error guardant embedding: {str(e)}")


@app.post("/identify")
async def identify(file: UploadFile, db: Session = Depends(get_db)) -> dict:
    # Validació MIME
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Només s’accepten fitxers d’imatge")

    # Convertir la imatge a embedding facial (128 dims)
    embedding_vec = await image_to_embedding(file)

    try:
        # Cerca del veí més proper per L2 (pgvector)
        # Nota: pgvector.sqlalchemy ofereix mètodes d’operador de distància
        # Exemple: Embedding.vector.l2_distance(embedding_vec)
        nearest = (
            db.query(Embedding, Actor)
            .join(Actor, Embedding.actor_id == Actor.id)
            .order_by(Embedding.vector.l2_distance(embedding_vec))
            .limit(1)
            .all()
        )

        if not nearest:
            raise HTTPException(status_code=404, detail="Cap actor coincideix")

        best_embedding, best_actor = nearest[0]
        # Calcular distància per convertir-la a confiança
        # Fem una consulta puntual per obtenir la distància exacta (si cal):
        # Però podem reutilitzar l’ordenació: tornem a calcular per seguretat
        # pgvector distance computation:
        dist_row = (
            db.query(Embedding.vector.l2_distance(embedding_vec).label("distance"))
            .filter(Embedding.id == best_embedding.id)
            .first()
        )
        distance = float(dist_row.distance) if dist_row and dist_row.distance is not None else 1.0
        confidence = distance_to_confidence(distance)

        return {
            "actor": {
                "id": best_actor.id,
                "name": best_actor.name,
                "tmdb_id": best_actor.tmdb_id,
                "imdb_id": best_actor.imdb_id,
            },
            "confidence": confidence,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error consultant BD: {str(e)}")
