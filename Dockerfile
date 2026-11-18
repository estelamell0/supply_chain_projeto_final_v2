# ==============================================================================
# Dockerfile - Ambiente Integrado do Laboratório 03 (Sigstore, Cosign & Capstone Base)
# Baseado em Alpine Linux + Multi-Stage Copy de ferramentas oficiais
#
# Ferramentas incluídas:
# - Cosign v2.4.1 (Sigstore) - Assinatura digital OCI, Keyless OIDC & Atestações in-toto
# - Syft v1.19.0 (Anchore) - Engenharia de SBOM (CycloneDX 1.6 & SPDX 3.0)
# - Trivy v0.58.2 (Aqua Security) - Scanner de Imagens, Licenças e Vulnerabilidades
# - Conftest v0.56.0 (Open Policy Agent) - Policy as Code com Rego v1 (preparado p/ Aula 07)
# - OSV-Scanner v1.9.2 (Google) - Auditoria de CVEs em ecossistemas abertos
# - Node.js 18 + npm - Aplicação alvo (payment-api)
# - Python 3 - Ferramentas de inspeção e conformidade
# - Docker CLI + jq + openssl + git + bash - Utilitários de DevSecOps
# ==============================================================================

FROM anchore/syft:v1.19.0 AS syft_bin
FROM aquasec/trivy:0.58.2 AS trivy_bin
FROM openpolicyagent/conftest:v0.56.0 AS conftest_bin

FROM node:18-alpine

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV SYFT_CHECK_FOR_APP_UPDATE=false
ENV TRIVY_SKIP_VERSION_CHECK=true
ENV TRIVY_DISABLE_TELEMETRY=true
ENV COSIGN_EXPERIMENTAL=1

# 1. Instalar utilitários essenciais do sistema via APK
RUN apk add --no-cache \
    bash \
    ca-certificates \
    curl \
    wget \
    git \
    jq \
    openssl \
    python3 \
    py3-pip \
    docker-cli \
    docker-cli-buildx \
    tar \
    gzip

# 2. Copiar binários oficiais via Multi-Stage
COPY --from=syft_bin /syft /usr/local/bin/syft
COPY --from=trivy_bin /usr/local/bin/trivy /usr/local/bin/trivy
COPY --from=conftest_bin /conftest /usr/local/bin/conftest

# 3. Instalar Cosign (binário oficial estático Sigstore)
RUN ARCH=$(uname -m) && \
    if [ "$ARCH" = "x86_64" ]; then COSIGN_ARCH="amd64"; \
    elif [ "$ARCH" = "aarch64" ]; then COSIGN_ARCH="arm64"; \
    else COSIGN_ARCH="amd64"; fi && \
    curl -fsSL "https://github.com/sigstore/cosign/releases/download/v2.4.1/cosign-linux-${COSIGN_ARCH}" -o /usr/local/bin/cosign && \
    chmod +x /usr/local/bin/cosign

# 4. Instalar OSV-Scanner
RUN ARCH=$(uname -m) && \
    if [ "$ARCH" = "x86_64" ]; then OSV_ARCH="amd64"; \
    elif [ "$ARCH" = "aarch64" ]; then OSV_ARCH="arm64"; \
    else OSV_ARCH="amd64"; fi && \
    curl -fsSL "https://github.com/google/osv-scanner/releases/download/v1.9.2/osv-scanner_linux_${OSV_ARCH}" -o /usr/local/bin/osv-scanner && \
    chmod +x /usr/local/bin/osv-scanner

# 5. Criar diretório de trabalho padrão
WORKDIR /workspace

CMD ["/bin/bash"]

