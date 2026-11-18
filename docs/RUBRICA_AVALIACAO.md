# Rubrica Oficial de Avaliação — Projeto Final Capstone (v2 — Nota Máxima: 10,0)

Todas as três trilhas permitem alcançar a **nota máxima 10,0**, têm **teto máximo estimado de 2 horas** e cobrem **todos os módulos das Aulas 01 a 08** em camadas tecnológicas progressivas (*Estático/Código* → *CLI Local* → *Cloud CI/CD Keyless*).

---

## Matriz Geral de Pesos (Total = 10,0 Pontos)

| Dimensão Avaliada | Aulas Cobertas | Peso | O Que É Verificado em Essência |
| :--- | :---: | :---: | :--- |
| **1. Higiene de Dependências, Build & Frameworks** | **01, 02** | **2,0** | Mapeamento SLSA/SSDF, isolamento `.npmrc`, `--ignore-scripts`, tratamento de range semântico e remoção/bloqueio de `GPL-3.0`. |
| **2. SBOM & Triagem OpenVEX** | **03, 04** | **2,0** | Inspeção ou geração de CycloneDX 1.6 (PURLs), scan/correlação de CVEs e redação/atestação de `attestations/vex_customizado.openvex.json`. |
| **3. Integridade Criptográfica & Segurança de CI/CD** | **05, 06** | **2,5** | Hardening de Dockerfile/Workflow (`permissions`, SHA pinning), imutabilidade por `@sha256:`, Cosign (local ou Keyless OIDC Fulcio/Rekor) e *in-toto*. |
| **4. Policy as Code (Rego v1 / Conftest)** | **07** | **2,0** | Implementação das regras `deny contains msg if` em `policies/openvex_audit.rego` e/ou execução comprovando `FAIL` e `PASS`. |
| **5. Dossiê de Evidências, Síntese & Autoverificação** | **08 (+ Bloco Express)** | **1,5** | Organização do template da trilha, dossiê `dossie_conformidade.json` ou artifacts, `selfcheck_capstone.py` limpo e Bloco Express (dispensado no Modo Incremental). |

---

## Critérios Detalhados por Trilha

### 🔵 Trilha 1 — Análise, Auditoria Estática & Design (10,0 pts | Alvo: ~95 min)
| Critério | Pontos | Requisitos para Pontuação Máxima |
| :--- | :---: | :--- |
| **1. Matriz 6 Elos & Auditoria de Dependências** | **2,0** | Matriz dos Elos 2–6 preenchida com precisão contra **SLSA v1.0 / NIST SSDF** + diagnóstico de `.npmrc`, `--ignore-scripts` e risco de `^4.18.2` vs. lockfile. |
| **2. SBOM & Redação OpenVEX (`vex_customizado`)** | **2,0** | Listagem dos PURLs e identificação da `GPL-3.0` em `sbom_referencia.cdx.json` + 3º statement (`CVE-2024-29041`) completo em `attestations/vex_customizado.openvex.json` sem `TODO`s. |
| **3. `Dockerfile.hardened`, CI/CD & Bundle Sigstore** | **2,5** | `docker/Dockerfile.hardened` com digest SHA-256 e `USER node` + respostas precisas aos 3 checks de `pipeline_vulneravel.yml` vs `golden_pipeline_capstone.yml` + papéis do Fulcio/Rekor. |
| **4. Design Rego v1 (`openvex_audit.rego`)** | **2,0** | Implementação das Regras 2 e 3 em `policies/openvex_audit.rego` com sintaxe `import rego.v1` válida + explicação sobre `deny contains` vs `allow := false`. |
| **5. Relatório & Self-Check** | **1,5** | `TEMPLATE_ENTREGA_TRILHA_1.md` completo sem lacunas `[...]` e saída limpa de `python3 tools/selfcheck_capstone.py --trilha 1`. |

---

### 🟡 Trilha 2 — Sandbox CLI Local & Enforcement (10,0 pts | Alvo: ~100 min)
| Critério | Pontos | Requisitos para Pontuação Máxima |
| :--- | :---: | :--- |
| **1. Sandbox, `--ignore-scripts`, Digest & SBOM** | **2,0** | Execução isolada de `npm install --ignore-scripts`, build/push em `localhost:5000`, captura real de `$IMAGE_DIGEST` e geração de `dist/sbom.cdx.json` via `syft`. |
| **2. Scan Trivy & OpenVEX (`vex_customizado`)** | **2,0** | Execução do `trivy image --severity HIGH,CRITICAL` e preenchimento completo de `attestations/vex_customizado.openvex.json` sem `TODO`s. |
| **3. Cosign, Ataque Tag Tampering & In-Toto** | **2,5** | Assinatura por digest, log comprovando bloqueio de `busybox:latest` (`Error: no signatures found`), restauração e selagem das 2 atestações (`cyclonedx`, `openvex`) + `verify-attestation`. |
| **4. Enforcement Conftest (`openvex_audit.rego`)** | **2,0** | Conclusão de regra(s) `TODO` em `policies/openvex_audit.rego` + logs reais de `conftest test` provando `FAIL` (`Dockerfile.inseguro` + `GPL-3.0`) e `PASS` (`Dockerfile.app`, SLSA, OpenVEX). |
| **5. Dossiê, Bloco Express & Self-Check** | **1,5** | `dist/dossie_conformidade.json` gerado + remoção de `cosign.key` + `selfcheck --trilha 2` OK + Bloco Express de Aulas 01/05 preenchido *(dispensado se `[x] Modo Incremental`)*. |

---

### 🔴 Trilha 3 — Engenharia de Esteira em Nuvem & Keyless OIDC (10,0 pts | Alvo: ~95 min)
| Critério | Pontos | Requisitos para Pontuação Máxima |
| :--- | :---: | :--- |
| **1. Hardening do Workflow & Remediação `GPL-3.0`** | **2,0** | Resolução dos `TODO`s (`id-token: write` e SHA-1 de `setup-node`) antes do push + captura da 1ª run bloqueada + remoção limpa da `gpl-math-lib` nos 3 locais. |
| **2. SBOM & Atestação OpenVEX em Nuvem** | **2,0** | Preenchimento de `attestations/vex_customizado.openvex.json` sem `TODO`s + geração automática do SBOM CycloneDX e atestação *in-toto* no GHCR na run verde. |
| **3. Keyless Signing Público (Fulcio + Rekor)** | **2,5** | Run **verde** assinando via OIDC sem chaves estáticas + pacote público no GHCR + saída real de `cosign verify` e `verify-attestation` (via Codespaces/CLI) + índice no Rekor. |
| **4. Quality Gate Conftest em CI/CD (`Rego v1`)** | **2,0** | Conclusão de regra(s) `TODO` em `policies/openvex_audit.rego` validada pelo pipeline + evidência real de bloqueio da licença `GPL-3.0` pelo `sbom_license.rego`. |
| **5. Artifacts, Bloco Express & Self-Check** | **1,5** | Download do `supply-chain-evidence-bundle` + `selfcheck --trilha 3` sem pendências + Bloco Express de Aulas 01/02 preenchido *(dispensado se `[x] Modo Incremental`)*. |
