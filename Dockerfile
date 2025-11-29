# Imatge base lleugera amb Python
FROM python:3.11-slim

# Instal·lar dependències del sistema necessàries per a dlib i face-recognition
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    libboost-all-dev \
    && rm -rf /var/lib/apt/lists/*

# Directori de treball
WORKDIR /app

# Copiar requirements i instal·lar dependències Python
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el codi del backend
COPY backend/ .

# Exposar port
EXPOSE 8000

# Comanda per arrencar FastAPI amb Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
