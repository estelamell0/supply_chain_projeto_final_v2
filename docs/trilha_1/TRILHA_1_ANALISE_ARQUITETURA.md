# 🔵 Trilha 1: Análise, Auditoria Estática & Design

**Nota Máxima:** `10,0`  
**Tempo Estimado:** **~95 min** *(Teto máximo: 2h00)*  
**Camada Tecnológica:** Análise estática, revisão de código, design de políticas Rego v1 e modelagem formal — **zero exigência de Docker ou nuvem**.  
**Cobertura Curricular:** Aulas 01 a 08 completas.

---

## Objetivo da Trilha
Demonstrar domínio técnico de ponta a ponta sobre os 8 módulos de *Supply Chain Security* analisando manifestos, escrevendo políticas de conformidade e estruturando controles preventivos para o microsserviço `payment-api`.

---

## Roteiro Cronometrado (Alvo: 95 min)

### Etapa 1: Matriz de Riscos (6 Elos) & Auditoria de Dependências — `~20 min` *(Aulas 01 & 02)*
Preencha a Seção 1 de [`docs/trilha_1/TEMPLATE_ENTREGA_TRILHA_1.md`](./TEMPLATE_ENTREGA_TRILHA_1.md):
1. **Matriz Compacta dos 6 Elos:** Preencha os Elos **2 a 6** (Dependencies, Build, Artifacts, Distribution, Runtime) seguindo o modelo conciso do Elo 1 (Source), mapeando cada risco aos frameworks **SLSA v1.0** e **NIST SP 800-218 (SSDF)**.
2. **Auditoria de [`src/.npmrc`](../../src/.npmrc), [`src/package.json`](../../src/package.json) e [`src/package-lock.json`](../../src/package-lock.json):**
   - Explique como `src/.npmrc` + `npm install --ignore-scripts` mitigam *Dependency Confusion* e ataques *postinstall*.
   - Aponte o risco do range semântico `^4.18.2` no `express` frente ao bloqueio por integridade SHA-512 no lockfile.

### Etapa 2: Análise de SBOM & Triagem OpenVEX — `~25 min` *(Aulas 03 & 04)*
1. Sem rodar `syft`, inspecione [`attestations/sbom_referencia.cdx.json`](../../attestations/sbom_referencia.cdx.json):
   - Liste os **PURLs** catalogados e explique como o PURL permite correlação determinística de CVEs.
   - Identifique o componente que viola a política comercial (`GPL-3.0`) e descreva a correção necessária.
2. Abra o esqueleto [`attestations/vex_customizado.openvex.json`](../../attestations/vex_customizado.openvex.json) e complete o **3º statement (`CVE-2024-29041` no `express`)**:
   - Substitua os marcadores `TODO` por uma `justification` oficial válida da especificação OpenVEX v0.2.0 (ex.: `vulnerable_code_not_in_execute_path` ou `code_not_reachable`) e redija um `impact_statement` técnico objetivo.

### Etapa 3: Hardening de Container, Auditoria CI/CD & Sigstore — `~25 min` *(Aulas 05 & 06)*
1. Compare [`docker/Dockerfile.inseguro`](../../docker/Dockerfile.inseguro) e [`docker/Dockerfile.app`](../../docker/Dockerfile.app) e crie **`docker/Dockerfile.hardened`** aplicando:
   - `FROM` fixado por **Digest SHA-256 imutável** (`FROM node:18-alpine@sha256:8d6421d663b4c28fd3ebc498332f249011d118945588d0a35cb9bc4b8ca09d9e`);
   - Execução explícita como usuário não-privilegiado (`USER node`).
2. Compare [`pipeline_vulneravel.yml`](../../.github/workflows/pipeline_vulneravel.yml) e [`golden_pipeline_capstone.yml`](../../.github/workflows/golden_pipeline_capstone.yml) e responda aos **3 checks objetivos** no template:
   - Impacto de `permissions: write-all` vs. escopo mínimo (`contents: read`, `packages: write`, `id-token: write`);
   - Diferença entre tag mutável `@v4` e Commit SHA-1 de 40 caracteres (e efeito de um SHA inválido no Actions);
   - Papéis do **Fulcio** (certificado efêmero OIDC) e do **Rekor** (Árvore de Merkle imutável), inspecionando [`attestations/keyless_bundle_sample.json`](../../attestations/keyless_bundle_sample.json) ou executando `python3 tools/verify_keyless_bundle.py`.

### Etapa 4: Policy as Code (Rego v1) & Autoverificação — `~25 min` *(Aulas 07 & 08)*
1. Abra o esqueleto guiado [`policies/openvex_audit.rego`](../../policies/openvex_audit.rego) (a Regra 1 já vem pronta como referência).
2. Implemente e descomente as **Regras 2 e 3** em sintaxe `import rego.v1` válida:
   - **Regra 2:** Bloquear caso o array `statements` esteja ausente ou vazio (`count == 0`);
   - **Regra 3:** Bloquear caso algum statement com `status == "not_affected"` esteja com `justification` vazia ou contendo `"TODO"`.
3. Preencha a Etapa 4 do template explicando por que `deny contains msg if` é preferível a um booleano simples (`allow := false`) e valide tudo localmente:
   ```bash
   python3 tools/selfcheck_capstone.py --trilha 1
   ```

---

## O Que Entregar (Checklist Trilha 1)
- [ ] [`docs/trilha_1/TEMPLATE_ENTREGA_TRILHA_1.md`](./TEMPLATE_ENTREGA_TRILHA_1.md) preenchido sem lacunas `[...]`.
- [ ] `docker/Dockerfile.hardened` com digest SHA-256 e `USER node`.
- [ ] `attestations/vex_customizado.openvex.json` atualizado sem `TODO`s.
- [ ] `policies/openvex_audit.rego` com as 3 regras `deny contains` ativas.
- [ ] `python3 tools/selfcheck_capstone.py --trilha 1` finalizado com `[RESULTADO] Verificacao estrutural concluida sem erros criticos!`.

> 💡 **Quer evoluir depois (Modo Incremental)?** Todos os arquivos que você criou aqui (`Dockerfile.hardened`, `vex_customizado.openvex.json` e `openvex_audit.rego`) serão executados diretamente na **Trilha 2** e na **Trilha 3**, dispensando o Bloco Express conceitual repetido!
