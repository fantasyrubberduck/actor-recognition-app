from fastapi import FastAPI
from pydantic import BaseModel
import face_recognition, base64, io
from PIL import Image
import numpy as np
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configura els orígens permesos
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Pots restringir-ho a ["http://localhost:5500"] o al domini concret
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dataset inicial
known_faces = {
    "Brad Pitt": face_recognition.face_encodings(
        face_recognition.load_image_file("backend/data/brad_pitt.jpg"))[0],
    "Luis Tosar": face_recognition.face_encodings(
        face_recognition.load_image_file("backend/data/luis_tosar.jpg"))[0],
    "Paul Giamatti": face_recognition.face_encodings(
        face_recognition.load_image_file("backend/data/paul_giamatti.jpg"))[0],
    "Scarlett Johansson": face_recognition.face_encodings(
        face_recognition.load_image_file("backend/data/scarlett_johansson.jpg"))[0]
}

class ImageData(BaseModel):
    image: str

@app.post("/identify")
async def identify(data: ImageData):
    image_bytes = base64.b64decode(data.image.split(",")[1])
    img = Image.open(io.BytesIO(image_bytes))
    np_img = np.array(img)

    encodings = face_recognition.face_encodings(np_img)
    if not encodings:
        return {"actor_name": "Desconegut"}

    face_encoding = encodings[0]
    for actor, known_encoding in known_faces.items():
        match = face_recognition.compare_faces([known_encoding], face_encoding)[0]
        if match:
            return {"actor_name": actor}

    return {"actor_name": "Desconegut"}

