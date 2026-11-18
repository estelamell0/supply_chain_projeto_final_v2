# Glossário Simples — Supply Chain Security & Termos Adjacentes

Um guia de bolso escrito em linguagem simples e direta para você consultar sempre que encontrar uma sigla ou termo técnico diferente durante as **Trilhas 1, 2 e 3**.

---

## Índice Rápido
1. [Siglas e Abreviações de Mercado (A–Z)](#1-siglas-e-abreviações-de-mercado-az)
2. [Os 6 Passos da Cadeia de Software & Ataques Comuns](#2-os-6-passos-da-cadeia-de-software--ataques-comuns)
3. [Criptografia, Assinaturas Digitais & Sigstore](#3-criptografia-assinaturas-digitais--sigstore)
4. [SBOM, OpenVEX & Regras Automáticas (Rego / Conftest)](#4-sbom-openvex--regras-automáticas-rego--conftest)
5. [Termos Adjacentes (Containers, Node.js, Git, Redes & AppSec)](#5-termos-adjacentes-containers-nodejs-git-redes--appsec)

---

## 1. Siglas e Abreviações de Mercado (A–Z)

| Sigla | Nome em Inglês | O Que Significa na Prática |
| :--- | :--- | :--- |
| **AGPL / GPL** | *Affero / General Public License* | Licenças de código aberto "contagiosas": se você usar uma biblioteca assim em um sistema comercial fechado, pode ser obrigado a abrir o código do sistema inteiro. Por isso empresas costumam bloqueá-las. |
| **AIBOM / ML-BOM** | *AI / Machine Learning Bill of Materials* | Lista de ingredientes de um sistema de Inteligência Artificial (qual modelo foi usado, base de treinamento, pesos e licenças). |
| **API** | *Application Programming Interface* | Porta de entrada por onde sistemas conversam pela rede (ex.: a `payment-api` recebe pedidos de pagamento via HTTP). |
| **CA** | *Certificate Authority* | "Cartório digital" que emite certificados provando quem é o dono de uma chave (ex.: o **Fulcio** no Sigstore). |
| **CI/CD** | *Continuous Integration / Continuous Delivery* | Robô na nuvem (como o GitHub Actions) que baixa o código, instala pacotes, testa, cria a imagem Docker e publica tudo automaticamente. |
| **CPE** | *Common Platform Enumeration* | Formato antigo para dar nome a sistemas e programas em bancos de vulnerabilidades (hoje quase sempre substituído pelo **PURL**). |
| **CSAF** | *Common Security Advisory Framework* | Padrão em JSON usado por empresas para publicar alertas oficiais de falhas de segurança e documentos VEX. |
| **CT** | *Certificate Transparency* | "Livro público de cartório" onde todo certificado emitido fica registrado para ninguém conseguir falsificar sem ser visto. |
| **CVE** | *Common Vulnerabilities and Exposures* | Código único mundial de uma falha de segurança descoberta (ex.: `CVE-2024-29041`). |
| **CVSS** | *Common Vulnerability Scoring System* | Nota de `0.0` a `10.0` que mede o quão grave uma falha pode ser em tese (*LOW, MEDIUM, HIGH, CRITICAL*), mesmo que o seu app nem use a função falha. |
| **CWE** | *Common Weakness Enumeration* | Nome da "família" do erro de programação (ex.: `CWE-601` = redirecionamento aberto). |
| **DAST** | *Dynamic Application Security Testing* | Teste de segurança feito atacando a aplicação enquanto ela está rodando no ar. |
| **DSSE** | *Dead Simple Signing Envelope* | "Envelope digital" simples usado para embrulhar e assinar relatórios JSON (como SBOM e OpenVEX) sem risco de alteração. |
| **EO 14028** | *Executive Order 14028* | Decreto do governo dos EUA (2021) exigindo SBOM e boas práticas de segurança (NIST SSDF) de quem vende software para o governo. |
| **EPSS** | *Exploit Prediction Scoring System* | Porcentagem (`0%` a `100%`) que estima a chance de uma falha (CVE) ser realmente atacada nos próximos 30 dias. |
| **GHCR** | *GitHub Container Registry* | "Galpão" do GitHub para guardar imagens Docker (`ghcr.io/usuario/repo/imagem`). |
| **GPG / PGP** | *GNU Privacy Guard / Pretty Good Privacy* | Programa clássico de assinatura digital com chaves guardadas no PC, usado para assinar commits Git e arquivos. |
| **IaC** | *Infrastructure as Code* | Configurar servidores, redes e containers escrevendo arquivos de texto versionados (como `Dockerfile` e arquivos `.yml`), em vez de clicar em painéis. |
| **JWT** | *JSON Web Token* | "Crachá digital" em texto assinado que prova a identidade de um usuário ou robô por poucos minutos. |
| **KEV** | *Known Exploited Vulnerabilities* | Lista oficial do governo dos EUA com falhas que **já estão sendo atacadas de verdade** na internet. |
| **K8s** | *Kubernetes* | Sistema que gerencia dezenas ou milhares de containers rodando em servidores e pode barrar imagens sem assinatura. |
| **MFA** | *Multi-Factor Authentication* | Autenticação em 2 passos (senha + código no celular/app). Impede que um invasor entre só roubando a senha do dono de um pacote. |
| **NIST SSDF** | *Secure Software Development Framework* | Guia oficial de boas práticas da NIST dividido em 4 grupos: **PO** (preparar), **PS** (proteger código), **PW** (construir com segurança) e **RV** (responder a falhas). |
| **NTIA** | *National Telecommunications and Information Administration* | Órgão dos EUA que listou os campos mínimos obrigatórios de um SBOM (quem fez, nome, versão, lista de dependências, data). |
| **OCI** | *Open Container Initiative* | Padrão universal das imagens Docker. Graças a ele, a imagem, a assinatura e o SBOM ficam guardados juntos no mesmo lugar. |
| **OIDC** | *OpenID Connect* | Protocolo moderno que permite ao GitHub Actions gerar um crachá temporário (**JWT**) provando quem está rodando a esteira, sem precisar guardar senhas fixas. |
| **OPA** | *Open Policy Agent* | Motor que lê regras de segurança (escritas na linguagem **Rego**) para dizer "pode passar" ou "está bloqueado". |
| **OSV** | *Open Source Vulnerabilities* | Banco gratuito de falhas mantido pelo Google para bibliotecas abertas (npm, Python, Alpine, etc.). |
| **PAT** | *Personal Access Token* | Senha longa pessoal do GitHub. Evitamos usá-la em esteiras porque, se vazar, dá acesso amplo à conta. |
| **PKI** | *Public Key Infrastructure* | Conjunto de regras, cartórios digitais (CAs) e chaves que faz certificados digitais funcionarem na internet. |
| **PoLP** | *Principle of Least Privilege* | Princípio do Menor Privilégio: dar para cada pessoa ou robô **só** a permissão mínima necessária (ex.: só ler código, nunca apagar). |
| **PPE** | *Poisoned Pipeline Execution* | Ataque onde alguém envia um código ou Pull Request adulterado para fazer o robô de CI/CD rodar comandos maliciosos e roubar segredos. |
| **PURL** | *Package URL* | Endereço único padronizado de qualquer biblioteca (ex.: `pkg:npm/express@4.18.2`), usado pelos scanners para não errar o nome do pacote. |
| **RBAC** | *Role-Based Access Control* | Controle de acesso baseado em função (ex.: quem é "leitor" não pode publicar imagem). |
| **REST** | *Representational State Transfer* | Jeito padrão de criar APIs Web usando pedidos HTTP simples (`GET` para buscar, `POST` para enviar) e respostas em JSON. |
| **SAN** | *Subject Alternative Name* | Campo dentro do certificado digital onde o **Fulcio** grava o endereço exato do repositório e workflow do GitHub que assinou a imagem. |
| **SAST** | *Static Application Security Testing* | Ferramenta que lê o código-fonte parado procurando erros de segurança antes mesmo de rodar o programa. |
| **SBOM** | *Software Bill of Materials* | Lista completa de todos os ingredientes (bibliotecas e pacotes do sistema) que existem dentro de um software ou container. |
| **SCA** | *Software Composition Analysis* | Análise automática das bibliotecas de terceiros para achar falhas conhecidas (CVEs) e licenças proibidas. |
| **SCVS** | *Software Component Verification Standard* | Lista de checagem da OWASP para medir o nível de maturidade de segurança da cadeia de componentes de uma empresa. |
| **SemVer** | *Semantic Versioning* | Formato de versão `MAIOR.MENOR.CORREÇÃO` (`4.18.2`). Símbolos como `^` deixam o gerenciador baixar atualizações sozinho se não houver trava. |
| **SET** | *Signed Entry Timestamp* | Recibo com carimbo de data/hora assinado pelo **Rekor** provando quando a assinatura foi registrada. |
| **SLSA** | *Supply-chain Levels for Software Artifacts* | Níveis de maturidade (L1, L2, L3) que garantem que o programa foi compilado num ambiente confiável e não foi mexido no caminho. |
| **SPDX** | *Software Package Data Exchange* | Outro formato padrão de SBOM (além do CycloneDX) e também a lista oficial de siglas de licenças (`MIT`, `GPL-3.0-only`). |
| **TSA** | *Timestamp Authority* | Serviço que carimba a data e hora oficial de uma assinatura digital. |
| **TUF** | *The Update Framework* | Conjunto de regras criptográficas que protege atualizações contra arquivos velhos ou falsos. |
| **VEX** | *Vulnerability Exploitability eXchange* | Documento que acompanha o SBOM para avisar se uma falha (CVE) encontrada realmente afeta ou não o nosso sistema. |

---

## 2. Os 6 Passos da Cadeia de Software & Ataques Comuns

1. **Source (Código-Fonte e Git):**
   - **Branch Protection:** Trava no GitHub que proíbe mandar código direto para a branch `main` sem revisão de outra pessoa (Pull Request).
   - **Signed Commits:** Assinatura nos commits provando que foi mesmo você quem escreveu o código.
2. **Dependencies (Bibliotecas de Terceiros):**
   - **Dependency Confusion:** Quando uma empresa tem um pacote interno privado (ex.: `@corp/payment-vault`) e um atacante cria um pacote público com o mesmo nome e versão gigante (`99.0.0`) para enganar o `npm`. Evitamos isso apontando `@corp` para o servidor interno no `src/.npmrc`.
   - **Typosquatting:** Criar um pacote falso com erro de digitação famoso (ex.: `expresss` em vez de `express`) esperando alguém digitar errado.
   - **Lifecycle Scripts (`preinstall` / `postinstall`):** Comandos escondidos dentro de pacotes npm que rodam sozinhos na hora do `npm install`. A flag `--ignore-scripts` desliga isso.
   - **Lockfile (`package-lock.json`):** Lista travada que fixa a versão exata e a "impressão digital" (`sha512`) de cada biblioteca instalada.
3. **Build (Fábrica / CI-CD):**
   - **Runners Efêmeros:** Máquinas criadas do zero só para rodar 1 vez a esteira e depois apagadas (não sobra lixo nem vírus de builds anteriores).
   - **SHA Pinning de Actions:** Em vez de escrever `uses: actions/checkout@v4` (que pode ser trocado depois), fixamos o código exato de 40 letras/números do commit (`@b4ffde65...`).
   - **Permissões Mínimas (`permissions:`):** Dar ao robô apenas `contents: read`, `packages: write` e `id-token: write`, nunca `write-all`.
4. **Artifacts (Imagens Docker / Pacotes):**
   - **Tag Mutável vs. Digest SHA-256:** Uma tag como `:latest` ou `:v1.0.0` é só um apelido que pode ser colado em outra imagem amanhã. Já o **Digest (`@sha256:...`)** é o cálculo matemático único dos arquivos: se mudar 1 letra, o digest muda.
5. **Distribution (Registry / Repositório de Imagens):**
   - **Tag Tampering (Troca de Etiqueta):** Quando alguém substitui a imagem por trás de uma tag conhecida (ex.: troca `payment-api:v1.0.0` por um `busybox` sem assinatura). O `cosign verify` detecta e bloqueia na hora.
6. **Runtime & Compliance (Execução e Auditoria):**
   - **Admission Control:** Porteiro automático (como Kyverno ou OPA Gatekeeper no Kubernetes) que não deixa nenhum container subir se estiver sem assinatura ou violar regras.
   - **Evidence-as-Code:** Guardar as provas de segurança (hashes do lockfile, SBOM, OpenVEX, SLSA) em um arquivo estruturado (`dist/dossie_conformidade.json`).

---

## 3. Criptografia, Sigstore, Proveniência & Atestações

- **Hash Criptográfico (SHA-256 / SHA-512):** Uma conta matemática que transforma qualquer arquivo em um código único de letras e números. Se alguém alterar 1 vírgula do arquivo, o hash muda completamente.
- **Chave Privada vs. Chave Pública:** Na assinatura tradicional (`cosign.key` e `cosign.pub`), você assina com a **chave privada** (secreta, nunca pode ir para o GitHub!) e qualquer pessoa confere usando a **chave pública**.
- **Assinatura Keyless (Sigstore — Sem Chave Fixa):** Em vez de guardar um arquivo `cosign.key` que pode vazar:
  1. O GitHub Actions pede um crachá temporário (**OIDC / JWT**) com `id-token: write`;
  2. O Cosign cria uma chave descartável só na memória e envia para o **Fulcio** junto com o crachá;
  3. O **Fulcio** confere e emite um certificado que vale só **10 minutos**, gravando nele qual repositório e workflow assinaram;
  4. O **Cosign** assina a imagem e registra o carimbo no **Rekor** (um livro público onde nada pode ser apagado, baseado em **Árvore de Merkle**);
  5. A chave descartável é apagada da memória. Depois, qualquer pessoa confere a assinatura usando o endereço do workflow + certificado + registro do Rekor.
- **Atestação *in-toto* (`cosign attest`):** É como grampear um documento assinado (o SBOM ou o laudo OpenVEX) diretamente na imagem Docker dentro do Registry, garantindo que aquele laudo pertence exatamente àquela imagem.

---

## 4. SBOM, OpenVEX & Regras Automáticas (Rego / Conftest)

- **CycloneDX e SPDX:** Os dois formatos padrão de SBOM. Neste projeto usamos **CycloneDX 1.6 (JSON)**.
- **Syft / Trivy:**
  - **Syft:** Olha dentro da imagem Docker e gera o arquivo SBOM (`dist/sbom.cdx.json`).
  - **Trivy:** Lê a imagem e lista quais falhas (CVEs) existem nos pacotes dela.
- **OpenVEX (`not_affected`):** Usado para dizer "essa falha existe na biblioteca, mas **não afeta** nosso app" — sempre explicando o porquê com uma justificativa oficial (ex.: `vulnerable_code_not_in_execute_path`) e um texto humano (`impact_statement`).
- **Policy as Code (Rego v1 + Conftest):**
  - Em vez de uma pessoa ficar revisando arquivos na mão, escrevemos regras em arquivos `.rego` (`import rego.v1`) usando `deny contains msg if { ... }`.
  - O programa **Conftest** lê o `.rego` e testa um arquivo (`Dockerfile`, SBOM, OpenVEX). Se algo estiver fora da regra, ele retorna `FAIL` e trava o processo.

---

## 5. Termos Adjacentes (Containers, Node.js, Git, Redes & AppSec)

- **Container vs. Máquina Virtual (VM):** Uma VM simula um computador inteiro com outro sistema operacional pesado; um container usa o próprio núcleo (kernel) do sistema hospedeiro, isolando apenas processos, pastas e rede (via **Namespaces** e **Cgroups**).
- **`.dockerignore`:** Arquivo que avisa o Docker quais pastas/arquivos locais ele **não** deve copiar ao montar a imagem (economiza tempo e evita copiar segredos ou atalhos quebrados no Windows).
- **`USER root` vs. `USER node`:** `root` (`UID 0`) tem poder total dentro do container. Usar `USER node` limita o estrago caso um invasor consiga rodar comandos dentro da aplicação.
- **`dumb-init`:** Mini-programa colocado na frente do Node.js no `Dockerfile` para garantir que o container feche direito quando receber um comando de desligar.
- **`npm install` vs. `npm ci`:** `npm install` pode atualizar pacotes dentro de faixas como `^4.18.2`; `npm ci` (*Clean Install*) instala exatamente o que está travado no `package-lock.json` e dá erro se os arquivos não baterem.
- **GitHub Codespaces:** Um VS Code completo que abre direto no navegador em uma máquina na nuvem do GitHub — ótimo na Trilha 3 para rodar `cosign verify` sem precisar instalar nada no seu PC.
- **`network_mode: "service:registry"` (Docker Compose):** Faz o container de ferramentas `capstone` dividir o mesmo endereço de rede do `registry`, permitindo acessar `localhost:5000` diretamente.
- **Shift-Left Security:** Colocar testes e travas de segurança o mais cedo possível (no código e no CI), antes que o sistema vá para o ar.
- **Defesa em Profundidade & Zero Trust:** Não confiar em apenas uma proteção (somar lockfile + `--ignore-scripts` + `USER node` + Conftest + assinatura) e sempre exigir prova matemática antes de confiar em qualquer arquivo.
- **Falso Positivo vs. Falso Negativo:** Falso positivo é um alarme falso (o scanner avisa de uma falha que o app nem usa — resolvemos com **OpenVEX**); falso negativo é uma falha real que passou despercebida.
- **Falhas citadas nos exemplos OpenVEX do projeto:**
  - **Prototype Pollution (`CVE-2022-24999`):** Quando dados maliciosos alteram propriedades internas de objetos JavaScript.
  - **ReDoS (`CVE-2020-28500`):** Texto especialmente montado que trava o processador ao passar por uma expressão regular lenta.
  - **Open Redirect (`CVE-2024-29041`):** Quando `res.redirect()` aceita um link enviado pelo usuário e redireciona a vítima para um site malicioso externo.
