# 🟡 Manual da Trilha 2: Comandos no Docker Local (Sandbox CLI & Conftest)

**Nota Máxima:** `10,0`  
**Tempo Estimado:** **~100 min** *(no máximo 2h00 — se preparar o Docker antes)*  
**O Que Você Precisa:** Docker e Docker Compose rodando no seu computador (**não precisa de conta na nuvem**).  
**O Que Você Vai Praticar:** Todos os 8 assuntos do curso (Aulas 01 a 08) operando ferramentas reais (`syft`, `trivy`, `cosign`, `conftest`) dentro de um container isolado.

---

## Como Funciona Esta Trilha?
Você não precisa instalar `syft`, `trivy`, `cosign` nem `conftest` direto no seu Windows/Mac/Linux. Nós já colocamos todas essas ferramentas dentro de um container chamado **`capstone`**, junto com um repositório local de imagens (**`registry`** na porta `5000`).

Tudo o que você observar na tela vai ser colado no arquivo [`TEMPLATE_ENTREGA_TRILHA_2.md`](./TEMPLATE_ENTREGA_TRILHA_2.md).

> 💡 **Dica de Ouro (Antes de Começar):**  
> Abra o terminal na pasta raiz `supply_chain_final_v2/` e monte a imagem do laboratório **antes** da aula para economizar de 15 a 20 minutos de download:
> ```powershell
> docker compose build capstone
> ```
> *(No Linux/macOS/WSL, rode também `chmod +x setup_capstone.sh clean_capstone.sh` antes.)*

---

## Passo a Passo Detalhado

### Etapa 1: Subir o Ambiente, Instalar com Trava & Gerar o SBOM — `~25 min` *(Aulas 02, 03 & 06)*

1. **Inicie o Registry local e entre no container de ferramentas:**
   ```powershell
   docker compose up -d registry
   docker compose run --rm capstone
   ```
   *O que acontece:* o terminal vai mudar para `/workspace#`. Você já está dentro do Linux com todas as ferramentas prontas e com a pasta do projeto espelhada ali dentro.

2. **Confira o isolamento de pacotes privados e instale sem rodar scripts ocultos:**
   ```bash
   cat src/.npmrc
   cd src && npm install --ignore-scripts && cd ..
   ```
   *Por que fazemos isso?* O `src/.npmrc` garante que pacotes `@corp` não sejam buscados na internet pública (*Dependency Confusion*), e `--ignore-scripts` bloqueia qualquer comando automático escondido dentro dos pacotes.

3. **Construa a imagem Docker da `payment-api`, envie para o Registry local (`localhost:5000`) e pegue o código matemático único dela (`$IMAGE_DIGEST`):**
   ```bash
   docker build -f docker/Dockerfile.app -t localhost:5000/payment-api:v1.0.0 .
   docker push localhost:5000/payment-api:v1.0.0
   IMAGE_DIGEST=$(docker inspect --format '{{range .RepoDigests}}{{println .}}{{end}}' localhost:5000/payment-api:v1.0.0 | grep localhost:5000 | head -n 1)
   echo "Lacre Matemático: $IMAGE_DIGEST"
   ```
   *O que vai aparecer:* uma linha parecida com `Lacre Matemático: localhost:5000/payment-api@sha256:1b17ebb...`. **Copie essa linha inteira para a Seção 1 do seu Template 2.**

4. **Gere a lista de componentes (SBOM) usando o `syft`:**
   ```bash
   mkdir -p dist
   syft $IMAGE_DIGEST -o cyclonedx-json=dist/sbom.cdx.json
   ```
   *O que acontece:* o `syft` abre a imagem e salva em `dist/sbom.cdx.json` a lista completa de pacotes Alpine + Node.js (incluindo a biblioteca `gpl-math-lib`).

---

### Etapa 2: Escanear Falhas (`trivy`) & Completar o OpenVEX — `~20 min` *(Aulas 03 & 04)*

1. **Procure falhas de segurança (`HIGH` e `CRITICAL`) na imagem:**
   ```bash
   trivy image --severity HIGH,CRITICAL localhost:5000/payment-api:v1.0.0
   ```
   *O que vai aparecer:* uma tabela mostrando falhas encontradas no sistema Alpine (como `libcrypto3`, `musl`, `zlib`) e nos pacotes Node. **Copie um resumo dessa saída para a Seção 2 do Template 2.**

2. **Complete o laudo OpenVEX em [`attestations/vex_customizado.openvex.json`](../../attestations/vex_customizado.openvex.json):**
   - Abra esse arquivo no editor e procure o **3º bloco** (`CVE-2024-29041` no `express`).
   - Troque o `"TODO_SUBSTITUA_POR_JUSTIFICATIVA_OFICIAL_OPENVEX"` por `"vulnerable_code_not_in_execute_path"` (ou `"code_not_reachable"`).
   - Troque o `"TODO: ..."` em `"impact_statement"` explicando em português que a `payment-api` só tem rotas JSON (`/health` e `/api/v1/payments`) e não usa `res.redirect()`.
   - *(Se você já fez a Trilha 1 no Modo Incremental, esse arquivo já está pronto.)*

---

### Etapa 3: Assinar com Cosign, Simular Ataque & Anexar Atestações — `~25 min` *(Aula 06)*

