# 🟡 Trilha 2: Sandbox CLI Local & Enforcement

**Nota Máxima:** `10,0`  
**Tempo Estimado:** **~100 min** *(Teto máximo: 2h00 — com pré-aquecimento do Docker antes da sessão)*  
**Camada Tecnológica:** Operação determinística em Docker local (`syft`, `trivy`, `cosign`, `conftest`, `generate_compliance_dossier.py`) — **sem necessidade de nuvem**.  
**Cobertura Curricular:** Aulas 01 a 08 completas.

---

## Pré-Aquecimento Recomendado (Antes de Iniciar o Cronômetro)
Para economizar ~15–20 min de download em aula, faça o build prévio das imagens de laboratório no host (dentro de `supply_chain_final_v2/`):
- **Windows (PowerShell):** `docker compose build capstone`
- **Linux/macOS/WSL:** `chmod +x setup_capstone.sh clean_capstone.sh && docker compose build capstone`

---

## Roteiro Cronometrado (Alvo: 100 min)

### Etapa 1: Sandbox, Dependências & Build Imutável — `~25 min` *(Aulas 02, 03 & 06)*
1. Inicialize o Registry OCI local e entre no container de trabalho:
   ```powershell
   docker compose up -d registry; docker compose run --rm capstone
   ```
2. Dentro do container (`/workspace#`), verifique o isolamento do escopo `@corp` em `src/.npmrc` e instale dependências com trava contra scripts de ciclo de vida:
   ```bash
   cat src/.npmrc
   cd src && npm install --ignore-scripts && cd ..
   ```
3. Construa, envie para o Registry local (`localhost:5000`) e capture o **Digest SHA-256 imutável**:
   ```bash
   docker build -f docker/Dockerfile.app -t localhost:5000/payment-api:v1.0.0 . && docker push localhost:5000/payment-api:v1.0.0
   IMAGE_DIGEST=$(docker inspect --format '{{range .RepoDigests}}{{println .}}{{end}}' localhost:5000/payment-api:v1.0.0 | grep localhost:5000 | head -n 1)
   echo "Lacre Matemático: $IMAGE_DIGEST"
   ```
4. Gere o **SBOM CycloneDX 1.6** diretamente do digest publicado:
   ```bash
   mkdir -p dist
   syft $IMAGE_DIGEST -o cyclonedx-json=dist/sbom.cdx.json
   ```

### Etapa 2: Scan de Vulnerabilidades & Laudo OpenVEX — `~20 min` *(Aulas 03 & 04)*
1. Execute o scan de CVEs na imagem:
   ```bash
   trivy image --severity HIGH,CRITICAL localhost:5000/payment-api:v1.0.0
   ```
2. Abra [`attestations/vex_customizado.openvex.json`](../../attestations/vex_customizado.openvex.json) e complete o **3º statement** substituindo os marcadores `TODO` por uma `justification` oficial OpenVEX v0.2.0 e um `impact_statement` coerente. *(Se veio da Trilha 1 em Modo Incremental, este arquivo já está pronto!)*

### Etapa 3: Assinatura Cosign, Tag Tampering & In-Toto — `~25 min` *(Aula 06)*
1. Gere o par de chaves local e assine a imagem pelo **Digest SHA-256**:
   ```bash
   COSIGN_PASSWORD="" cosign generate-key-pair
   COSIGN_PASSWORD="" cosign sign --key cosign.key --tlog-upload=false -y $IMAGE_DIGEST
   cosign verify --key cosign.pub --insecure-ignore-tlog=true localhost:5000/payment-api:v1.0.0
   ```
2. **Prova de Ataque (*Tag Tampering*):** Sobrescreva a tag `:v1.0.0` com `busybox:latest` não assinado e comprove o bloqueio (`Error: no signatures found`):
   ```bash
   docker pull busybox:latest && docker tag busybox:latest localhost:5000/payment-api:v1.0.0 && docker push localhost:5000/payment-api:v1.0.0
   cosign verify --key cosign.pub --insecure-ignore-tlog=true localhost:5000/payment-api:v1.0.0
   ```
