## 📄 README.md

```markdown
# 🎬 Actor Recognition App (MVP)

Aplicació web que permet identificar actors a partir d’una captura amb la càmera del dispositiu.  
Funciona com un “Shazam per actors”: captura → backend → identificació → informació cultural.

---

## 🚀 Funcionalitats actuals (MVP)
- Captura d’imatges amb la càmera (frontend web).
- Enviament al backend via API REST (FastAPI).
- Reconeixement facial amb dataset local (OpenCV/face_recognition).
- Resposta amb nom de l’actor o “Desconegut”.
- Interfície minimalista amb vídeo i botó de captura.

---

## 🏗️ Arquitectura
- **Frontend**: HTML + CSS + JavaScript (PWA minimalista).
- **Backend**: Python + FastAPI.
- **Base de dades**: Dataset local amb imatges d’actors.
- **API externa**: TMDb (per informació cultural, en fases posteriors).

---

## ⚙️ Instal·lació

### 1. Clonar repositori
```bash
git clone git@github.com:usuari/actor-recognition-app.git
cd actor-recognition-app
```

### 2. Configurar backend
```bash
cd backend
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

### 3. Llançar servidor
```bash
uvicorn main:app --reload
```

El backend estarà disponible a:  
👉 `http://localhost:8000`

### 4. Llançar frontend
```bash
cd frontend
python -m http.server 5500
```

Obre al navegador:  
👉 `http://localhost:5500/index.html`

---

## 🔒 Configuració CORS
El backend inclou middleware CORS per permetre connexions des del frontend.  
Si vols restringir orígens, edita `main.py`:

```python
allow_origins=["http://localhost:5500"]
```

---

## 📂 Estructura del projecte
```
actor-recognition-app/
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── data/            # Dataset d’imatges d’actors
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
└── README.md
```

---

## 🧭 Roadmap
- [ ] Integració amb TMDb per mostrar filmografia.  
- [ ] Mode quiz i gamificació.  
- [ ] Cache local per actors més consultats.  
- [ ] Suport multillenguatge (Català, Castellà, Anglès).  
- [ ] Mode offline amb PWA.  

---

## 👨‍💻 Autor
Projecte creat per Jordi, com a MVP per explorar aplicacions culturals basades en reconeixement facial.

```


