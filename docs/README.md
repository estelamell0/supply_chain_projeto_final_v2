# Índice & Instruções Gerais — Projeto Final Capstone (`docs/`)

Bem-vindo(a) à central de documentação do **Projeto Final de Supply Chain Security (`payment-api`)**.  
Todas as três trilhas cobrem **todos os conceitos das Aulas 01 a 08**, valem até **10,0 pontos** e foram desenhadas para conclusão em **até 2 horas** (~95 a 100 min).

---

## 1. Navegação da Documentação

### Guias Gerais (`docs/`)
- [`RUBRICA_AVALIACAO.md`](./RUBRICA_AVALIACAO.md) — Critérios e pesos oficiais (0 a 10,0) nas 5 dimensões.
- [`CHECKLIST_ENTREGA.md`](./CHECKLIST_ENTREGA.md) — Lista de verificação final para todas as trilhas.
- [`COMO_LER_OS_ARTEFATOS.md`](./COMO_LER_OS_ARTEFATOS.md) — Guia de leitura de SBOM, OpenVEX, SLSA, Bundle Sigstore e Rego v1.
- [`README_POLITICAS.md`](./README_POLITICAS.md) — Resumo e exemplos das políticas Rego v1 em [`../policies/`](../policies/).

### Pastas por Trilha
| Trilha | Pasta | Roteiro Passo a Passo | Template(s) de Entrega |
| :--- | :--- | :--- | :--- |
| **🔵 Trilha 1 — Análise, Auditoria & Design** *(Zero Docker/Nuvem)* | [`trilha_1/`](./trilha_1/) | [`TRILHA_1_ANALISE_ARQUITETURA.md`](./trilha_1/TRILHA_1_ANALISE_ARQUITETURA.md) | [`TEMPLATE_ENTREGA_TRILHA_1.md`](./trilha_1/TEMPLATE_ENTREGA_TRILHA_1.md) • [`TEMPLATE_ENTREGA_TRILHA_1.docx`](./trilha_1/TEMPLATE_ENTREGA_TRILHA_1.docx) *(Word)* |
| **🟡 Trilha 2 — Sandbox CLI Local** *(Docker + Registry)* | [`trilha_2/`](./trilha_2/) | [`TRILHA_2_EXECUCAO_LOCAL_CLI.md`](./trilha_2/TRILHA_2_EXECUCAO_LOCAL_CLI.md) | [`TEMPLATE_ENTREGA_TRILHA_2.md`](./trilha_2/TEMPLATE_ENTREGA_TRILHA_2.md) |
| **🔴 Trilha 3 — Esteira em Nuvem & Keyless** *(GitHub Actions)* | [`trilha_3/`](./trilha_3/) | [`TRILHA_3_CICD_NUVEM_KEYLESS.md`](./trilha_3/TRILHA_3_CICD_NUVEM_KEYLESS.md) | [`TEMPLATE_ENTREGA_TRILHA_3.md`](./trilha_3/TEMPLATE_ENTREGA_TRILHA_3.md) |

---

## 2. Como Funciona & Regras Gerais

1. **Escolha 1 Trilha (ou evolua de forma incremental):**
   - Você deve concluir **pelo menos 1 trilha** (`Trilha 1`, `Trilha 2` ou `Trilha 3`).
   - Se quiser evoluir (`1 → 2 → 3`), marque **`[x] Modo Incremental`** no cabeçalho dos templates das Trilhas 2 e 3 para reutilizar os artefatos já criados e dispensar o **Bloco Express** repetido.
2. **Aterrissagem Segura:**
   - Se iniciar na Trilha 2 ou 3 e enfrentar bloqueios de ambiente perto do prazo, você pode migrar para a **Trilha 1** entregando o relatório e os artefatos estáticos correspondentes sem prejuízo de nota.
3. **Segurança de Chaves:**
   - Nunca inclua arquivos `cosign.key` reais em repositórios públicos no GitHub.
4. **Autoverificação Obrigatória Antes da Entrega:**
   ```bash
   python3 tools/selfcheck_capstone.py --trilha <1|2|3>
   ```
   *(Adicione `--incremental` se estiver usando o Modo Incremental.)*

---

## 3. O Que Entregar por Trilha

- **🔵 Trilha 1:**
  - Relatório preenchido ([`docs/trilha_1/TEMPLATE_ENTREGA_TRILHA_1.md`](./trilha_1/TEMPLATE_ENTREGA_TRILHA_1.md) ou versão Word [`TEMPLATE_ENTREGA_TRILHA_1.docx`](./trilha_1/TEMPLATE_ENTREGA_TRILHA_1.docx));
  - `docker/Dockerfile.hardened` criado com `@sha256:` e `USER node`;
  - [`attestations/vex_customizado.openvex.json`](../attestations/vex_customizado.openvex.json) completo sem marcadores `TODO`;
  - [`policies/openvex_audit.rego`](../policies/openvex_audit.rego) com as Regras 2 e 3 implementadas em `import rego.v1`.
- **🟡 Trilha 2:**
  - Relatório preenchido ([`docs/trilha_2/TEMPLATE_ENTREGA_TRILHA_2.md`](./trilha_2/TEMPLATE_ENTREGA_TRILHA_2.md)) com logs reais (`$IMAGE_DIGEST`, bloqueio de *tag tampering* no Cosign, `verify-attestation`, `FAIL`/`PASS` do Conftest e Dossiê);
  - `dist/sbom.cdx.json` e `dist/dossie_conformidade.json` gerados localmente;
  - [`attestations/vex_customizado.openvex.json`](../attestations/vex_customizado.openvex.json) e [`policies/openvex_audit.rego`](../policies/openvex_audit.rego) completos sem `TODO`s;
  - Chave privada `cosign.key` removida.
- **🔴 Trilha 3:**
  - Repositório público no GitHub com os `TODO`s resolvidos em [`.github/workflows/golden_pipeline_capstone.yml`](../.github/workflows/golden_pipeline_capstone.yml) (`id-token: write` + SHA-1 em `setup-node`), [`attestations/vex_customizado.openvex.json`](../attestations/vex_customizado.openvex.json) e [`policies/openvex_audit.rego`](../policies/openvex_audit.rego);
  - Link/log da **1ª run bloqueada** (`GPL-3.0`) + commit de remediação + link da **2ª run verde** com Artifacts;
  - Pacote público no GHCR + saída do `cosign verify` / `verify-attestation` e Log Index do Rekor;
  - Relatório preenchido ([`docs/trilha_3/TEMPLATE_ENTREGA_TRILHA_3.md`](./trilha_3/TEMPLATE_ENTREGA_TRILHA_3.md)).