3. Restaure a imagem legítima, assine o digest e sele as **2 atestações *in-toto* essenciais** (SBOM CycloneDX + Laudo OpenVEX):
   ```bash
   docker build -f docker/Dockerfile.app -t localhost:5000/payment-api:v1.0.0 . && docker push localhost:5000/payment-api:v1.0.0
   IMAGE_DIGEST=$(docker inspect --format '{{range .RepoDigests}}{{println .}}{{end}}' localhost:5000/payment-api:v1.0.0 | grep localhost:5000 | head -n 1)
   COSIGN_PASSWORD="" cosign sign --key cosign.key --tlog-upload=false -y $IMAGE_DIGEST
   COSIGN_PASSWORD="" cosign attest --key cosign.key --predicate dist/sbom.cdx.json --type cyclonedx --tlog-upload=false -y $IMAGE_DIGEST
   COSIGN_PASSWORD="" cosign attest --key cosign.key --predicate attestations/vex_customizado.openvex.json --type openvex --tlog-upload=false -y $IMAGE_DIGEST
   cosign verify-attestation --key cosign.pub --type openvex --insecure-ignore-tlog=true $IMAGE_DIGEST | jq '.payload | @base64d | fromjson'
   ```

### Etapa 4: Conftest (Rego v1), Dossiê & Bloco Express — `~30 min` *(Aulas 01, 05, 07 & 08)*
1. Complete pelo menos **1 regra `TODO`** em [`policies/openvex_audit.rego`](../../policies/openvex_audit.rego) *(ou utilize o arquivo completo caso tenha feito a Trilha 1)*.
2. Execute o **Conftest** comprovando **1 bloqueio (`FAIL`)** e **1 aprovação (`PASS`)**:
   ```bash
   # Testes FAIL esperados (Dockerfile inseguro e licença GPL-3.0 no SBOM):
   conftest test docker/Dockerfile.inseguro -p policies/dockerfile.rego
   conftest test dist/sbom.cdx.json -p policies/sbom_license.rego

   # Testes PASS esperados (Dockerfile blindado, Proveniência SLSA e seu OpenVEX):
   conftest test docker/Dockerfile.app -p policies/dockerfile.rego
   conftest test attestations/slsa_predicate.json -p policies/slsa_provenance.rego
   conftest test attestations/vex_customizado.openvex.json -p policies/openvex_audit.rego
   ```
3. Gere o **Dossiê de Conformidade** (*Evidence-as-Code*) consolidando lockfile, SBOM, OpenVEX, SLSA e política Rego:
   ```bash
   python3 tools/generate_compliance_dossier.py
   cat dist/dossie_conformidade.json
   ```
4. Remova `cosign.key` após concluir os testes, preencha [`docs/trilha_2/TEMPLATE_ENTREGA_TRILHA_2.md`](./TEMPLATE_ENTREGA_TRILHA_2.md) (respondendo ao **Bloco Express de Aulas 01 & 05**, ou marcando **`[x] Modo Incremental`** se já concluiu a Trilha 1) e valide:
   ```bash
   rm -f cosign.key
   python3 tools/selfcheck_capstone.py --trilha 2
   ```

---

## O Que Entregar (Checklist Trilha 2)
- [ ] [`docs/trilha_2/TEMPLATE_ENTREGA_TRILHA_2.md`](./TEMPLATE_ENTREGA_TRILHA_2.md) preenchido com logs reais (`$IMAGE_DIGEST`, bloqueio no Cosign, `verify-attestation`, `FAIL`/`PASS` no Conftest e Dossiê).
- [ ] `dist/sbom.cdx.json` e `dist/dossie_conformidade.json` gerados localmente.
- [ ] `attestations/vex_customizado.openvex.json` e `policies/openvex_audit.rego` completos sem `TODO`s.
- [ ] Chave privada `cosign.key` removida + `python3 tools/selfcheck_capstone.py --trilha 2` sem erros críticos.
