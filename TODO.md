# TODO - Actor Recognition App 🎭

Llista de tasques concretes i accionables per al desenvolupament immediat del projecte.

---

## 🔧 Backend
- [ ] Revisar i provar tots els endpoints (`/identify`, `/actors`, `/actors/{id}`, etc.)
- [ ] Afegir validació extra per a imatges (tipus MIME, mida màxima)
- [ ] Implementar endpoint per eliminar actors i embeddings
- [ ] Afegir autenticació JWT per protegir l’API
- [ ] Escriure tests unitàris amb Pytest per cada endpoint

---

## 🗄️ Base de dades
- [ ] Revisar esquemes i indexos vectorials
- [ ] Afegir constraints per evitar duplicats d’actors
- [ ] Crear migracions amb `alembic` per gestionar canvis futurs
- [ ] Ampliar seeder amb més actors i imatges de fonts lliures (Wikimedia Commons)

---

## 🐳 DevOps
- [ ] Afegir secrets segurs a GitHub Actions (DB_PASSWORD, TMDB_API_KEY)
- [ ] Configurar workflow de CI per executar Pytest amb cobertura
- [ ] Afegir badge de cobertura al README
- [ ] Configurar CD per desplegar automàticament en Railway o Back4App

---

## 📄 Documentació
- [ ] Ampliar README amb exemples de crides a l’API
- [ ] Afegir Postman collection per provar endpoints
- [ ] Documentar arquitectura i flux de dades
- [ ] Escriure guia d’instal·lació pas a pas per estudiants

---

## 🎨 Frontend (futur)
- [ ] Crear prototip senzill amb React/Vue per provar identificacions
- [ ] Integrar amb backend via API REST
- [ ] Mostrar resultats amb imatge i biografia de TMDb
