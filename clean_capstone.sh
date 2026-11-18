#!/usr/bin/env bash
set -e

echo "Limpando artefatos gerados no Capstone..."

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if docker compose version >/dev/null 2>&1; then
    DOCKER_COMPOSE="docker compose"
elif command -v docker-compose >/dev/null 2>&1; then
    DOCKER_COMPOSE="docker-compose"
else
    DOCKER_COMPOSE="docker compose"
fi

$DOCKER_COMPOSE down -v --remove-orphans

rm -f dist/sbom.cdx.json cosign.key cosign.pub

if [ -d "src/node_modules" ]; then
    find src/node_modules -mindepth 1 -maxdepth 1 ! -name '@corp' ! -name 'gpl-math-lib' ! -name 'express' ! -name 'lodash' -exec rm -rf {} + 2>/dev/null || true
fi

echo "Ambiente Capstone limpo e resetado com sucesso!"

