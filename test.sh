#!/bin/bash

# Script de test ràpid per comprovar el backend

echo "➡️ Comprovant que el backend està en marxa..."

# Esperar uns segons perquè el backend estigui llest
sleep 5

# Crida a l'endpoint /actors
RESPONSE=$(curl -s http://localhost:8000/actors)

echo "➡️ Resposta del backend:"
echo "$RESPONSE"

# Validar si conté 'actors'
if echo "$RESPONSE" | grep -q "actors"; then
  echo "✅ Test correcte: el backend respon amb la llista d'actors."
else
  echo "❌ Error: el backend no ha retornat la llista esperada."
fi
