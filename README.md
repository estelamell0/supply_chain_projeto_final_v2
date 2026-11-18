# Projeto Final (Capstone v2): Esteira Blindada & Governança de Supply Chain

**Disciplina:** Supply Chain Security & DevSecOps Architecture (Ada Tech)  
**Nota Máxima:** `10,0` em qualquer uma das 3 Trilhas  
**Tempo Estimado:** **~95 a 100 min** *(Teto máximo: **2h00** por trilha)*  
**Alvo do Projeto:** Microsserviço financeiro `payment-api` (Node.js + Docker + Sigstore + Policy as Code)

---

## 1. Visão Geral & Modelo Pedagógico

Este repositório é **100% autocontido**:
1. **Equivalência Conceitual Completa (Aulas 01 a 08):** Todas as 3 trilhas cobrem **todos os 8 módulos do curso** de forma independente. Escolha **apenas 1 Trilha** (ou evolua incrementalmente).
2. **Progressão Tecnológica Incremental (`Trilha 1 → 2 → 3`):** A dificuldade evolui na **camada tecnológica** (*Estática/Código* → *CLI Local* → *Cloud CI/CD + Keyless OIDC*). Quem avançar entre trilhas pode marcar **`[x] Modo Incremental`** nos templates das Trilhas 2 e 3 para reutilizar artefatos já criados.

> 👉 **Comece por aqui:** Leia o índice geral da documentação em [`docs/README.md`](./docs/README.md).

---

## 2. Escolha sua Trilha

| Trilha | Camada Tecnológica | Pré-requisito de Ambiente | Pasta da Trilha | Roteiro & Template |
| :--- | :--- | :--- | :--- | :--- |
| **🔵 Trilha 1: Análise, Auditoria & Design** | Revisão de manifestos, matriz SLSA/SSDF, redação OpenVEX e regras Rego v1. | **Mínimo** (Editor/IDE; zero Docker ou nuvem). | [`docs/trilha_1/`](./docs/trilha_1/) | [`Roteiro`](./docs/trilha_1/TRILHA_1_ANALISE_ARQUITETURA.md) • [`Template MD`](./docs/trilha_1/TEMPLATE_ENTREGA_TRILHA_1.md) • [`Template Word (.docx)`](./docs/trilha_1/TEMPLATE_ENTREGA_TRILHA_1.docx) |
| **🟡 Trilha 2: Sandbox CLI Local** | `npm --ignore-scripts`, Registry local, `syft`, `trivy`, `cosign` (tampering + *in-toto*), `conftest` e dossiê. | **Local** (Docker + Compose; pré-build recomendado). | [`docs/trilha_2/`](./docs/trilha_2/) | [`Roteiro`](./docs/trilha_2/TRILHA_2_EXECUCAO_LOCAL_CLI.md) • [`Template MD`](./docs/trilha_2/TEMPLATE_ENTREGA_TRILHA_2.md) |
| **🔴 Trilha 3: Esteira em Nuvem (Keyless)** | Correção de `TODO`s no Actions, ciclo Red→Green (`GPL-3.0`), GHCR público e verificação **Keyless OIDC**. | **Cloud** (GitHub público + Codespaces; zero Docker local). | [`docs/trilha_3/`](./docs/trilha_3/) | [`Roteiro`](./docs/trilha_3/TRILHA_3_CICD_NUVEM_KEYLESS.md) • [`Template MD`](./docs/trilha_3/TEMPLATE_ENTREGA_TRILHA_3.md) |

---

## 3. Mapa de Pastas e Arquivos do Projeto

