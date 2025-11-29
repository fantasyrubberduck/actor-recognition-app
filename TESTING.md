# Guia de Testing - Actor Recognition App 🎭

Aquest document descriu les pautes per escriure, organitzar i executar tests al projecte.

---

## 🧪 Tipus de tests

- **Unit tests**  
  Verifiquen la lògica interna de funcions i mòduls (per exemple, validació d’imatges, creació d’actors).

- **Integration tests**  
  Comproven la interacció entre components (FastAPI + PostgreSQL + pgvector).

- **End-to-end tests (E2E)**  
  Simulen crides reals a l’API (`/identify`, `/actors`) per validar el flux complet.

---

## 📂 Estructura recomanada

```
backend/
  ├── app/
  │   ├── main.py
  │   └── ...
  ├── tests/
  │   ├── test_unit.py
  │   ├── test_integration.py
  │   └── test_e2e.py
```

---

## ⚙️ Configuració

1. **Instal·lar Pytest**
   ```bash
   pip install pytest
   ```

2. **Fitxer `pytest.ini`**
   ```ini
   [pytest]
   testpaths = tests
   python_files = test_*.py
   ```

---

## 🚀 Execució de tests

- Executar tots els tests:
  ```bash
  pytest
  ```

- Executar un test concret:
  ```bash
  pytest tests/test_unit.py::test_add_actor
  ```

- Generar informe de cobertura:
  ```bash
  pytest --cov=backend --cov-report=html
  ```

---

## 🐳 Testing amb Docker

1. Arrenca la base de dades amb Docker Compose:
   ```bash
   docker-compose up -d db
   ```

2. Executa els tests dins el contenidor:
   ```bash
   docker-compose run backend pytest
   ```

---

## 🔄 Integració amb CI

- El workflow de GitHub Actions (`ci.yml`) executa automàticament els tests en cada *push* o *pull request*.  
- Si algun test falla, el badge del `README.md` mostrarà estat vermell.  
- Es recomana afegir un **badge de cobertura** per visualitzar el percentatge de tests passats.

---

## 📜 Bones pràctiques

- Escriu tests per cada nova funcionalitat.  
- Mantén els tests independents (no dependre d’ordre d’execució).  
- Usa dades de prova consistents (fixtures).  
- Documenta els casos límit i errors esperats.  
