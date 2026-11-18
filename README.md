# Projeto Final: Protegendo a Entrega do Microsserviço `payment-api`

**Disciplina:** Segurança na Cadeia de Suprimentos de Software (Ada Tech)  
**Nota Máxima:** `10,0` em qualquer uma das 3 Trilhas  
**Tempo Estimado:** **~95 a 100 min** *(no máximo **2h00** por trilha)*  
**O Que Vamos Proteger:** Uma API simples em Node.js chamada `payment-api`

---

## 1. Como Este Projeto Funciona (Em Poucas Palavras)

Tudo o que você precisa já está pronto dentro desta pasta: código, arquivos de exemplo, regras de segurança e guias.

1. **Todas as trilhas ensinam os mesmos 8 assuntos (Aulas 01 a 08):** Você só precisa escolher **1 Trilha** para fazer. Não importa qual escolher, você vai passar por todos os temas do curso.
2. **O que muda entre as trilhas é só a ferramenta usada:**
   - **Trilha 1:** Você lê os arquivos e escreve as correções no editor de texto (**sem Docker e sem nuvem**).
   - **Trilha 2:** Você roda as ferramentas de segurança no seu computador usando **Docker**.
   - **Trilha 3:** Você coloca tudo para rodar automaticamente na nuvem usando o **GitHub Actions**.
3. **Quer fazer mais de uma trilha?** Pode começar na 1, depois ir para a 2 e para a 3 marcando **`[x] Modo Incremental`** no topo do arquivo de entrega das Trilhas 2 e 3. Assim você reaproveita o que já fez e pula perguntas repetidas.

> 👉 **Por onde começar:** Abra [`docs/README.md`](./docs/README.md) para ver o passo a passo geral.

---

## 2. Escolha sua Trilha

| Trilha | O Que Você Vai Usar | O Que Precisa no Seu PC | Pasta da Trilha | Links Diretos |
| :--- | :--- | :--- | :--- | :--- |
| **🔵 Trilha 1: Leitura, Auditoria e Código** | Só seu editor de texto (VS Code, etc.) para analisar arquivos e escrever regras. | **Nada pesado** (sem Docker e sem nuvem). | [`docs/trilha_1/`](./docs/trilha_1/) | [`Manual`](./docs/trilha_1/MANUAL_TRILHA_1.md) • [`Template MD`](./docs/trilha_1/TEMPLATE_ENTREGA_TRILHA_1.md) • [`Template Word`](./docs/trilha_1/TEMPLATE_ENTREGA_TRILHA_1.docx) |
| **🟡 Trilha 2: Comandos no Terminal (Docker)** | Ferramentas locais no terminal (`syft`, `trivy`, `cosign`, `conftest`). | **Docker** instalado e rodando. | [`docs/trilha_2/`](./docs/trilha_2/) | [`Manual`](./docs/trilha_2/MANUAL_TRILHA_2.md) • [`Template MD`](./docs/trilha_2/TEMPLATE_ENTREGA_TRILHA_2.md) |
| **🔴 Trilha 3: Automação na Nuvem (GitHub)** | Esteira automática no GitHub Actions, publicação no GHCR e assinatura sem senha/chave fixa. | **Conta gratuita no GitHub** (sem Docker no PC). | [`docs/trilha_3/`](./docs/trilha_3/) | [`Manual`](./docs/trilha_3/MANUAL_TRILHA_3.md) • [`Template MD`](./docs/trilha_3/TEMPLATE_ENTREGA_TRILHA_3.md) |

---

## 3. O Que Tem em Cada Pasta do Projeto

