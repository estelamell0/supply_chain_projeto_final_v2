# 🔴 Manual da Trilha 3: Automação na Nuvem (GitHub Actions & Keyless)

**Nota Máxima:** `10,0`  
**Tempo Estimado:** **~95 min** *(no máximo 2h00)*  
**O Que Você Precisa:** Uma conta gratuita no **GitHub** (e navegador para usar o **GitHub Codespaces**). **Não precisa de Docker instalado no seu PC.**  
**O Que Você Vai Praticar:** Todos os 8 assuntos do curso (Aulas 01 a 08) em uma esteira real de nuvem, com bloqueio automático de licença proibida e assinatura sem senha/chave fixa (*Keyless*).

---

## Como Funciona Esta Trilha?
Nesta trilha, quem constrói a imagem, gera o SBOM, roda as regras do Conftest e assina a imagem é o robô do **GitHub Actions** na nuvem.

A jornada acontece em **3 grandes momentos**:
1. **Você arruma 2 pequenos `TODO`s na esteira** (e completa o OpenVEX + Rego v1) antes de subir para o GitHub.
2. **Ciclo Vermelho → Verde:** No 1º envio, a esteira **vai falhar de propósito** porque existe uma biblioteca proibida (`gpl-math-lib`, licença `GPL-3.0`). Você guarda a prova do bloqueio, remove essa biblioteca e envia de novo para a esteira ficar **Verde**.
3. **Verificação Pública:** Você deixa o pacote público no GitHub (GHCR) e confere a assinatura pelo **GitHub Codespaces** (direto no navegador, sem instalar nada no PC).

---

## Antes de Começar (Preparando o Repositório)
1. Crie um repositório **Público** novo no seu GitHub (ex.: `payment-api-capstone`).
2. Copie o conteúdo da pasta `supply_chain_final_v2/` para a raiz desse repositório na branch `main`.
3. **Atenção muito importante:** Na hora do `git add .`, a pasta `src/node_modules/` **precisa subir junto** para o GitHub (o `.gitignore` deste projeto já está preparado para deixá-la passar). Sem ela, o pacote corporativo simulado `@corp/payment-vault` não será encontrado na nuvem.

---

## Passo a Passo Detalhado

### Etapa 1: Corrigir os `TODO`s da Esteira, OpenVEX & Rego v1 — `~25 min` *(Aulas 05 & 07)*

Antes de dar `git push`, abra os 3 arquivos abaixo no seu editor:

1. **Arquivo [`.github/workflows/golden_pipeline_capstone.yml`](../../.github/workflows/golden_pipeline_capstone.yml):**
   - **TODO 1 (Permissão para assinatura sem chave):** Por volta da linha 15, apague o `# ` da frente de `# id-token: write` para deixá-la ativa alinhada abaixo de `packages: write`.
   - **TODO 2 (Travar Action por código SHA-1):** Por volta da linha 34, troque `uses: actions/setup-node@v4` pelo código imutável que já está anotado no comentário logo acima dela:
     ```yaml
     uses: actions/setup-node@60edb5dd545a775178f52524783378180af0d1f8
     ```
   - *(Obs.: O outro arquivo `.github/workflows/pipeline_vulneravel.yml` tem `if: false` e serve apenas de exemplo inseguro; não precisa mexer nele.)*

2. **Arquivo [`attestations/vex_customizado.openvex.json`](../../attestations/vex_customizado.openvex.json):**
   - No 3º bloco (`CVE-2024-29041` no `express`), substitua os dois textos com `TODO` por `"vulnerable_code_not_in_execute_path"` e pela explicação em português de que a `payment-api` não usa `res.redirect()`. *(Se veio das Trilhas 1 ou 2, já está pronto.)*

3. **Arquivo [`policies/openvex_audit.rego`](../../policies/openvex_audit.rego):**
   - Descomente e complete pelo menos **1 das regras `TODO`** (Regra 2 ou Regra 3) para que o Conftest valide seu arquivo OpenVEX na esteira. *(Se veio das Trilhas 1 ou 2, já está pronto.)*

4. **Teste rápido antes do 1º push:**
   ```bash
   python3 tools/selfcheck_capstone.py --trilha 3
   ```
   *O que esperar:* Ele deve dar `[PASS]` nos `TODO`s do workflow, no OpenVEX, no Rego e no mock `@corp/payment-vault`, deixando apenas um aviso (`[WARN]`) dizendo que a `gpl-math-lib` ainda está lá (e ela **precisa** estar lá para o próximo passo).

---

### Etapa 2: Ciclo Vermelho → Correção → Verde no GitHub Actions — `~35 min` *(Aulas 02, 03, 04 & 07)*

