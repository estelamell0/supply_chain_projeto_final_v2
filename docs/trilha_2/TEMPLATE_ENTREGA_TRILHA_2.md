# Relatório de Evidências CLI — Projeto Final Capstone (Trilha 2)

**Nome do Aluno(a):** [Seu Nome Completo]  
**Turma:** Supply Chain Security (Turma 1746)  
**Trilha Escolhida:** Trilha 2 — Sandbox CLI Local & Enforcement *(Tempo-alvo: ~100 min | Teto: 2h)*  
**Data:** [DD/MM/AAAA]

- **Modalidade de Entrega:**
  - `[ ] Trilha Única` *(primeira trilha entregue — responder também ao **Bloco Express** no final)*
  - `[ ] Modo Incremental` *(já entreguei a Trilha 1 — **Bloco Express dispensado**; reutilizando `vex_customizado.openvex.json` e `openvex_audit.rego`)*

---

## 1. Setup, Dependências, Build Imutável & SBOM — *Aulas 02, 03 & 06* (`2,0 pts`)
- **Confirmação de trava de pacotes (`src/.npmrc` + `npm install --ignore-scripts`):** `[ ] Executado dentro do sandbox`
- **Digest SHA-256 capturado (`$IMAGE_DIGEST`):**
  ```text
  [Cole aqui a saída de: echo "Lacre Matemático: $IMAGE_DIGEST"]
  ```
- **Confirmação do SBOM (`dist/sbom.cdx.json` via `syft`):** `[ ] Gerado`

---

## 2. Scan de Vulnerabilidades (`trivy`) & OpenVEX — *Aulas 03 & 04* (`2,0 pts`)
- **Resumo das CVEs `HIGH`/`CRITICAL` encontradas pelo `trivy`:**
  ```text
  [Cole aqui um resumo da saída do comando: trivy image --severity HIGH,CRITICAL localhost:5000/payment-api:v1.0.0]
  ```
- **Laudo atualizado em [`attestations/vex_customizado.openvex.json`](../../attestations/vex_customizado.openvex.json):** `[ ] Sem marcadores TODO`
- **Justificativa OpenVEX resumida (por que a vulnerabilidade triada não afeta a `payment-api`):** [...]

---

## 3. Cosign, Bloqueio de Adulteração & Atestações *in-toto* — *Aula 06* (`2,5 pts`)
- **Log de bloqueio no ataque de *Tag Tampering* (`busybox:latest` -> `Error: no signatures found`):**
  ```text
  [Cole aqui a saída do cosign verify após sobrescrever a tag :v1.0.0]
  ```
- **Atestações *in-toto* seladas (`--type cyclonedx` e `--type openvex`) e verificação decodificada:**
  ```json
  [Cole aqui a saída do cosign verify-attestation --type openvex ... | jq '.payload | @base64d | fromjson']
  ```

---

## 4. Conftest (Rego v1), Dossiê & Self-Check — *Aulas 07 & 08* (`2,0 pts`)
- **Regra concluída em [`policies/openvex_audit.rego`](../../policies/openvex_audit.rego):** `[ ] Pelo menos 2 regras deny ativas testadas`
- **Teste de Bloqueio (`FAIL` esperado — `Dockerfile.inseguro` + `dist/sbom.cdx.json` com `GPL-3.0`):**
  ```text
  [Cole aqui a saída FAIL do conftest test]
  ```
- **Teste Aprovado (`PASS` esperado — `Dockerfile.app`, `slsa_predicate.json` e `vex_customizado.openvex.json`):**
  ```text
  [Cole aqui a saída PASS do conftest test]
  ```
- **Conteúdo do `dist/dossie_conformidade.json` gerado (`generate_compliance_dossier.py`):**
  ```json
  [Cole aqui a saída de: cat dist/dossie_conformidade.json]
  ```
- **Saída do `python3 tools/selfcheck_capstone.py --trilha 2`:**
  ```text
  [Cole aqui o resultado do selfcheck --trilha 2]
  ```

---

## 5. Bloco Express Conceitual — *Aulas 01 & 05* (`1,5 pts`)
*(Dispensado automaticamente caso você marque a opção **Modo Incremental** no cabeçalho acima!)*

1. **Mapeamento de Frameworks:** Cite 2 comandos que você executou nesta trilha (ex.: `syft`, `cosign sign` ou `npm install --ignore-scripts`) e indique qual requisito do **SLSA v1.0** ou **NIST SSDF** cada um atende: [...]
2. **Auditoria de CI/CD (`pipeline_vulneravel.yml`):** Aponte **2 falhas críticas** no arquivo `.github/workflows/pipeline_vulneravel.yml` (ex.: `permissions` e pinning) que precisam ser evitadas ao levar este build local para a nuvem: [...]
