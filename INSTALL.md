# Guia d'Instal·lació - Actor Recognition App 🎭

Aquest document explica com instal·lar i executar el projecte pas a pas.

---

## 📌 Requisits previs

- Git (per clonar el repositori)
- Docker i Docker Compose
- Opcional Make (per simplificar ordres amb el `Makefile`)

---

## 🚀 Instal·lació

1. Clonar el repositori
   ```bash
   git clone httpsgithub.comusuarirepositori.git
   cd repositori
   ```

2. Configurar variables d'entorn
   - Crea un fitxer `.env` a la carpeta `backend` amb
     ```env
     POSTGRES_DB=actorsdb
     POSTGRES_USER=postgres
     POSTGRES_PASSWORD=supersecret
     TMDB_API_KEY=la_teva_clau_tmdb
     ```
   - Assegura’t que `.env` està inclòs al `.gitignore`.

3. Construir i arrencar serveis amb Docker Compose
   ```bash
   docker-compose up --build -d
   ```

4. Comprovar que el backend funciona
   - Obre el navegador a [httplocalhost8000docs](httplocalhost8000docs)
   - Veureu la documentació interactiva de l’API (Swagger UI).

---

## 🧪 Test ràpid

1. Dona permisos d’execució al script
   ```bash
   chmod +x test.sh
   ```

2. Executa el test
   ```bash
   .test.sh
   ```

3. Si tot funciona, veuràs una resposta amb la llista d’actors inicials.

---

## 🔧 Ús del Makefile (opcional)

Si tens `make` instal·lat, pots utilitzar ordres simplificades

- `make build` → construeix les imatges  
- `make up` → arrenca els serveis  
- `make down` → para i elimina contenidors  
- `make logs` → mostra els logs en temps real  
- `make seed` → executa el seeder Python  

---

## 📜 Notes

- El backend s’executa al port 8000.  
- La base de dades PostgreSQL s’executa al port 5432.  
- Els scripts `init.sql` i `seeder.sql` inicialitzen la BD amb taules i actors de prova.  