1. **1º Push (Execução Vermelha de Propósito):**
   ```bash
   git add .
   git commit -m "chore: configura esteira capstone"
   git push origin main
   ```
   - Vá no seu repositório no GitHub e clique na aba **Actions**.
   - Clique na execução que abriu. Você verá o **Gate 1** (`Dockerfile` e `OpenVEX`) passar, mas o passo **`Generate CycloneDX SBOM & Enforce License Policy`** vai **falhar** mostrando `VIOLACAO DE LICENCA: O componente 'gpl-math-lib@1.0.0' possui licenca proibida 'GPL-3.0-only'`.
   - **Guarde agora no seu [`TEMPLATE_ENTREGA_TRILHA_3.md`](./TEMPLATE_ENTREGA_TRILHA_3.md):** o link dessa execução que falhou e o trecho do log com o erro `GPL-3.0`.

2. **Remova a biblioteca proibida `gpl-math-lib` nos 3 lugares:**
   - **Lugar 1 — [`src/package.json`](../../src/package.json):** apague a linha `"gpl-math-lib": "1.0.0"` (e tire a vírgula sobrando no final da linha de cima, se houver, para não quebrar o JSON).
   - **Lugar 2 — [`src/package-lock.json`](../../src/package-lock.json):**
     - Perto da linha 14, apague `"gpl-math-lib": "1.0.0",`;
     - Perto da linha 379, apague todo o bloco `"node_modules/gpl-math-lib": { ... },`.
   - **Lugar 3 — Pasta física:** apague a pasta `src/node_modules/gpl-math-lib`.

3. **2º Push (Execução Verde + Assinatura Keyless):**
   ```bash
   git add .
   git commit -m "fix: remove dependencia gpl-math-lib"
   git push origin main
   ```
   - Acompanhe na aba **Actions**: agora tudo ficará **Verde**.
   - Abra o passo **`Sign Container Image (Keyless OIDC)`** no log da execução verde: lá dentro estará impresso o comando exato `cosign verify ...` já preenchido com o seu usuário, repositório e digest, além da linha `tlog entry created with index: <NUMERO>` (esse número é o registro no **Rekor**).

---

### Etapa 3: Deixar Pacote Público, Conferir Assinatura & Artifacts — `~35 min` *(Aulas 01, 06 & 08)*

1. **Deixe a imagem pública no GHCR:**
   - Na página inicial do seu repositório no GitHub, olhe a coluna da direita em **Packages** e clique em **`payment-api`**.
   - Clique em **Package settings** (canto direito) → desça até **Danger Zone** → **Change package visibility** → escolha **Public** e confirme. *(Sem isso, o comando público de verificação dá erro de permissão.)*

2. **Confirme a assinatura sem precisar de Docker no seu PC (via GitHub Codespaces):**
   - Volte para a página principal do repositório, clique no botão verde **`<> Code`** → aba **Codespaces** → **Create codespace on main**.
   - Quando o terminal do navegador abrir, baixe o `cosign` com 1 comando:
     ```bash
     curl -fsSL https://github.com/sigstore/cosign/releases/download/v2.4.1/cosign-linux-amd64 -o /tmp/cosign && chmod +x /tmp/cosign
     ```
   - Agora rode a verificação da imagem (trocando `cosign` por `/tmp/cosign` no comando copiado do log da sua Run Verde) e verifique também a atestação OpenVEX:
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
   - **Copie as saídas para a Seção 3 do seu Template 3.**
   - *(Opcional legal: abra `https://search.sigstore.dev/?logIndex=<NUMERO>` no navegador para ver sua assinatura gravada para sempre no livro público do Rekor.)*

3. **Baixe os Artifacts e finalize o relatório:**
   - Na aba **Summary** da Run Verde no GitHub Actions, role até **Artifacts** e confirme o pacote **`supply-chain-evidence-bundle`** (ele contém `sbom.cdx.json`, `dossie_conformidade.json` e `vex_customizado.openvex.json`).
   - Preencha [`docs/trilha_3/TEMPLATE_ENTREGA_TRILHA_3.md`](./TEMPLATE_ENTREGA_TRILHA_3.md) (respondendo o **Bloco Express**, ou marcando **`[x] Modo Incremental`** no topo se já fez a Trilha 1 ou 2) e valide:
     ```bash
     python3 tools/selfcheck_capstone.py --trilha 3
     ```
     *(Use `--incremental` se marcou Modo Incremental.)*

---

## O Que Entregar (Resumo Trilha 3)
- [ ] Repositório público no GitHub com os `TODO`s resolvidos (`id-token: write`, SHA-1 no `setup-node`, `vex_customizado.openvex.json` e `openvex_audit.rego`).
- [ ] Link e log da **1ª execução bloqueada** (`GPL-3.0`) + commit de remoção + link da **2ª execução verde**.
- [ ] Saída do `cosign verify` e `verify-attestation` + índice do Rekor + Artifacts gerados.
- [ ] [`docs/trilha_3/TEMPLATE_ENTREGA_TRILHA_3.md`](./TEMPLATE_ENTREGA_TRILHA_3.md) preenchido e validado com `python3 tools/selfcheck_capstone.py --trilha 3`.
