# Como Ler os Arquivos de Segurança do Projeto

Não sabe onde olhar dentro dos arquivos JSON e `.rego` de `attestations/` e `policies/`? Este guia vai direto ao ponto para você achar cada informação rápido.

---

## 1. Lista de Peças do Software: SBOM (`attestations/sbom_referencia.cdx.json`)
Pense no **SBOM** como a "tabela nutricional" do seu sistema: ele lista tudo o que vai dentro do container.

1. **`metadata.component`**: Mostra o nome da imagem principal (`localhost:5000/payment-api`).
2. **`components[]`**: É a lista de todas as bibliotecas instaladas. Dentro de cada item, olhe 3 coisas:
   - **`name` e `version`**: Nome e versão da biblioteca (ex.: `express` `4.18.2`).
   - **`purl`**: É o "CPF único" do pacote (ex.: `pkg:npm/express@4.18.2` ou `pkg:npm/gpl-math-lib@1.0.0`). É por esse código que os scanners procuram falhas de segurança sem confundir pacotes parecidos.
   - **`licenses[].license.id`**: Mostra a licença de uso (ex.: `MIT`, `Proprietary`, `GPL-3.0`). **É aqui que você vê que a `gpl-math-lib` usa `GPL-3.0`, que é proibida neste projeto.**

---

## 2. Justificativa de Falhas: OpenVEX (`attestations/vex_template.openvex.json` e `vex_customizado.openvex.json`)
Scanners às vezes apontam uma falha (CVE) em uma biblioteca, mas a nossa aplicação nem usa aquela parte do código. O **OpenVEX** serve para registrar formalmente essa explicação para os auditores:
- **`@context`**: Sempre precisa ser `"https://openvex.dev/ns/v0.2.0"` (indica a versão oficial do padrão).
- **`statements[]`**: Cada item da lista fala sobre uma falha (`vulnerability.name`, como `CVE-2024-29041`) e traz:
  - **`status`**: Diz se afeta ou não. Quando não afeta, usamos `"not_affected"`.
  - **`justification`** *(obrigatório quando for `"not_affected"`)*: Motivo padronizado em inglês. Os valores oficiais mais usados são:
    - `component_not_present` (o componente nem está lá);
    - `vulnerable_code_not_present` (o trecho falho não foi incluído);
    - `vulnerable_code_not_in_execute_path` (o código existe, mas o app nunca chama essa função);
    - `vulnerable_code_cannot_be_controlled_by_adversary` (o usuário não consegue controlar a entrada);
    - `inline_mitigations_already_exist` (já existe outra trava no código que impede o ataque).
  - **`impact_statement`**: Frase em português explicando com suas palavras por que a `payment-api` está segura.

---

## 3. Certidão de Nascimento do Build: SLSA (`attestations/slsa_predicate.json`)
Prova **quem** construiu o sistema e **de onde** veio o código:
- **`buildDefinition.externalParameters.workflow.ref`**: Mostra qual branch do Git disparou a construção (ex.: `"refs/heads/main"`).
- **`runDetails.builder.id`**: Mostra o endereço oficial do robô que fez o build (ex.: `"https://github.com/actions/runner/slsa-builder-l2"`). Se alguém compilasse no notebook pessoal, esse endereço seria diferente e seria bloqueado.

---

## 4. Comprovante da Assinatura Sem Chave Fixa (`attestations/keyless_bundle_sample.json`)
Se você rodar `python3 tools/verify_keyless_bundle.py`, ele lê esse arquivo e mostra duas provas juntas:
1. **Certificado Fulcio (dura só ~10 minutos):** Prova qual repositório e arquivo YAML do GitHub pediu a assinatura.
2. **Registro Rekor (Log Index `#12984920`):** Um carimbo público imutável provando a data e hora exata em que a assinatura foi feita (enquanto aqueles 10 minutos ainda valiam).

---

## 5. Regras Automáticas de Bloqueio (`policies/*.rego`)
As regras são escritas em **Rego v1** (`import rego.v1`) e rodam com o programa **Conftest**:
- Todo bloco **`deny contains msg if { ... }`** funciona como uma lista de verificações: se **todas** as linhas dentro das chaves `{ ... }` forem verdadeiras para um erro, a regra dispara a mensagem `msg` e **trava** a esteira (`FAIL`).
  - `policies/dockerfile.rego`: Barra imagem `:latest` e container rodando como `USER root`.
  - `policies/sbom_license.rego`: Barra qualquer pacote com licença `GPL-3.0` ou `AGPL-3.0`.
  - `policies/slsa_provenance.rego`: Só aceita builds feitos pelo robô oficial na branch `main`.
  - `policies/openvex_audit.rego`: Arquivo com espaço guiado (`TODO`) para você completar e barrar laudos OpenVEX vazios ou sem justificativa.
