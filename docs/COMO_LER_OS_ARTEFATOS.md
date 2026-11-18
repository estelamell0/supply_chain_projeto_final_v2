# Como Ler e Interpretar os Artefatos de Supply Chain Security

Este guia mostra exatamente **onde olhar** dentro dos arquivos JSON e Rego v1 de `attestations/` e `policies/` para responder com precisão às etapas do Capstone (nas Trilhas 1, 2 e 3).

---

## 1. Anatomia do SBOM (`attestations/sbom_referencia.cdx.json`)
Um arquivo **CycloneDX 1.6** possui três blocos principais:
1. **`metadata.component`**: Identifica o artefato-alvo (nossa imagem `localhost:5000/payment-api` e seu digest).
2. **`components[]`**: Lista cada biblioteca ou pacote de SO encontrado. Em cada item, observe:
   - **`name` e `version`**: Nome e versão exata do pacote.
   - **`purl`** (*Package URL*): Identificador universal padronizado (ex.: `pkg:npm/express@4.18.2` ou `pkg:npm/gpl-math-lib@1.0.0`). É o campo usado por scanners como Grype, Trivy e Dependency-Track para cruzar componentes contra bases de CVEs.
   - **`licenses[].license.id`**: Identificador SPDX da licença (ex.: `MIT`, `Proprietary`, `GPL-3.0`). **É aqui que identificamos a violação `gpl-math-lib` (`GPL-3.0`).**

---

## 2. Anatomia do Laudo OpenVEX (`attestations/vex_template.openvex.json` e `vex_customizado.openvex.json`)
O **OpenVEX v0.2.0** documenta decisões formais sobre CVEs para eliminar falsos positivos sem silenciar riscos:
- **`@context`**: Deve apontar para `"https://openvex.dev/ns/v0.2.0"`.
- **`statements[]`**: Cada declaração liga uma vulnerabilidade (`vulnerability.name`, ex.: `CVE-...`) aos produtos afetados (`products[]`) com:
  - **`status`**: `"not_affected"`, `"affected"`, `"fixed"` ou `"under_investigation"`.
  - **`justification`** *(obrigatória quando `status == "not_affected"`)*: Valores oficiais da spec v0.2.0:
    - `component_not_present`
    - `vulnerable_code_not_present`
    - `vulnerable_code_not_in_execute_path` (ou `code_not_reachable` em templates legados)
    - `vulnerable_code_cannot_be_controlled_by_adversary`
    - `inline_mitigations_already_exist`
  - **`impact_statement`**: Explicação humana auditável justificando por que a aplicação não é explorável.

---

## 3. Anatomia da Proveniência SLSA v1.0 (`attestations/slsa_predicate.json`)
A "certidão de nascimento" do build possui dois blocos essenciais:
- **`buildDefinition.externalParameters.workflow`**:
  - **`ref`**: Branch/tag que disparou o build (ex.: `"refs/heads/main"`).
  - **`repository`** e **`path`**: Repositório e arquivo YAML do workflow oficial.
- **`runDetails.builder.id`**: Identidade do construtor autorizado (ex.: `"https://github.com/actions/runner/slsa-builder-l2"`). Se o build fosse feito em laptop pessoal, este campo não bateria com a allowlist.

---

## 4. Anatomia do Bundle Keyless Sigstore (`attestations/keyless_bundle_sample.json`)
Ao rodar `python3 tools/verify_keyless_bundle.py attestations/keyless_bundle_sample.json`, você disseca as duas metades da prova sem chave estática:
1. **Certificado Fulcio (X.509 efêmero ~10 min):** Traz extensões OIDC provando qual **Subject Alternative Name (SAN)** (repositório + workflow + branch) e qual **Issuer** (`https://token.actions.githubusercontent.com`) solicitaram a assinatura.
2. **Rekor SET (*Signed Entry Timestamp*):** Prova criptográfica de inclusão na árvore de Merkle pública do Rekor, garantindo que a assinatura foi criada **durante os 10 minutos** em que o certificado efêmero era válido.

---

## 5. Como Ler e Escrever Políticas Rego v1 (`policies/*.rego`)
- **`import rego.v1`**: Ativa a sintaxe moderna exigindo `contains` e `if` explícitos.
- **`deny contains msg if { ... }`**: Todas as linhas dentro das chaves funcionam como **AND lógico**. Se todas forem verdadeiras para algum elemento de `input`, a mensagem `msg` é emitida e o Conftest retorna `FAIL` (`exit code 1`).
  - `policies/dockerfile.rego`: Converte o Dockerfile em array de instruções (`step.Cmd`, `step.Value[0]`).
  - `policies/sbom_license.rego`: Itera em `input.components` e cruza `lic_id in forbidden_licenses`.
  - `policies/slsa_provenance.rego`: Usa `object.get(input, "predicate", input)` para funcionar tanto no JSON bruto quanto dentro de um envelope *in-toto*.
  - `policies/openvex_audit.rego`: Esqueleto guiado para você validar `@context`, `statements` não vazio e `justification` obrigatória em `not_affected`.
