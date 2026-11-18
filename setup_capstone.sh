#!/usr/bin/env bash
set -e

echo "=========================================================================="
echo " [INFO] INICIALIZANDO PROJETO FINAL CAPSTONE: SUPPLY CHAIN SECURITY"
echo "=========================================================================="

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

mkdir -p dist

if docker compose version >/dev/null 2>&1; then
    DOCKER_COMPOSE="docker compose"
elif command -v docker-compose >/dev/null 2>&1; then
    DOCKER_COMPOSE="docker-compose"
else
    DOCKER_COMPOSE="docker compose"
fi

echo "[1/3] Subindo Registry OCI Local (porta 5000)..."
$DOCKER_COMPOSE up -d registry

echo "[2/3] Construindo imagem do ambiente Capstone (supply-chain-capstone)..."
$DOCKER_COMPOSE build capstone

echo ""
echo "[3/3] Ambiente pronto com sucesso!"
echo "Para entrar no terminal do Capstone, execute:"
echo "  $DOCKER_COMPOSE run --rm capstone"
echo "=========================================================================="

