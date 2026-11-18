# Como Sua Entrega Será Avaliada (Nota Máxima: 10,0)

Todas as três trilhas valem **10,0 pontos** e cobrem os **mesmos 8 módulos do curso (Aulas 01 a 08)**, só mudando o nível de ferramenta usada (análise no código, terminal Docker local ou esteira automática na nuvem).

---

## Resumo dos Pesos (Total = 10,0 Pontos)

| O Que Avaliamos | Aulas | Peso | Em Resumo |
| :--- | :---: | :---: | :--- |
| **1. Cuidados com Dependências, Build & Conceitos** | **01, 02** | **2,0** | Entender riscos da cadeia, isolar pacotes privados (`.npmrc`), travar scripts (`--ignore-scripts`) e lidar com a biblioteca `GPL-3.0`. |
| **2. Lista de Componentes (SBOM) & Triagem (OpenVEX)** | **03, 04** | **2,0** | Ler ou gerar o SBOM, analisar vulnerabilidades e preencher o laudo `vex_customizado.openvex.json`. |
| **3. Assinatura Digital & Segurança da Esteira (CI/CD)** | **05, 06** | **2,5** | Deixar Dockerfile e Workflow seguros (menor permissão, hashes fixos) e assinar/verificar imagens com Cosign. |
| **4. Regras Automáticas de Bloqueio (Rego v1)** | **07** | **2,0** | Completar regras no arquivo `policies/openvex_audit.rego` e/ou provar o bloqueio e a aprovação com Conftest. |
| **5. Relatório Final & Dossiê** | **08** | **1,5** | Entregar o template bem preenchido com as provas pedidas e o dossiê/artifacts da trilha. |

---

## Detalhes por Trilha

### 🔵 Trilha 1 — Leitura, Auditoria e Código (10,0 pts)
1. **Matriz dos 6 Elos & Dependências (`2,0 pts`):** Preencher a tabela dos elos 2 a 6 e explicar `.npmrc`, `--ignore-scripts` e o risco do `^4.18.2`.
2. **SBOM & OpenVEX (`2,0 pts`):** Listar os PURLs e o pacote `GPL-3.0` do SBOM de exemplo + completar o 3º item (`CVE-2024-29041`) em `attestations/vex_customizado.openvex.json` sem deixar `TODO`.
3. **`Dockerfile.hardened`, CI/CD & Sigstore (`2,5 pts`):** Criar `docker/Dockerfile.hardened` com endereço `@sha256:` fixo e `USER node` + responder às 3 perguntas de CI/CD e Fulcio/Rekor.
4. **Regras em Rego v1 (`2,0 pts`):** Completar as Regras 2 e 3 em `policies/openvex_audit.rego` com sintaxe válida + explicar por que usar `deny contains`.
5. **Relatório Completo (`1,5 pt`):** `TEMPLATE_ENTREGA_TRILHA_1.md` (ou `.docx`) todo preenchido sem `[...]` e entrega organizada dos 3 arquivos criados *(o `selfcheck` é opcional nesta trilha)*.

### 🟡 Trilha 2 — Comandos no Docker Local (10,0 pts)
1. **Sandbox, Build & SBOM (`2,0 pts`):** Instalar dependências com `--ignore-scripts`, enviar imagem para `localhost:5000`, pegar o `$IMAGE_DIGEST` e gerar `dist/sbom.cdx.json` com `syft`.
2. **Scan & OpenVEX (`2,0 pts`):** Rodar `trivy` e preencher o `TODO` em `attestations/vex_customizado.openvex.json`.
3. **Cosign & Ataque Simulado (`2,5 pts`):** Assinar pelo digest, mostrar o bloqueio ao trocar a imagem por `busybox` (`Error: no signatures found`), restaurar e anexar SBOM + OpenVEX.
4. **Conftest (`2,0 pts`):** Completar regra(s) em `policies/openvex_audit.rego` e mostrar logs reais de `FAIL` (erros propositais) e `PASS` (tudo certo).
5. **Dossiê, Bloco Express & Validação (`1,5 pt`):** Gerar `dist/dossie_conformidade.json`, apagar `cosign.key`, rodar `selfcheck --trilha 2` sem erros e responder ao Bloco Express *(dispensado se marcou `Modo Incremental`)*.

### 🔴 Trilha 3 — Esteira na Nuvem & Keyless (10,0 pts)
1. **Ajuste da Esteira & Remoção da `GPL-3.0` (`2,0 pts`):** Resolver os 2 `TODO`s no `golden_pipeline_capstone.yml`, registrar a 1ª execução bloqueada e remover a `gpl-math-lib` nos 3 locais.
2. **SBOM & OpenVEX na Nuvem (`2,0 pts`):** Completar `attestations/vex_customizado.openvex.json` sem `TODO` e comprovar a publicação do SBOM e atestação OpenVEX no GHCR.
3. **Assinatura Keyless Pública (`2,5 pts`):** Execução **verde** no GitHub Actions + pacote público no GHCR + saída de `cosign verify` / `verify-attestation` (via Codespaces ou CLI) + registro no Rekor.
4. **Portão de Políticas Rego v1 (`2,0 pts`):** Completar regra(s) em `policies/openvex_audit.rego` e comprovar o bloqueio da `GPL-3.0` na 1ª execução.
5. **Artifacts, Bloco Express & Validação (`1,5 pt`):** Baixar o pacote `supply-chain-evidence-bundle`, rodar `selfcheck --trilha 3` sem erros e responder ao Bloco Express *(dispensado se marcou `Modo Incremental`)*.
