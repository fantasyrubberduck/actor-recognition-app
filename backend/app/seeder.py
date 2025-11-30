import os
import numpy as np
import face_recognition
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import Base, Actor, Embedding  # importa els models del teu main.py

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "actorsdb")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "supersecret")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def generate_embedding(image_path: str) -> np.ndarray:
    img = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(img)
    if not face_locations:
        raise ValueError(f"No s’ha detectat cap cara a {image_path}")
    encodings = face_recognition.face_encodings(img, face_locations)
    if not encodings:
        raise ValueError(f"No s’ha pogut obtenir embedding a {image_path}")
    return encodings[0]

def seed():
    session = SessionLocal()

    actors_data = [
        {"name": "Penélope Cruz", "tmdb_id": 878, "imdb_id": "nm0004851", "image": "images/penelope_cruz.jpg"},
        {"name": "Javier Bardem", "tmdb_id": 879, "imdb_id": "nm0000849", "image": "images/javier_bardem.jpg"},
        {"name": "Antonio Banderas", "tmdb_id": 880, "imdb_id": "nm0000104", "image": "images/antonio_banderas.jpg"},
    ]

    for data in actors_data:
        existing = session.query(Actor).filter(Actor.tmdb_id == data["tmdb_id"]).first()
        if existing:
            print(f"ℹ️ Actor {data['name']} ja existeix (tmdb_id={data['tmdb_id']})")
            continue

        actor = Actor(name=data["name"], tmdb_id=data["tmdb_id"], imdb_id=data["imdb_id"])
        session.add(actor)
        session.commit()
        session.refresh(actor)

        try:
            embedding_vec = generate_embedding(data["image"])
            emb = Embedding(actor_id=actor.id, vector=embedding_vec.tolist())
            session.add(emb)
            session.commit()
            print(f"✅ Afegit {actor.name} amb embedding")
        except Exception as e:
            print(f"⚠️ No s’ha pogut generar embedding per {actor.name}: {e}")

    session.close()

if __name__ == "__main__":
    seed()
