# Módulo de Políticas Rego v1 — Policy as Code (Conftest)

Este diretório reúne as políticas declarativas em **Rego v1 (`import rego.v1`)** usadas em todas as trilhas do Projeto Final — tanto em design estático (**Trilha 1**) quanto em enforcement via **Conftest** (**Trilhas 2 e 3**).

## Arquivos Disponíveis

1. **`dockerfile.rego`**:
   - Proíbe tags mutáveis (`:latest`) no `FROM`.
   - Proíbe execução como `USER root` e exige uma instrução `USER` explícita.
2. **`sbom_license.rego`**:
   - Exige formato CycloneDX válido.
   - Bloqueia componentes com licenças copyleft restritivas (`GPL-3.0`, `AGPL-3.0`).
3. **`slsa_provenance.rego`**:
   - Valida se a proveniência SLSA v1.0 foi gerada por um Builder oficial autorizado (`runDetails.builder.id`).
   - Exige que o build tenha partido da branch oficial (`refs/heads/main`).
4. **`openvex_audit.rego`** *(Esqueleto Guiado — Desafio Prático)*:
   - Regra 1 (pronta): exige `@context == "https://openvex.dev/ns/v0.2.0"`.
   - Regra 2 (`TODO`): exigir que `statements` não esteja vazio.
   - Regra 3 (`TODO`): exigir `justification` válida (e sem `TODO`) em todo statement `not_affected`.

## Exemplos de Execução com Conftest

```bash
# 1. Testar Dockerfile inseguro (deve FALHAR / BLOQUEAR)
conftest test docker/Dockerfile.inseguro -p policies/dockerfile.rego

# 2. Testar Dockerfile blindado (deve PASSAR)
conftest test docker/Dockerfile.app -p policies/dockerfile.rego

# 3. Testar SBOM de referencia com gpl-math-lib (deve FALHAR / BLOQUEAR)
conftest test attestations/sbom_referencia.cdx.json -p policies/sbom_license.rego

# 4. Testar Proveniencia SLSA v1.0 (deve PASSAR)
conftest test attestations/slsa_predicate.json -p policies/slsa_provenance.rego

# 5. Testar Laudo OpenVEX customizado apos completar o TODO (deve PASSAR)
conftest test attestations/vex_customizado.openvex.json -p policies/openvex_audit.rego
```
