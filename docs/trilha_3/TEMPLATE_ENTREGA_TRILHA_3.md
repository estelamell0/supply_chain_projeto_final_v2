# Relatório de Evidências Cloud-Native — Projeto Final Capstone (Trilha 3)

**Nome do Aluno(a):** [Seu Nome Completo]  
**Turma:** Supply Chain Security (Turma 1746)  
**Trilha Escolhida:** Trilha 3 — Engenharia de Esteira em Nuvem & Keyless OIDC *(Tempo-alvo: ~95 min | Teto: 2h)*  
**Data:** [DD/MM/AAAA]

- **Modalidade de Entrega:**
  - `[ ] Trilha Única` *(primeira trilha entregue — responder também ao **Bloco Express** no final)*
  - `[ ] Modo Incremental` *(já entreguei trilha anterior — **Bloco Express dispensado**; reutilizando `vex_customizado.openvex.json` e `openvex_audit.rego`)*

---

## 1. Links Oficiais da Entrega — *Aula 08* (`1,5 pts`)
- **Repositório Público no GitHub:** `https://github.com/<usuario>/<repositorio>`
- **Run Bloqueada pelo Conftest (`FAIL` intencional da `GPL-3.0`):** `https://github.com/<usuario>/<repositorio>/actions/runs/<id-run-fail>`
- **Run Verde Final (Após Remediação):** `https://github.com/<usuario>/<repositorio>/actions/runs/<id-run-pass>`
- **Pacote Público no GHCR:** `ghcr.io/<usuario>/<repositorio>/payment-api@sha256:<digest>`
- **Registro Público no Rekor (`search.sigstore.dev`):** [Cole aqui o Log Index ou URL da transação no Rekor]

---

## 2. Hardening da Esteira, Rego v1 & Ciclo Red → Green — *Aulas 02, 03, 05 & 07* (`3,5 pts`)
- **Correções aplicadas antes do 1º push:**
  - `[ ] TODO 1 resolvido: id-token: write habilitado em golden_pipeline_capstone.yml`
  - `[ ] TODO 2 resolvido: actions/setup-node fixado por SHA-1 de 40 caracteres`
  - `[ ] policies/openvex_audit.rego e attestations/vex_customizado.openvex.json sem TODOs pendentes`
- **Log do bloqueio inicial da `gpl-math-lib` pelo Conftest na run vermelha:**
  ```text
  [Cole aqui o trecho do log do GitHub Actions mostrando o FAIL do Conftest na licença GPL-3.0]
  ```
- **Commit da remediação (remoção de `gpl-math-lib`):** `<hash-do-commit>`

---

## 3. Verificação Pública Keyless (Fulcio + Rekor) & Atestação OpenVEX — *Aulas 04 & 06* (`3,5 pts`)
- **Comando público executado (via GitHub Codespaces, CLI local ou container):**
  ```bash
  cosign verify --certificate-identity="https://github.com/<usuario>/<repositorio>/.github/workflows/golden_pipeline_capstone.yml@refs/heads/main" --certificate-oidc-issuer="https://token.actions.githubusercontent.com" ghcr.io/<usuario>/<repositorio>/payment-api@sha256:<digest>
  ```
- **Saída real do `cosign verify` e `cosign verify-attestation --type openvex`:**
  ```text
  [Cole aqui a saída confirmando assinatura Keyless OIDC e payload OpenVEX decodificado]
  ```

---

## 4. Artifacts & Self-Check — *Aula 08* (`0,5 pt`)
- **Artifacts baixados da aba Summary da run verde (`supply-chain-evidence-bundle`):**
  - `[ ] dist/sbom.cdx.json`
  - `[ ] dist/dossie_conformidade.json`
  - `[ ] attestations/vex_customizado.openvex.json`
- **Saída do `python3 tools/selfcheck_capstone.py --trilha 3`:**
  ```text
  [Cole aqui o resultado do selfcheck --trilha 3]
  ```

---

## 5. Bloco Express Conceitual — *Aulas 01 & 02* (`1,0 pt`)
*(Dispensado automaticamente caso você marque a opção **Modo Incremental** no cabeçalho acima!)*

1. **SLSA v1.0 / NIST SSDF:** Por que o build executado no GitHub Actions com `id-token: write` e registro no Rekor atende a garantias superiores às de um build manual local? [...]
2. **Proteção contra Dependency Confusion:** Qual a função do arquivo `src/.npmrc` e da flag `npm install --ignore-scripts` executada na esteira? [...]
