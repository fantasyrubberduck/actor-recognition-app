# Roadmap del Projecte Actor Recognition App 🎭

Aquest document descriu les fites i millores planificades per al projecte.  
La roadmap és orientativa i pot evolucionar segons les necessitats i les contribucions.

---

## 🚀 MVP (versió inicial)
- [x] Backend amb FastAPI
- [x] Base de dades PostgreSQL amb extensió pgvector
- [x] Endpoints bàsics:
  - POST `/identify`
  - POST `/actors`
  - POST `/actors/{actor_id}/add_embedding`
  - GET `/actors`
  - GET `/actors/{actor_id}`
- [x] Integració amb TMDb API per enriquir resultats
- [x] Scripts d’inicialització (`init.sql`, `seeder.sql`)
- [x] Workflow CI + Docker amb GitHub Actions
- [x] Documentació inicial (`README.md`, `LICENSE`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`)

---

## 🧩 Properes fites
- [ ] **Autenticació JWT** per protegir l’API
- [ ] **Gestió d’usuaris** (rols: admin, col·laborador, lector)
- [ ] **Endpoint per eliminar actors/embeddings**
- [ ] **Frontend senzill** (React/Vue) per provar identificacions
- [ ] **Millora del seeder** amb més actors i imatges de fonts lliures (Wikimedia Commons)
- [ ] **Tests automatitzats** amb Pytest i cobertura
- [ ] **Badge de cobertura** al README

---

## 🔮 Futur
- [ ] **Desplegament en núvol** (Railway, Back4App, PythonAnywhere)
- [ ] **CI/CD complet** amb desplegament automàtic
- [ ] **Escalabilitat**: partició de serveis (API, DB, embeddings)
- [ ] **Cache amb Redis** per accelerar consultes
- [ ] **Suport multillenguatge** (Català, Castellà, Anglès)
- [ ] **Integració amb altres fonts** (IMDb, Wikidata)
- [ ] **Documentació avançada** amb OpenAPI i Postman collections
