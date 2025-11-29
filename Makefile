# Variables
COMPOSE = docker-compose

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