- [`README.md`](./README.md) — Esta página inicial.
- [`docs/`](./docs/) — Todos os manuais, guias fáceis, glossário, notas e templates de entrega:
  - [`docs/README.md`](./docs/README.md) — Índice geral com o resumo do que entregar.
  - [`docs/GLOSSARIO_SUPPLY_CHAIN.md`](./docs/GLOSSARIO_SUPPLY_CHAIN.md) — Explicação simples de todas as siglas e termos técnicos.
  - [`docs/COMO_LER_OS_ARTEFATOS.md`](./docs/COMO_LER_OS_ARTEFATOS.md) — Mostra exatamente onde olhar dentro dos arquivos JSON e Rego.
  - [`docs/RUBRICA_AVALIACAO.md`](./docs/RUBRICA_AVALIACAO.md) — Como sua entrega será pontuada (0 a 10,0).
  - [`docs/CHECKLIST_ENTREGA.md`](./docs/CHECKLIST_ENTREGA.md) — Lista de conferência antes de entregar.
  - [`docs/README_POLITICAS.md`](./docs/README_POLITICAS.md) — Explicação das regras automáticas de bloqueio.
  - [`docs/trilha_1/`](./docs/trilha_1/), [`docs/trilha_2/`](./docs/trilha_2/), [`docs/trilha_3/`](./docs/trilha_3/) — Manuais detalhados e templates de cada trilha.
- [`src/`](./src/) — O código da aplicação `payment-api` ([`app.js`](./src/app.js), [`package.json`](./src/package.json), [`package-lock.json`](./src/package-lock.json), [`.npmrc`](./src/.npmrc) e bibliotecas em [`node_modules/`](./src/node_modules/)).
- [`docker/`](./docker/) — Modelos de container: [`Dockerfile.app`](./docker/Dockerfile.app) (bom) e [`Dockerfile.inseguro`](./docker/Dockerfile.inseguro) (com erros propositais para você encontrar).
- [`.github/workflows/`](./.github/workflows/) — Esteiras do GitHub Actions: [`pipeline_vulneravel.yml`](./.github/workflows/pipeline_vulneravel.yml) (insegura, apenas para comparar) e [`golden_pipeline_capstone.yml`](./.github/workflows/golden_pipeline_capstone.yml) (da Trilha 3, com 2 ajustes guiados).
- [`attestations/`](./attestations/) — Arquivos de exemplo e modelos de segurança: [`sbom_referencia.cdx.json`](./attestations/sbom_referencia.cdx.json), [`vex_template.openvex.json`](./attestations/vex_template.openvex.json), [`vex_customizado.openvex.json`](./attestations/vex_customizado.openvex.json), [`slsa_predicate.json`](./attestations/slsa_predicate.json) e [`keyless_bundle_sample.json`](./attestations/keyless_bundle_sample.json).
- [`policies/`](./policies/) — Regras que barram problemas automaticamente: [`dockerfile.rego`](./policies/dockerfile.rego), [`sbom_license.rego`](./policies/sbom_license.rego), [`slsa_provenance.rego`](./policies/slsa_provenance.rego) e [`openvex_audit.rego`](./policies/openvex_audit.rego).
- [`tools/`](./tools/) — Scripts Python que ajudam você: [`verify_keyless_bundle.py`](./tools/verify_keyless_bundle.py), [`generate_compliance_dossier.py`](./tools/generate_compliance_dossier.py) e [`selfcheck_capstone.py`](./tools/selfcheck_capstone.py).
- [`dist/`](./dist/) — Pasta onde ficam salvos os relatórios gerados automaticamente (como [`dossie_conformidade.json`](./dist/dossie_conformidade.json)).
- Arquivos do ambiente Docker (Trilha 2): [`Dockerfile`](./Dockerfile), [`docker-compose.yml`](./docker-compose.yml), [`setup_capstone.sh`](./setup_capstone.sh), [`clean_capstone.sh`](./clean_capstone.sh), [`.dockerignore`](./.dockerignore) e [`.gitignore`](./.gitignore).

---

## 4. Cuidados Finais Antes de Entregar

1. **Nunca suba `cosign.key` para o GitHub:** se você gerou uma chave na Trilha 2, apague o arquivo `cosign.key` antes de enviar qualquer coisa.
2. **Conferência rápida (script Python):**
   - **Obrigatório** nas Trilhas 2 e 3.
   - **Opcional (apenas recomendado)** na Trilha 1 para checar se não faltou nenhum arquivo ou resposta.
   ```bash
   python3 tools/selfcheck_capstone.py --trilha <1|2|3>
   ```
   *(Se estiver fazendo mais de uma trilha na sequência, adicione `--incremental` no comando.)*
