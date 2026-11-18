# Guia Geral da Documentação (`docs/`)

Esta pasta guarda todas as explicações, manuais e modelos de entrega do Projeto Final (`payment-api`).  
Não importa qual trilha você escolha: todas ensinam os mesmos 8 assuntos do curso, valem até **10,0 pontos** e foram planejadas para durar **até 2 horas** (~95 a 100 min).

---

## 1. O Que Tem Aqui Dentro?

### Documentos Gerais (`docs/`)
- [`GLOSSARIO_SUPPLY_CHAIN.md`](./GLOSSARIO_SUPPLY_CHAIN.md) — **Seu dicionário de bolso:** explica de forma simples todas as siglas e termos técnicos usados no projeto.
- [`COMO_LER_OS_ARTEFATOS.md`](./COMO_LER_OS_ARTEFATOS.md) — Mostra onde olhar dentro dos arquivos JSON (SBOM, OpenVEX, SLSA, Bundle) e das regras Rego.
- [`RUBRICA_AVALIACAO.md`](./RUBRICA_AVALIACAO.md) — Explica quanto vale cada parte da sua entrega (de 0 a 10,0).
- [`CHECKLIST_ENTREGA.md`](./CHECKLIST_ENTREGA.md) — Lista simples para você marcar e ter certeza de que não esqueceu nada.
- [`README_POLITICAS.md`](./README_POLITICAS.md) — Explica o que faz cada regra automática da pasta [`../policies/`](../policies/).

### Pastas das Trilhas
| Trilha | Pasta | Manual Passo a Passo | Modelo de Entrega |
| :--- | :--- | :--- | :--- |
| **🔵 Trilha 1 — Leitura e Código** *(sem Docker, sem nuvem)* | [`trilha_1/`](./trilha_1/) | [`MANUAL_TRILHA_1.md`](./trilha_1/MANUAL_TRILHA_1.md) | [`TEMPLATE_ENTREGA_TRILHA_1.md`](./trilha_1/TEMPLATE_ENTREGA_TRILHA_1.md) • [`Versão Word (.docx)`](./trilha_1/TEMPLATE_ENTREGA_TRILHA_1.docx) |
| **🟡 Trilha 2 — Comandos no Docker** *(roda no seu PC)* | [`trilha_2/`](./trilha_2/) | [`MANUAL_TRILHA_2.md`](./trilha_2/MANUAL_TRILHA_2.md) | [`TEMPLATE_ENTREGA_TRILHA_2.md`](./trilha_2/TEMPLATE_ENTREGA_TRILHA_2.md) |
| **🔴 Trilha 3 — Automação no GitHub** *(roda na nuvem)* | [`trilha_3/`](./trilha_3/) | [`MANUAL_TRILHA_3.md`](./trilha_3/MANUAL_TRILHA_3.md) | [`TEMPLATE_ENTREGA_TRILHA_3.md`](./trilha_3/TEMPLATE_ENTREGA_TRILHA_3.md) |

---

## 2. Regras Simples para Não Ter Erro

1. **Escolha 1 Trilha (ou faça em sequência):**
   - Você só precisa entregar **1 trilha** (`Trilha 1`, `Trilha 2` ou `Trilha 3`).
   - Se quiser fazer outra trilha depois (`1 → 2 → 3`), marque **`[x] Modo Incremental`** no topo do novo modelo de entrega. Isso permite reaproveitar seus arquivos e pular perguntas repetidas.
2. **Plano B sem perda de nota ("Aterrissagem Segura"):**
   - Começou na Trilha 2 ou 3 e o computador/internet travou perto do prazo? Pode mudar para a **Trilha 1** sem perder pontos. Basta preencher o modelo da Trilha 1 e entregar os arquivos estáticos dela.
3. **Cuidado com a chave privada (`cosign.key`):**
   - Nunca envie o arquivo `cosign.key` para um repositório público do GitHub.
4. **Script de conferência (Opcional na Trilha 1 / Obrigatório nas Trilhas 2 e 3):**
   ```bash
   python3 tools/selfcheck_capstone.py --trilha <1|2|3>
   ```
   *(Se estiver usando o Modo Incremental, adicione `--incremental` no final.)*

---

## 3. O Que Você Precisa Entregar em Cada Trilha

- **🔵 Na Trilha 1:**
  1. O relatório preenchido ([`TEMPLATE_ENTREGA_TRILHA_1.md`](./trilha_1/TEMPLATE_ENTREGA_TRILHA_1.md) ou o arquivo Word [`TEMPLATE_ENTREGA_TRILHA_1.docx`](./trilha_1/TEMPLATE_ENTREGA_TRILHA_1.docx));
  2. O arquivo `docker/Dockerfile.hardened` criado por você (com endereço `@sha256:` fixo e `USER node`);
  3. O arquivo [`attestations/vex_customizado.openvex.json`](../attestations/vex_customizado.openvex.json) com o `TODO` resolvido;
  4. O arquivo [`policies/openvex_audit.rego`](../policies/openvex_audit.rego) com as Regras 2 e 3 completas.

- **🟡 Na Trilha 2:**
  1. O relatório preenchido ([`TEMPLATE_ENTREGA_TRILHA_2.md`](./trilha_2/TEMPLATE_ENTREGA_TRILHA_2.md)) com as saídas copiadas do terminal;
  2. Os arquivos `dist/sbom.cdx.json` e `dist/dossie_conformidade.json` gerados pelos comandos;
  3. Os arquivos [`attestations/vex_customizado.openvex.json`](../attestations/vex_customizado.openvex.json) e [`policies/openvex_audit.rego`](../policies/openvex_audit.rego) sem `TODO`s;
  4. Garantir que `cosign.key` foi apagado.

- **🔴 Na Trilha 3:**
  1. Repositório público no GitHub com os `TODO`s resolvidos em [`.github/workflows/golden_pipeline_capstone.yml`](../.github/workflows/golden_pipeline_capstone.yml), [`attestations/vex_customizado.openvex.json`](../attestations/vex_customizado.openvex.json) e [`policies/openvex_audit.rego`](../policies/openvex_audit.rego);
  2. Link e trecho do erro da **1ª execução bloqueada** (por causa da `gpl-math-lib`) + commit da correção + link da **2ª execução verde**;
  3. Pacote público no GHCR + saída da verificação pública (`cosign verify` e `verify-attestation`) + registro no Rekor;
  4. O relatório preenchido ([`TEMPLATE_ENTREGA_TRILHA_3.md`](./trilha_3/TEMPLATE_ENTREGA_TRILHA_3.md)).
