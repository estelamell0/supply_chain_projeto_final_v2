# Relatório de Auditoria & Arquitetura — Projeto Final Capstone (Trilha 1)

**Nome do Aluno(a):** [Seu Nome Completo]  
**Turma:** Supply Chain Security (Turma 1746)  
**Trilha Escolhida:** Trilha 1 — Análise, Auditoria Estática & Design *(Tempo-alvo: ~95 min | Teto: 2h)*  
**Data:** [DD/MM/AAAA]

---

> 💡 **Como preencher:** Seja objetivo e técnico. Na **Etapa 1**, o **Elo 1 (Source)** já vem preenchido como modelo de concisão (1–2 linhas por célula). Preencha todos os campos `[...]` e atualize os arquivos solicitados (`Dockerfile.hardened`, `vex_customizado.openvex.json` e `openvex_audit.rego`).

---

## Etapa 1: Matriz de Riscos (6 Elos) & Dependências — *Aulas 01 & 02* (`2,0 pts`)

### 1.1 Matriz dos 6 Elos na `payment-api`
| Elo da Cadeia | Ameaça Principal no Projeto | Controle no Repositório / Recomendado | Framework (SLSA v1.0 / NIST SSDF) |
| :--- | :--- | :--- | :--- |
| **1. Source** *(Modelo)* | Commits sem revisão ou *force push* na `main` permitem injeção silenciosa de código. | *Branch Protection* + PR aprovado + commits assinados (GPG/SSH). | NIST SSDF **PS.1** e **PO.5** |
| **2. Dependencies** | [...] | [...] | [...] |
| **3. Build (CI/CD)** | [...] | [...] | [...] |
| **4. Artifacts (OCI)** | [...] | [...] | [...] |
| **5. Distribution (Registry)** | [...] | [...] | [...] |
| **6. Runtime / Compliance** | [...] | [...] | [...] |

### 1.2 Auditoria Rápida de Dependências (`src/.npmrc`, `package.json`, `package-lock.json`)
- **Por que `src/.npmrc` + `npm install --ignore-scripts` bloqueiam *Dependency Confusion* e ataques *postinstall*?** [...]
- **Qual o risco de `express` usar intervalo `^4.18.2` no `package.json` vs. integridade no `package-lock.json`?** [...]

---

## Etapa 2: SBOM & Triagem OpenVEX — *Aulas 03 & 04* (`2,0 pts`)

### 2.1 Análise de [`attestations/sbom_referencia.cdx.json`](../../attestations/sbom_referencia.cdx.json)
- **PURLs identificados e função do PURL na correlação de CVEs:** [...]
- **Pacote que viola política de licença (`GPL-3.0`) e ação corretiva proposta:** [...]

### 2.2 Declaração OpenVEX Redigida ([`attestations/vex_customizado.openvex.json`](../../attestations/vex_customizado.openvex.json))
- **Status de entrega:** `[ ] Preenchido o 3º statement (CVE-2024-29041) substituindo os marcadores TODO por justification oficial OpenVEX v0.2.0 e impact_statement técnico`
- **Justificativa oficial escolhida e resumo em 2 linhas do porquê não afeta a `payment-api`:** [...]

---

## Etapa 3: Hardening, Auditoria CI/CD & Sigstore — *Aulas 05 & 06* (`2,5 pts`)

### 3.1 Hardening Estático (`docker/Dockerfile.hardened`)
| Item Auditado | O Que Encontrei no `Dockerfile.inseguro` | Correção Aplicada no `Dockerfile.hardened` |
| :--- | :--- | :--- |
| **Imagem Base (`FROM`)** | [...] | [...] |
| **Instalação (`npm`) & Privilégio (`USER`)** | [...] | [...] |

- **Arquivo entregue:** `docker/Dockerfile.hardened` *(marque após criar: `[ ] Criado com @sha256: e USER node`)*

### 3.2 Auditoria Objetiva de CI/CD (`pipeline_vulneravel.yml` vs. `golden_pipeline_capstone.yml`)
1. **Risco de `permissions: write-all` vs. papel de `contents: read`, `packages: write` e `id-token: write`:** [...]
2. **Diferença de segurança entre `@v4` vs. Commit SHA-1 de 40 caracteres (e efeito de um SHA inválido):** [...]
3. **Papéis do Fulcio (certificado efêmero) e Rekor (Árvore de Merkle) vistos em `keyless_bundle_sample.json`:** [...]

---

## Etapa 4: Policy as Code (Rego v1) & Fechamento — *Aulas 07 & 08* (`3,5 pts`)

1. **Por que `deny contains msg if { ... }` em `import rego.v1` é superior a um simples `allow := false`?** [...]
2. **Arquivo entregue:** [`policies/openvex_audit.rego`](../../policies/openvex_audit.rego) *(marque após completar as Regras 2 e 3: `[ ] Regras 2 e 3 implementadas sem TODOs`)*

> 💡 **Conferência Opcional (Recomendada):** Caso queira verificar automaticamente se todos os arquivos obrigatórios foram criados e se não restou nenhuma lacuna `[...]`, execute `python3 tools/selfcheck_capstone.py --trilha 1` (não é obrigatório colar a saída neste relatório).