1. **Crie um par de chaves (`cosign.key` e `cosign.pub`) e assine a imagem:**
   ```bash
   COSIGN_PASSWORD="" cosign generate-key-pair
   COSIGN_PASSWORD="" cosign sign --key cosign.key --tlog-upload=false -y $IMAGE_DIGEST
   cosign verify --key cosign.pub --insecure-ignore-tlog=true localhost:5000/payment-api:v1.0.0
   ```
   *Por que `--tlog-upload=false`?* Porque estamos em um Registry local de testes, sem publicar na internet.

2. **Simule um ataque real (*Tag Tampering* — troca da etiqueta `:v1.0.0`):**
   Imagine que um invasor conseguiu trocar a imagem por trás da tag `:v1.0.0` colocando um `busybox` sem assinatura no lugar:
   ```bash
   docker pull busybox:latest
   docker tag busybox:latest localhost:5000/payment-api:v1.0.0
   docker push localhost:5000/payment-api:v1.0.0
   cosign verify --key cosign.pub --insecure-ignore-tlog=true localhost:5000/payment-api:v1.0.0
   ```
   *O que vai acontecer:* o Cosign **vai dar erro de propósito** mostrando `Error: no signatures found`. **Copie esse erro para a Seção 3 do Template 2** — ele prova que ninguém consegue se passar pela sua imagem sem sua chave.

3. **Restaure a imagem certa e "grampeie" (ateste) o SBOM e o OpenVEX nela:**
   ```bash
   docker build -f docker/Dockerfile.app -t localhost:5000/payment-api:v1.0.0 .
   docker push localhost:5000/payment-api:v1.0.0
   IMAGE_DIGEST=$(docker inspect --format '{{range .RepoDigests}}{{println .}}{{end}}' localhost:5000/payment-api:v1.0.0 | grep localhost:5000 | head -n 1)
   COSIGN_PASSWORD="" cosign sign --key cosign.key --tlog-upload=false -y $IMAGE_DIGEST
   COSIGN_PASSWORD="" cosign attest --key cosign.key --predicate dist/sbom.cdx.json --type cyclonedx --tlog-upload=false -y $IMAGE_DIGEST
   COSIGN_PASSWORD="" cosign attest --key cosign.key --predicate attestations/vex_customizado.openvex.json --type openvex --tlog-upload=false -y $IMAGE_DIGEST
   ```
   Agora leia de volta a atestação OpenVEX gravada no Registry e **cole o JSON na Seção 3 do Template 2**:
   ```bash
   cosign verify-attestation --key cosign.pub --type openvex --insecure-ignore-tlog=true $IMAGE_DIGEST | jq '.payload | @base64d | fromjson'
   ```

---

### Etapa 4: Regras Automáticas (`conftest`), Dossiê & Fechamento — `~30 min` *(Aulas 01, 05, 07 & 08)*

1. **Complete a regra Rego v1 em [`policies/openvex_audit.rego`](../../policies/openvex_audit.rego):**
   - Abra o arquivo e descomente/complete pelo menos **1 das regras `TODO`** (Regra 2 para proibir `statements` vazio, ou Regra 3 para exigir `justification` preenchida sem `TODO`). *(Se veio da Trilha 1, já está pronto.)*

2. **Rode os testes do Conftest provando um BLOQUEIO (`FAIL`) e uma APROVAÇÃO (`PASS`):**
   ```bash
   # 1. Estes dois DEVEM FALHAR (provam que a regra barra erros):
   conftest test docker/Dockerfile.inseguro -p policies/dockerfile.rego
   conftest test dist/sbom.cdx.json -p policies/sbom_license.rego

   # 2. Estes três DEVEM PASSAR (tudo em conformidade):
   conftest test docker/Dockerfile.app -p policies/dockerfile.rego
   conftest test attestations/slsa_predicate.json -p policies/slsa_provenance.rego
   conftest test attestations/vex_customizado.openvex.json -p policies/openvex_audit.rego
   ```
   *Dica:* O `sbom.cdx.json` falha porque tem a `gpl-math-lib` (`GPL-3.0`). **Copie as saídas `FAIL` e `PASS` para a Seção 4 do Template 2.**

3. **Gere o Dossiê Final que junta todas as provas:**
   ```bash
   python3 tools/generate_compliance_dossier.py
   cat dist/dossie_conformidade.json
   ```
   **Cole o JSON gerado na Seção 4 do Template 2.**

4. **Limpe a chave privada e valide sua entrega:**
   ```bash
   rm -f cosign.key
   python3 tools/selfcheck_capstone.py --trilha 2
   ```
   - Preencha a **Seção 5 (Bloco Express)** no final do [`TEMPLATE_ENTREGA_TRILHA_2.md`](./TEMPLATE_ENTREGA_TRILHA_2.md) *(ou marque **`[x] Modo Incremental`** no topo do arquivo se você já entregou a Trilha 1, e rode `selfcheck_capstone.py --trilha 2 --incremental`)*.
   - Ao sair do container (`exit`), você pode desligar o Registry local no host com `docker compose down`.

---

## O Que Entregar (Resumo Trilha 2)
- [ ] [`docs/trilha_2/TEMPLATE_ENTREGA_TRILHA_2.md`](./TEMPLATE_ENTREGA_TRILHA_2.md) preenchido com todas as saídas do terminal.
- [ ] `dist/sbom.cdx.json` e `dist/dossie_conformidade.json` gerados.
- [ ] `attestations/vex_customizado.openvex.json` e `policies/openvex_audit.rego` sem `TODO`s.
- [ ] `cosign.key` apagado + `python3 tools/selfcheck_capstone.py --trilha 2` sem erros críticos.
