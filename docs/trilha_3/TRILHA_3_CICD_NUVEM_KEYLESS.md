# 🔴 Trilha 3: Engenharia de Esteira em Nuvem & Keyless OIDC

**Nota Máxima:** `10,0`  
**Tempo Estimado:** **~95 min** *(Teto máximo: 2h00)*  
**Camada Tecnológica:** Automação em nuvem no **GitHub Actions**, Quality Gates com **Conftest (Rego v1)**, registro no **GHCR** e assinatura **Keyless OIDC (Fulcio + Rekor público)** — **não exige Docker local**.  
**Cobertura Curricular:** Aulas 01 a 08 completas.

---

## Pré-Requisitos
- Conta gratuita no **GitHub** com um **repositório público** criado a partir do conteúdo de `supply_chain_final_v2/` na raiz (branch `main`).
- **Atenção ao `git add .`:** Preserve a pasta `src/node_modules/` no commit (o `.gitignore` já está configurado para mantê-la), garantindo que o mock `@corp/payment-vault` funcione na nuvem.

---

## Roteiro Cronometrado (Alvo: 95 min)

### Etapa 1: Hardening da Esteira & Rego v1 ("Conserte os `TODO`s") — `~25 min` *(Aulas 05 & 07)*
Antes de fazer o primeiro `git push` para a branch `main`, execute as correções guiadas:
1. Em [`.github/workflows/golden_pipeline_capstone.yml`](../../.github/workflows/golden_pipeline_capstone.yml):
   - **TODO 1 (Menor Privilégio + OIDC):** Descomente `id-token: write` no bloco `permissions:`;
   - **TODO 2 (SHA Pinning):** Substitua `actions/setup-node@v4` pelo Commit SHA-1 imutável já anotado no comentário (`actions/setup-node@60edb5dd545a775178f52524783378180af0d1f8`).
   - *(Note que `.github/workflows/pipeline_vulneravel.yml` possui `if: false` para não conflitar na nuvem.)*
2. Complete os marcadores `TODO` em:
   - [`attestations/vex_customizado.openvex.json`](../../attestations/vex_customizado.openvex.json) (3º statement para `CVE-2024-29041` com `justification` oficial OpenVEX);
   - [`policies/openvex_audit.rego`](../../policies/openvex_audit.rego) (ative pelo menos 1 regra `TODO`, ou ambas — *se veio das Trilhas 1 ou 2 em Modo Incremental, esses arquivos já estão prontos!*).
3. Confira localmente antes do primeiro push (neste ponto, apenas o aviso de `gpl-math-lib` ainda presente é esperado):
   ```bash
   python3 tools/selfcheck_capstone.py --trilha 3
   ```

### Etapa 2: Ciclo Red → Remediação → Green no Actions — `~35 min` *(Aulas 02, 03, 04 & 07)*
1. **1º Push (`Red` Intencional — Prova do Gate `GPL-3.0`):**
   - Faça `git add .`, `git commit -m "chore: setup esteira capstone"` e `git push origin main`.
   - Acompanhe a aba **Actions** no GitHub: o Gate 1 (Dockerfile & OpenVEX) **passará**, mas o Gate 2 (`sbom_license.rego`) **bloqueará a esteira de propósito** ao detectar `gpl-math-lib` (`GPL-3.0`).
   - **Salve o link da run bloqueada e copie o trecho do log de falha do Conftest!**
2. **Remediação da Dependência Proibida (`~10 min`):**
   Remova `gpl-math-lib` exatamente nos 3 pontos abaixo:
   - `src/package.json`: remova a linha `"gpl-math-lib": "1.0.0"` (e a vírgula sobrando na linha anterior);
   - `src/package-lock.json`: remova `"gpl-math-lib": "1.0.0"` em `packages[""].dependencies` e todo o bloco `"node_modules/gpl-math-lib": { ... }`;
   - Apague a pasta `src/node_modules/gpl-math-lib`.
