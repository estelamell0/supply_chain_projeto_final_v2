# Guia das Políticas Automáticas (`policies/`)

Esta pasta guarda os arquivos `.rego` (linguagem **Rego v1**), lidos pelo programa **Conftest** para aprovar (`PASS`) ou bloquear (`FAIL`) arquivos do projeto automaticamente.

## O Que Cada Arquivo Verifica

1. **`policies/dockerfile.rego`** *(já pronta)*:
   - Barra se o `Dockerfile` usar a tag genérica `:latest`.
   - Barra se o container rodar como administrador (`USER root`) ou sem usuário definido.
2. **`policies/sbom_license.rego`** *(já pronta)*:
   - Confere se o arquivo é um SBOM no padrão CycloneDX.
   - Barra qualquer biblioteca com licença restritiva (`GPL-3.0`, `AGPL-3.0`), como a `gpl-math-lib`.
3. **`policies/slsa_provenance.rego`** *(já pronta)*:
   - Confere se o build veio de um robô oficial permitido e da branch `refs/heads/main`.
4. **`policies/openvex_audit.rego`** *(para você completar)*:
   - **Regra 1 (já pronta como exemplo):** Exige o `@context` oficial do OpenVEX (`https://openvex.dev/ns/v0.2.0`).
   - **Regra 2 (`TODO`):** Você deve completar para bloquear se a lista `statements` estiver vazia.
   - **Regra 3 (`TODO`):** Você deve completar para bloquear se algum item `"not_affected"` estiver sem `justification` (ou ainda com `TODO`).

## Comandos para Testar no Terminal (Trilha 2)

```bash
# Deve FALHAR (mostra os erros propositais)
conftest test docker/Dockerfile.inseguro -p policies/dockerfile.rego
conftest test dist/sbom.cdx.json -p policies/sbom_license.rego

# Deve PASSAR (depois que você completar suas regras)
conftest test docker/Dockerfile.app -p policies/dockerfile.rego
conftest test attestations/slsa_predicate.json -p policies/slsa_provenance.rego
conftest test attestations/vex_customizado.openvex.json -p policies/openvex_audit.rego
```
