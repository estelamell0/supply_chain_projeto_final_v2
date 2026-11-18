# Checklist Oficial de Entrega — Projeto Final Capstone (v2)

**Disciplina:** Supply Chain Security & DevSecOps Architecture (Turma 1746)  
**Alvo:** Microsserviço `payment-api`  
**Nota Máxima:** `10,0` em qualquer trilha *(Tempo-alvo: ~95–100 min | Teto: 2h00)*

---

## 📌 Regras Gerais (Todas as Trilhas)
- [ ] Escolha **1 Trilha** (ou avance no **Modo Incremental**, marcando `[x] Modo Incremental` nos templates 2 e 3 para reutilizar artefatos e pular o Bloco Express).
- [ ] **Segurança de Chaves:** Nunca envie `cosign.key` para repositórios públicos no GitHub.
- [ ] **Autoverificação:** Execute `python3 tools/selfcheck_capstone.py --trilha <1|2|3>` (use `--incremental` se aplicável).

---

## 🔄 Transição Fluida ("Aterrissagem Segura")
Se iniciou na **Trilha 2** ou **Trilha 3** e encontrou bloqueios de ambiente perto do prazo, migre com segurança para a **Trilha 1** utilizando `TEMPLATE_ENTREGA_TRILHA_1.md` e entregando os arquivos estáticos abaixo (continua valendo até `10,0`).

---

## 🔵 Trilha 1 — Análise, Auditoria Estática & Design *(~95 min)*
- [ ] [`docs/trilha_1/TEMPLATE_ENTREGA_TRILHA_1.md`](./trilha_1/TEMPLATE_ENTREGA_TRILHA_1.md) preenchido sem lacunas `[...]`.
- [ ] `docker/Dockerfile.hardened` criado (`FROM ...@sha256:` e `USER node`).
- [ ] `attestations/vex_customizado.openvex.json` atualizado sem marcadores `TODO`.
- [ ] `policies/openvex_audit.rego` com as Regras 2 e 3 implementadas em `import rego.v1`.
- [ ] `python3 tools/selfcheck_capstone.py --trilha 1` finalizado sem erros críticos.

---

## 🟡 Trilha 2 — Sandbox CLI Local & Enforcement *(~100 min)*
- [ ] [`docs/trilha_2/TEMPLATE_ENTREGA_TRILHA_2.md`](./trilha_2/TEMPLATE_ENTREGA_TRILHA_2.md) preenchido (com Bloco Express de Aulas 01/05 ou `[x] Modo Incremental`).
- [ ] `dist/sbom.cdx.json` e `dist/dossie_conformidade.json` gerados localmente.
- [ ] `attestations/vex_customizado.openvex.json` e `policies/openvex_audit.rego` completos sem `TODO`s.
- [ ] Evidências reais no template: `$IMAGE_DIGEST`, bloqueio no *tag tampering* (`busybox`), `verify-attestation` e `FAIL` + `PASS` no Conftest.
- [ ] `cosign.key` removida + `python3 tools/selfcheck_capstone.py --trilha 2` sem erros críticos.

---

## 🔴 Trilha 3 — Engenharia de Esteira em Nuvem & Keyless OIDC *(~95 min)*
- [ ] Repositório **público** no GitHub preservando `src/node_modules/@corp/payment-vault`.
- [ ] `TODO`s resolvidos em `golden_pipeline_capstone.yml` (`id-token: write` + SHA-1 em `setup-node`), `vex_customizado.openvex.json` e `policies/openvex_audit.rego`.
- [ ] Link/log da **1ª run bloqueada (`GPL-3.0`)** + commit de remediação + link da **2ª run verde**.
- [ ] Pacote no **GHCR definido como Public** + saída do `cosign verify` e `verify-attestation` (via Codespaces/CLI) + índice no **Rekor**.
- [ ] [`docs/trilha_3/TEMPLATE_ENTREGA_TRILHA_3.md`](./trilha_3/TEMPLATE_ENTREGA_TRILHA_3.md) preenchido (com Bloco Express ou `[x] Modo Incremental`) e validado com `python3 tools/selfcheck_capstone.py --trilha 3`.