3. **2º Push (`Green` — Publicação & Assinatura Keyless):**
   - Faça `git commit -am "fix: remove gpl-math-lib copyleft dependency"` e `git push origin main`.
   - Confirme a run **Verde**, que publica a imagem no GHCR, gera SBOM/Dossiê e assina com **Fulcio + Rekor público**.

### Etapa 3: GHCR Público, Verificação OIDC & Síntese — `~35 min` *(Aulas 01, 06 & 08)*
1. **Visibilidade Pública no GHCR:** Na página inicial do seu repositório no GitHub, acesse à direita **Packages → `payment-api` → Package settings → Change package visibility → Public** (sem isso, a verificação pública exigiria token).
2. **Verificação Pública Keyless (Sem Docker Local!):**
   - **Opção Recomendada (1 clique no navegador — GitHub Codespaces):** No seu repositório no GitHub, clique em **`<> Code` → Codespaces → Create codespace on main** e instale o `cosign` em segundos:
     ```bash
     curl -fsSL https://github.com/sigstore/cosign/releases/download/v2.4.1/cosign-linux-amd64 -o /tmp/cosign && chmod +x /tmp/cosign
     ```
     Em seguida, execute os comandos abaixo (copiando o comando pré-preenchido impresso no log da etapa **`Sign Container Image (Keyless OIDC)`** da sua run verde):
     ```bash
     /tmp/cosign verify \
       --certificate-identity="https://github.com/<SEU-USUARIO>/<SEU-REPO>/.github/workflows/golden_pipeline_capstone.yml@refs/heads/main" \
       --certificate-oidc-issuer="https://token.actions.githubusercontent.com" \
       ghcr.io/<seu-usuario-minusculo>/<seu-repo-minusculo>/payment-api@sha256:<DIGEST>

     /tmp/cosign verify-attestation \
       --type openvex \
       --certificate-identity="https://github.com/<SEU-USUARIO>/<SEU-REPO>/.github/workflows/golden_pipeline_capstone.yml@refs/heads/main" \
       --certificate-oidc-issuer="https://token.actions.githubusercontent.com" \
       ghcr.io/<seu-usuario-minusculo>/<seu-repo-minusculo>/payment-api@sha256:<DIGEST> | jq '.payload | @base64d | fromjson'
     ```
   - *(Alternativa: se você possui o container da Trilha 2 rodando localmente, basta usar `cosign verify` e `cosign verify-attestation` direto dele!)*
   - Consulte também o índice gravado no log (`tlog entry created with index: ...`) em `https://search.sigstore.dev/?logIndex=<INDICE>` e baixe o Artifact **`supply-chain-evidence-bundle`** na aba **Summary** da run verde.
3. Preencha [`docs/trilha_3/TEMPLATE_ENTREGA_TRILHA_3.md`](./TEMPLATE_ENTREGA_TRILHA_3.md) (incluindo o **Bloco Express de Aulas 01 & 02**, ou marcando **`[x] Modo Incremental`** se já entregou a Trilha 1 ou 2) e execute:
   ```bash
   python3 tools/selfcheck_capstone.py --trilha 3
   ```

---

## O Que Entregar (Checklist Trilha 3)
- [ ] Link do repositório público com os `TODO`s resolvidos (`id-token: write`, `@SHA-1`, `openvex_audit.rego` e `vex_customizado.openvex.json`).
- [ ] Link/log da **1ª run bloqueada** (`GPL-3.0`) + commit de remediação + link da **2ª run verde** com Artifacts.
- [ ] Saída pública do `cosign verify` + `cosign verify-attestation` e Log Index do Rekor.
- [ ] [`docs/trilha_3/TEMPLATE_ENTREGA_TRILHA_3.md`](./TEMPLATE_ENTREGA_TRILHA_3.md) preenchido e validado com `python3 tools/selfcheck_capstone.py --trilha 3`.
