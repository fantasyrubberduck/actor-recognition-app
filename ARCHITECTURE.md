# Arquitectura del Projecte Actor Recognition App 🎭

Aquest document descriu l’arquitectura del sistema, els components principals i el flux de dades.

---

## 🏗️ Components principals

- **Backend (FastAPI)**  
  - Servei principal que exposa els endpoints REST (`/identify`, `/actors`, etc.).  
  - Gestiona la lògica d’embeddings facials i la integració amb TMDb API.  
  - S’executa dins un contenidor Docker amb Uvicorn.

- **Base de dades (PostgreSQL + pgvector)**  
  - Emmagatzema actors, embeddings facials i metadades.  
  - Utilitza l’extensió `pgvector` per a la cerca semàntica d’embeddings.  
  - Inicialitzada amb `init.sql` i `seeder.sql`.

- **Integració amb TMDb API**  
  - Permet enriquir els resultats amb biografia, imatge oficial i metadades dels actors.  
  - Les claus API es gestionen amb `.env`.

- **Workflows CI/CD (GitHub Actions)**  
  - Construcció de la imatge Docker.  
  - Execució de tests (`test.sh`).  
  - Validació automàtica en cada *push* o *pull request*.  

---

## 🔄 Flux de dades

1. **Usuari** envia una imatge a l’endpoint `/identify`.  
2. **Backend FastAPI** processa la imatge amb `face-recognition` i genera embeddings.  
3. Els embeddings es comparen amb els existents a **PostgreSQL + pgvector**.  
4. Si hi ha coincidència, es retorna l’actor amb les dades enriquides de **TMDb API**.  
5. La resposta es retorna a l’usuari en format JSON.

---

## 📊 Diagrama d’arquitectura (simplificat)

```
+-----------+        +----------------+        +-------------------+
|   Usuari  | -----> |   Backend      | -----> |   PostgreSQL +    |
| (client)  |        |   FastAPI      |        |   pgvector        |
+-----------+        +----------------+        +-------------------+
                         |   ^
                         v   |
                    +----------------+
                    |   TMDb API     |
                    +----------------+
```

---

## 🚀 Futur
- Afegir **frontend senzill** per provar identificacions.  
- Autenticació JWT i gestió d’usuaris.  
- Cache amb Redis per accelerar consultes.  
- Desplegament automàtic en Railway o Back4App.  
