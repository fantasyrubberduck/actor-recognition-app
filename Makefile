# Variables
COMPOSE = docker compose

# Construir imatges
build:
	$(COMPOSE) build

# Arrencar serveis en segon pla
up:
	$(COMPOSE) up -d

# Parar i eliminar contenidors
down:
	$(COMPOSE) down

# Veure logs en temps real
logs:
	$(COMPOSE) logs -f

# Reiniciar serveis
restart: down up

# Executar seeder Python dins el backend
seed:
	$(COMPOSE) exec backend python seeder.py

# Obrir shell dins el backend
shell-backend:
	$(COMPOSE) exec backend bash

# Obrir shell dins la BD
shell-db:
	$(COMPOSE) exec db bash

# Reinicia completament la base de dades i els contenidors
reset-db:
	$(COMPOSE) down -v
	$(COMPOSE) up --build -d

# Mostra les taules existents a la BD
psql-tables:
	$(COMPOSE) exec db psql -U postgres -d actorsdb -c "\dt"

# Obre una shell psql dins del contenidor de la BD
psql-shell:
	$(COMPOSE) exec db psql -U postgres -d actorsdb