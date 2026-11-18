# 🔵 Manual da Trilha 1: Leitura, Auditoria & Código (Sem Docker e Sem Nuvem)

**Nota Máxima:** `10,0`  
**Tempo Estimado:** **~95 min** *(no máximo 2h00)*  
**O Que Você Precisa:** Apenas um editor de texto (como o VS Code). **Não precisa instalar Docker nem criar conta na nuvem.**  
**O Que Você Vai Praticar:** Todos os 8 assuntos do curso (Aulas 01 a 08) analisando arquivos reais e escrevendo 3 arquivos de correção.

---

## Como Funciona Esta Trilha?
Nesta trilha, você vai atuar como **Auditor(a) e Arquiteto(a) de Segurança**. Tudo o que você precisa responder fica no arquivo [`TEMPLATE_ENTREGA_TRILHA_1.md`](./TEMPLATE_ENTREGA_TRILHA_1.md) (ou na versão Word [`TEMPLATE_ENTREGA_TRILHA_1.docx`](./TEMPLATE_ENTREGA_TRILHA_1.docx), se preferir preencher no Word).

Além do relatório preenchido, você vai criar/completar **3 arquivos de código**:
1. `docker/Dockerfile.hardened` (um Dockerfile corrigido);
2. `attestations/vex_customizado.openvex.json` (completar 1 justificativa de segurança);
3. `policies/openvex_audit.rego` (completar 2 regras de bloqueio automático).

> 💡 **Precisa entender alguma sigla?** Consulte o [`GLOSSARIO_SUPPLY_CHAIN.md`](../GLOSSARIO_SUPPLY_CHAIN.md) ou o [`COMO_LER_OS_ARTEFATOS.md`](../COMO_LER_OS_ARTEFATOS.md).

---

## Passo a Passo Detalhado

### Etapa 1: Riscos da Cadeia & Segurança de Dependências — `~20 min` *(Aulas 01 & 02)*

1. **Abra o seu relatório:** [`docs/trilha_1/TEMPLATE_ENTREGA_TRILHA_1.md`](./TEMPLATE_ENTREGA_TRILHA_1.md) (ou o `.docx`).
2. **Preencha a tabela dos 6 Elos (Seção 1.1):**
   - O **Elo 1 (Source)** já vem pronto como exemplo para você ver o tamanho esperado da resposta (1 a 2 linhas por coluna).
   - Preencha os Elos **2 a 6** pensando na aplicação `payment-api`:
     - *Elo 2 (Dependencies):* Risco de alguém sequestrar o pacote `@corp/payment-vault` ou rodar vírus no `npm install`. Controle: `src/.npmrc` + `--ignore-scripts` + `package-lock.json`. (Framework: NIST SSDF **PW.4 / PS.3**).
     - *Elo 3 (Build CI/CD):* Risco de alguém alterar a esteira (PPE) ou usar permissões `write-all` / tags `@v3`. Controle: `permissions` mínimas + fixar Actions por SHA-1. (Framework: **SLSA Build L2** / NIST SSDF **PO.3**).
     - *Elo 4 (Artifacts):* Risco de tags mutáveis (`:latest`) ou container rodando como `root`. Controle: Digest `@sha256:` + `USER node` + SBOM. (Framework: **SLSA** / NIST SSDF **PS.2**).
     - *Elo 5 (Distribution):* Risco de trocarem a imagem no Registry. Controle: Assinatura Cosign + atestações *in-toto*. (Framework: **SLSA** / **SCVS**).
     - *Elo 6 (Runtime/Compliance):* Risco de subir imagem proibida em produção. Controle: Gate Conftest (Rego v1), Admission Control e Dossiê JSON. (Framework: NIST SSDF **PW.6 / RV.1** / **EO 14028**).
3. **Audite os 3 arquivos da pasta `src/` (Seção 1.2):**
   - Abra [`src/.npmrc`](../../src/.npmrc): veja que ele manda qualquer pacote `@corp/...` ir direto para `https://npm.corp.internal/` (evitando *Dependency Confusion*).
   - Abra [`src/package.json`](../../src/package.json) e [`src/package-lock.json`](../../src/package-lock.json): note que `express` está escrito como `"^4.18.2"` no `package.json` (o `^` permite atualizar sozinho), enquanto o `package-lock.json` trava a versão exata e o hash `sha512`. Explique esse risco e por que `--ignore-scripts` impede códigos maliciosos de `postinstall`.

---

### Etapa 2: Ler o SBOM & Completar o Laudo OpenVEX — `~25 min` *(Aulas 03 & 04)*

1. **Inspecione o SBOM pronto:** Abra [`attestations/sbom_referencia.cdx.json`](../../attestations/sbom_referencia.cdx.json) (não precisa rodar nenhum programa).
   - Procure o bloco `"components": [...]`.
   - Copie para o relatório os códigos **`purl`** que aparecem lá (ex.: `pkg:npm/express@4.18.2`, `pkg:npm/gpl-math-lib@1.0.0`, etc.) e explique com suas palavras para que serve o PURL (identificar pacotes sem confusão na hora de buscar falhas/CVEs).
   - Olhe os campos `"licenses"` e descubra **qual pacote usa a licença proibida `GPL-3.0`** (dica: é a `gpl-math-lib`) e diga o que deve ser feito no `package.json` (remover a dependência).