- [`README.md`](./README.md) — Este guia inicial na raiz.
- [`docs/`](./docs/) — Toda a documentação, guias, rubrica, checklists e templates:
  - [`docs/README.md`](./docs/README.md) — Índice e instruções gerais do projeto.
  - [`docs/RUBRICA_AVALIACAO.md`](./docs/RUBRICA_AVALIACAO.md) — Critérios de avaliação (0 a 10,0).
  - [`docs/CHECKLIST_ENTREGA.md`](./docs/CHECKLIST_ENTREGA.md) — Checklist final por trilha.
  - [`docs/COMO_LER_OS_ARTEFATOS.md`](./docs/COMO_LER_OS_ARTEFATOS.md) — Como inspecionar SBOM, OpenVEX, SLSA, Bundle e Rego.
  - [`docs/README_POLITICAS.md`](./docs/README_POLITICAS.md) — Guia das políticas Rego v1.
  - [`docs/trilha_1/`](./docs/trilha_1/), [`docs/trilha_2/`](./docs/trilha_2/), [`docs/trilha_3/`](./docs/trilha_3/) — Roteiros e templates específicos de cada trilha.
- [`src/`](./src/) — Microsserviço `payment-api` ([`app.js`](./src/app.js), [`package.json`](./src/package.json), [`package-lock.json`](./src/package-lock.json), [`.npmrc`](./src/.npmrc) e mocks em [`node_modules/`](./src/node_modules/)).
- [`docker/`](./docker/) — [`Dockerfile.app`](./docker/Dockerfile.app) (base endurecida) e [`Dockerfile.inseguro`](./docker/Dockerfile.inseguro) (alvo de auditoria/FAIL).
- [`.github/workflows/`](./.github/workflows/) — [`pipeline_vulneravel.yml`](./.github/workflows/pipeline_vulneravel.yml) (referência insegura) e [`golden_pipeline_capstone.yml`](./.github/workflows/golden_pipeline_capstone.yml) (esteira da Trilha 3 com 2 `TODO`s guiados).
- [`attestations/`](./attestations/) — [`sbom_referencia.cdx.json`](./attestations/sbom_referencia.cdx.json), [`vex_template.openvex.json`](./attestations/vex_template.openvex.json), [`vex_customizado.openvex.json`](./attestations/vex_customizado.openvex.json), [`slsa_predicate.json`](./attestations/slsa_predicate.json) e [`keyless_bundle_sample.json`](./attestations/keyless_bundle_sample.json).
- [`policies/`](./policies/) — Políticas Rego v1: [`dockerfile.rego`](./policies/dockerfile.rego), [`sbom_license.rego`](./policies/sbom_license.rego), [`slsa_provenance.rego`](./policies/slsa_provenance.rego) e [`openvex_audit.rego`](./policies/openvex_audit.rego).
- [`tools/`](./tools/) — Utilitários Python: [`verify_keyless_bundle.py`](./tools/verify_keyless_bundle.py), [`generate_compliance_dossier.py`](./tools/generate_compliance_dossier.py) e [`selfcheck_capstone.py`](./tools/selfcheck_capstone.py).
- [`dist/`](./dist/) — Diretório de saída para `sbom.cdx.json` e [`dossie_conformidade.json`](./dist/dossie_conformidade.json).
- Ambiente Sandbox (Trilha 2): [`Dockerfile`](./Dockerfile), [`docker-compose.yml`](./docker-compose.yml), [`setup_capstone.sh`](./setup_capstone.sh), [`clean_capstone.sh`](./clean_capstone.sh), [`.dockerignore`](./.dockerignore) e [`.gitignore`](./.gitignore).

---

## 4. O Que Entregar & Autoverificação

Consulte os detalhes do que deve ser entregue por trilha em [`docs/README.md`](./docs/README.md) e [`docs/CHECKLIST_ENTREGA.md`](./docs/CHECKLIST_ENTREGA.md).  
Antes de finalizar sua entrega:
1. Nunca deixe chaves privadas reais (`cosign.key`) na pasta raiz.
2. Execute o validador automático:
   ```bash
   python3 tools/selfcheck_capstone.py --trilha <1|2|3>
   ```
   *(Adicione `--incremental` caso esteja usando o Modo Incremental.)*
