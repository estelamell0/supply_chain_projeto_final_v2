# Checklist Final — Conferência Antes de Entregar

Use esta lista para ter certeza de que tudo na sua trilha está completo.

---

## 📌 Regras Gerais
- [ ] Escolhi **1 Trilha** (ou marquei `[x] Modo Incremental` nos templates 2 e 3 caso já tenha feito uma trilha antes).
- [ ] **Segurança:** Conferi que não deixei nenhum arquivo `cosign.key` (chave privada) na pasta raiz antes de enviar para o GitHub.
- [ ] **Conferência automática:** Nas Trilhas 2 e 3, rodei `python3 tools/selfcheck_capstone.py --trilha <2|3>` e não deu erros críticos. *(Na Trilha 1, rodar o script é opcional — recomendado apenas para checar se você não esqueceu nenhum arquivo ou lacuna `[...]`).*

---

## 🔄 Plano B ("Aterrissagem Segura")
Se você começou na **Trilha 2** ou **Trilha 3** e teve algum problema técnico perto do prazo final, pode mudar para a **Trilha 1** sem perder nota. Basta entregar o relatório da Trilha 1 preenchido e os 3 arquivos estáticos abaixo.

---

## 🔵 Trilha 1 — Leitura, Auditoria e Código
- [ ] [`docs/trilha_1/TEMPLATE_ENTREGA_TRILHA_1.md`](./trilha_1/TEMPLATE_ENTREGA_TRILHA_1.md) (ou o Word [`TEMPLATE_ENTREGA_TRILHA_1.docx`](./trilha_1/TEMPLATE_ENTREGA_TRILHA_1.docx)) preenchido sem deixar `[...]` sobrando.
- [ ] `docker/Dockerfile.hardened` criado (com imagem fixa por `@sha256:` e `USER node`).
- [ ] `attestations/vex_customizado.openvex.json` preenchido sem nenhum `TODO`.
- [ ] `policies/openvex_audit.rego` com as Regras 2 e 3 funcionando em `import rego.v1`.
- *(Opcional)* Rodar `python3 tools/selfcheck_capstone.py --trilha 1` só para conferir.

---

## 🟡 Trilha 2 — Comandos no Docker (CLI Local)
- [ ] [`docs/trilha_2/TEMPLATE_ENTREGA_TRILHA_2.md`](./trilha_2/TEMPLATE_ENTREGA_TRILHA_2.md) preenchido (com o Bloco Express no final, ou `[x] Modo Incremental` marcado).
- [ ] `dist/sbom.cdx.json` e `dist/dossie_conformidade.json` gerados dentro do container.
- [ ] `attestations/vex_customizado.openvex.json` e `policies/openvex_audit.rego` completos sem `TODO`s.
- [ ] Provas coladas no relatório: código `$IMAGE_DIGEST`, erro de bloqueio ao trocar a imagem por `busybox`, verificação da atestação, bloqueio (`FAIL`) + aprovação (`PASS`) no Conftest.
- [ ] `cosign.key` apagado (`rm -f cosign.key`) + `python3 tools/selfcheck_capstone.py --trilha 2` sem erros.

---

## 🔴 Trilha 3 — Automação no GitHub & Keyless
- [ ] Repositório **público** no GitHub com a pasta `src/node_modules/` incluída no envio.
- [ ] `TODO`s resolvidos em `.github/workflows/golden_pipeline_capstone.yml` (`id-token: write` e SHA-1 no `setup-node`), `vex_customizado.openvex.json` e `policies/openvex_audit.rego`.
- [ ] Link/trecho do log da **1ª execução bloqueada** (`GPL-3.0`) + commit removendo `gpl-math-lib` + link da **2ª execução verde**.
- [ ] Pacote `payment-api` no **GHCR mudado para Public** + saída do `cosign verify` e `verify-attestation` + número/link do **Rekor**.
- [ ] [`docs/trilha_3/TEMPLATE_ENTREGA_TRILHA_3.md`](./trilha_3/TEMPLATE_ENTREGA_TRILHA_3.md) preenchido e validado com `python3 tools/selfcheck_capstone.py --trilha 3`.