2. **Complete o laudo OpenVEX:** Abra [`attestations/vex_customizado.openvex.json`](../../attestations/vex_customizado.openvex.json).
   - Os 2 primeiros blocos já vêm prontos como modelo (`CVE-2022-24999` e `CVE-2020-28500`).
   - No **3º bloco (`CVE-2024-29041` no `express`)**, substitua os dois textos com `TODO`:
     - Em `"justification"`, troque `"TODO_SUBSTITUA_POR_JUSTIFICATIVA_OFICIAL_OPENVEX"` por uma justificativa oficial do OpenVEX v0.2.0 (ex.: `"vulnerable_code_not_in_execute_path"` ou `"code_not_reachable"`).
     - Em `"impact_statement"`, explique em português por que a `payment-api` não é afetada (dica: olhe [`src/app.js`](../../src/app.js) — a API só responde JSON em `/health` e `/api/v1/payments`, nunca chama `res.redirect()`).
   - Marque o `[x]` na Seção 2.2 do seu relatório e resuma a justificativa em 2 linhas.

---

### Etapa 3: Deixar o Dockerfile Seguro & Comparar Pipelines CI/CD — `~25 min` *(Aulas 05 & 06)*

1. **Crie o arquivo `docker/Dockerfile.hardened`:**
   - Compare [`docker/Dockerfile.inseguro`](../../docker/Dockerfile.inseguro) (cheio de erros: `FROM node:latest`, `npm install` sem trava, `USER root`) com [`docker/Dockerfile.app`](../../docker/Dockerfile.app).
   - Crie um novo arquivo chamado **`docker/Dockerfile.hardened`** baseado no `Dockerfile.app`, fazendo **dois cuidados principais**:
     1. Troque `FROM node:18-alpine` pelo endereço fixo com hash SHA-256 imutável:
        ```dockerfile
        FROM node:18-alpine@sha256:8d6421d663b4c28fd3ebc498332f249011d118945588d0a35cb9bc4b8ca09d9e
        ```
     2. Garanta que exista `USER node` (usuário comum, nunca `root`), e adicione comentários `#` explicando por que não usamos `npm install` solto.
   - Preencha a tabelinha da Seção 3.1 no seu relatório.
2. **Compare as duas esteiras do GitHub Actions:** Abra lado a lado [`pipeline_vulneravel.yml`](../../.github/workflows/pipeline_vulneravel.yml) e [`golden_pipeline_capstone.yml`](../../.github/workflows/golden_pipeline_capstone.yml) e responda às 3 perguntas da Seção 3.2:
   - **Pergunta 1:** Por que `permissions: write-all` é perigosa e o que faz cada uma das 3 permissões da esteira segura (`contents: read`, `packages: write`, `id-token: write`)?
   - **Pergunta 2:** Qual a diferença entre usar `@v4` e usar o código SHA-1 de 40 caracteres (`@b4ffde65...`), e o que acontece no GitHub Actions se o SHA estiver errado? *(O GitHub aborta a execução na hora.)*
   - **Pergunta 3:** Abra [`attestations/keyless_bundle_sample.json`](../../attestations/keyless_bundle_sample.json) (ou, se tiver Python, rode `python3 tools/verify_keyless_bundle.py`) e explique o papel do **Fulcio** (dá o certificado temporário de 10 min) e do **Rekor** (guarda a prova no livro público que não pode ser apagado).

---

### Etapa 4: Completar as Regras em Rego v1 & Fechar o Relatório — `~25 min` *(Aulas 07 & 08)*

1. Abra o arquivo guiado [`policies/openvex_audit.rego`](../../policies/openvex_audit.rego).
   - A **Regra 1** já vem pronta funcionando como exemplo (ela barra se o `@context` for diferente de `"https://openvex.dev/ns/v0.2.0"`).
   - Descomente e complete a **Regra 2** (para bloquear se `statements` estiver vazio — usando `stmts := object.get(input, "statements", [])` e `count(stmts) == 0`).
   - Descomente e complete a **Regra 3** (para bloquear se algum item com `stmt.status == "not_affected"` estiver com `justification` vazia `""` ou começando com `"TODO"`).
2. Na Seção 4 do seu relatório, explique por que usar `deny contains msg if { ... }` em Rego v1 é melhor do que apenas devolver `allow := false` *(porque `deny contains` mostra todas as mensagens de erro detalhadas de uma vez, em vez de só dizer "negado")*.

> 💡 **Conferência Opcional (Recomendada):** Nenhuma etapa da Trilha 1 exige rodar scripts. Mas, se você tiver Python 3 no computador e quiser checar se não esqueceu nenhum arquivo ou lacuna `[...]`, rode:
> ```bash
> python3 tools/selfcheck_capstone.py --trilha 1
> ```

---

## O Que Entregar (Resumo Trilha 1)
- [ ] [`docs/trilha_1/TEMPLATE_ENTREGA_TRILHA_1.md`](./TEMPLATE_ENTREGA_TRILHA_1.md) (ou o Word [`TEMPLATE_ENTREGA_TRILHA_1.docx`](./TEMPLATE_ENTREGA_TRILHA_1.docx)) todo preenchido sem `[...]`.
- [ ] `docker/Dockerfile.hardened` com `@sha256:` fixo e `USER node`.
- [ ] `attestations/vex_customizado.openvex.json` sem nenhum `TODO`.
- [ ] `policies/openvex_audit.rego` com as 3 regras `deny contains` completas.

> 💡 **Quer evoluir depois (Modo Incremental)?** Se decidir fazer a Trilha 2 ou 3 depois, você já vai levar esses 3 arquivos prontos e não precisará responder o Bloco Express repetido.
