#!/bin/bash

# Script para resumir capítulos usando OpenRouter con modelo gratuito
# Uso: ./run.sh [archivo_entrada] [archivo_salida] [modelo_opcional]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Valores por defecto
INPUT="${1:-input/EfectiveModernC++.md}"
OUTPUT="${2:-output/resumen.md}"
MODEL="${3:-openrouter/free}"

# Activar venv si existe
if [ -d .venv ]; then
    . .venv/bin/activate
fi

# Cargar variables de entorno desde .env
if [ -f .env ]; then
    set -a && source .env && set +a
fi

# Validar que tenemos las variables necesarias
if [ -z "$LLM_API_KEY" ] || [ -z "$LLM_BASE_URL" ]; then
    echo "Error: Variables de entorno LLM_API_KEY y LLM_BASE_URL no definidas."
    echo "Revisa el archivo .env"
    exit 1
fi

# Ejecutar el agente
echo "Resumiendo: $INPUT"
echo "Modelo: $MODEL"
./.venv/bin/python app/main.py \
    --input "$INPUT" \
    --output "$OUTPUT" \
    --model "$MODEL"

echo "✓ Resumen guardado en: $OUTPUT"
