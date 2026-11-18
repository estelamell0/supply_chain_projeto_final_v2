#!/usr/bin/env python3
"""
tools/selfcheck_capstone.py
Validador local de entrega para as 3 Trilhas do Projeto Final Capstone (v2).
Uso: python3 tools/selfcheck_capstone.py --trilha 1|2|3 [--incremental]
"""

import argparse
import json
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent


def ok(msg: str):
    print(f"  [PASS] {msg}")


def warn(msg: str):
    print(f"  [WARN] {msg}")


def fail(msg: str, errors: list):
    print(f"  [FAIL] {msg}")
    errors.append(msg)


def check_common(errors: list):
    if (ROOT / "cosign.key").exists():
        fail(
            "Chave privada 'cosign.key' encontrada na raiz! Remova antes de commitar em repositorio publico.",
            errors,
        )
    else:
        ok("Nenhuma chave privada 'cosign.key' exposta na raiz.")


def check_vex_customizado(errors: list):
    vex_custom = ROOT / "attestations" / "vex_customizado.openvex.json"
    if not vex_custom.exists():
        fail("Arquivo obrigatorio ausente: attestations/vex_customizado.openvex.json", errors)
        return

    try:
        raw_txt = vex_custom.read_text(encoding="utf-8-sig")
        vdata = json.loads(raw_txt)
        stmts = vdata.get("statements", [])
        if not stmts:
            fail("attestations/vex_customizado.openvex.json esta com 'statements' vazio.", errors)
            return

        if "TODO" in raw_txt:
            warn(
                "attestations/vex_customizado.openvex.json ainda contem marcadores 'TODO' para preencher (justification / impact_statement)."
            )
        else:
            ok(
                f"attestations/vex_customizado.openvex.json valido ({len(stmts)} statement(s) sem TODOs pendentes)."
            )
    except Exception as e:
        fail(f"attestations/vex_customizado.openvex.json invalido: {e}", errors)


def check_rego_openvex(errors: list, min_active_rules: int = 2):
    rego_ov = ROOT / "policies" / "openvex_audit.rego"
    if not rego_ov.exists():
        fail("Arquivo obrigatorio ausente: policies/openvex_audit.rego", errors)
        return

    rtxt = rego_ov.read_text(encoding="utf-8-sig", errors="replace")
    has_import = bool(re.search(r"(?m)^\s*import\s+rego\.v1\b", rtxt))
    active_denies = len(re.findall(r"(?m)^\s*deny\s+contains\b", rtxt))

    if not has_import:
        fail("policies/openvex_audit.rego precisa declarar 'import rego.v1'.", errors)
    elif active_denies < min_active_rules:
        warn(
            f"policies/openvex_audit.rego possui apenas {active_denies} regra(s) 'deny contains' ativa(s); esperado >= {min_active_rules} (complete os TODOs)."
        )
    else:
        ok(
            f"policies/openvex_audit.rego valido com 'import rego.v1' e {active_denies} regra(s) 'deny contains' ativa(s)."
        )


def is_incremental_template(txt: str, cli_incremental: bool) -> bool:
    if cli_incremental:
        return True
    return bool(re.search(r"(?m)^\s*-\s*`?\[[xX]\]\s*Modo Incremental\b", txt))


def check_template_gaps(tpl_path: Path, is_incremental: bool, extra_markers: list = None):
    if not tpl_path.exists():
        warn(f"Template nao encontrado: {tpl_path.relative_to(ROOT)}")
        return

    txt = tpl_path.read_text(encoding="utf-8-sig", errors="replace")

    # Se estiver em Modo Incremental, ignora marcadores dentro da secao Bloco Express
    txt_to_check = txt
    if is_incremental:
        txt_to_check = re.split(r"(?m)^##\s+.*Bloco Express", txt, maxsplit=1)[0]

    pending_dots = txt_to_check.count("[...]")
    pending_paste = txt_to_check.count("[Cole aqui")
    extra_hits = sum(txt_to_check.count(m) for m in (extra_markers or []))
    total_pending = pending_dots + pending_paste + extra_hits

    if total_pending > 0:
        warn(
            f"{tpl_path.name} ainda contem {total_pending} lacuna(s)/marcador(es) de modelo para preencher."
        )
    else:
        mode_label = "Modo Incremental" if is_incremental else "Trilha Unica"
        ok(f"{tpl_path.name} preenchido ({mode_label}).")


def check_trilha_1(errors: list):
    print("\n=== VALIDANDO TRILHA 1 (ANALISE ESTÁTICA & ARQUITETURA | <= 2h) ===")
    report_candidates = [
        ROOT / "RELATORIO_AUDITORIA_TRILHA_1.md",
        ROOT / "docs" / "trilha_1" / "TEMPLATE_ENTREGA_TRILHA_1.md",
    ]
    found_report = next((p for p in report_candidates if p.exists()), None)
    if not found_report:
        fail("Relatorio da Trilha 1 nao encontrado.", errors)
    else:
        txt = found_report.read_text(encoding="utf-8-sig", errors="replace")
        pending = txt.count("[...]")
        if pending > 0:
            warn(f"{found_report.name} ainda contem {pending} lacuna(s) '[...]' para preencher.")
        else:
            ok(f"{found_report.name} preenchido sem lacunas '[...]'.")

    df_hard = ROOT / "docker" / "Dockerfile.hardened"
    if df_hard.exists():
        df_txt = df_hard.read_text(encoding="utf-8-sig", errors="replace")
        active_lines = [
            line.split("#", 1)[0].strip()
            for line in df_txt.splitlines()
            if line.split("#", 1)[0].strip()
        ]
        has_sha256 = any(
            l.upper().startswith("FROM ") and "@sha256:" in l.lower() for l in active_lines
        )
        user_lines = [l for l in active_lines if re.match(r"(?i)^USER\s+\S+", l)]
        has_non_root_user = bool(user_lines) and not any(
            re.match(r"(?i)^USER\s+(?:root|0)(?:\s|$|:)", l) for l in user_lines
        )
        if has_sha256 and has_non_root_user:
            ok("docker/Dockerfile.hardened encontrado com digest SHA-256 e usuario nao-root.")
        else:
            warn(
                "docker/Dockerfile.hardened existe, mas confira se contem 'FROM ...@sha256:' e instrucao ativa 'USER' nao-root."
            )
    else:
        fail("Arquivo obrigatorio ausente: docker/Dockerfile.hardened", errors)

    check_vex_customizado(errors)
    check_rego_openvex(errors, min_active_rules=3)


def check_trilha_2(errors: list, cli_incremental: bool):
    print("\n=== VALIDANDO TRILHA 2 (SANDBOX CLI LOCAL & CONFTEST | <= 2h) ===")
    sbom = ROOT / "dist" / "sbom.cdx.json"
    if sbom.exists():
        try:
            sdata = json.loads(sbom.read_text(encoding="utf-8-sig"))
            if sdata.get("bomFormat") == "CycloneDX":
                ok(
                    f"dist/sbom.cdx.json valido ({len(sdata.get('components', []))} componentes)."
                )
            else:
                fail("dist/sbom.cdx.json nao esta no formato CycloneDX.", errors)
        except Exception as e:
            fail(f"dist/sbom.cdx.json invalido: {e}", errors)
    else:
        fail("Arquivo obrigatorio ausente: dist/sbom.cdx.json (gere com syft).", errors)

    dossier = ROOT / "dist" / "dossie_conformidade.json"
    if dossier.exists():
        try:
            ddata = json.loads(dossier.read_text(encoding="utf-8-sig"))
            if "evidence_chain" in ddata:
                ok(
                    f"dist/dossie_conformidade.json valido (chaves: {list(ddata['evidence_chain'].keys())})."
                )
            else:
                warn("dist/dossie_conformidade.json encontrado, mas confira o campo 'evidence_chain'.")
        except Exception as e:
            fail(f"dist/dossie_conformidade.json invalido: {e}", errors)
    else:
        fail(
            "Arquivo obrigatorio ausente: dist/dossie_conformidade.json (rode python3 tools/generate_compliance_dossier.py).",
            errors,
        )

    check_vex_customizado(errors)
    check_rego_openvex(errors, min_active_rules=2)

    tpl2 = ROOT / "docs" / "trilha_2" / "TEMPLATE_ENTREGA_TRILHA_2.md"
    txt2 = tpl2.read_text(encoding="utf-8-sig", errors="replace") if tpl2.exists() else ""
    inc = is_incremental_template(txt2, cli_incremental)
    check_template_gaps(tpl2, inc)


def check_trilha_3(errors: list, cli_incremental: bool):
    print("\n=== VALIDANDO TRILHA 3 (CI/CD NUVEM & KEYLESS OIDC | <= 2h) ===")
    wf = ROOT / ".github" / "workflows" / "golden_pipeline_capstone.yml"
    if not wf.exists():
        fail(".github/workflows/golden_pipeline_capstone.yml nao encontrado.", errors)
    else:
        wtxt = wf.read_text(encoding="utf-8-sig", errors="replace")
        active_lines = [line.split("#", 1)[0] for line in wtxt.splitlines()]
        active_text = "\n".join(active_lines)

        uses_lines = re.findall(r"uses:\s*([^\s#]+)", active_text)
        unpinned = [u for u in uses_lines if not re.search(r"@[0-9a-fA-F]{40}$", u)]
        if unpinned:
            fail(
                f"Actions sem SHA-1 de 40 caracteres no workflow (resolva o TODO): {unpinned}",
                errors,
            )
        else:
            ok(
                f"Todas as {len(uses_lines)} GitHub Actions estao fixadas por SHA-1 de 40 caracteres."
            )

        if re.search(r"(?m)^\s*id-token:\s*write\b", active_text):
            ok("Permissao ativa 'id-token: write' configurada para Cosign Keyless OIDC.")
        else:
            fail(
                "Permissao 'id-token: write' esta comentada ou ausente no workflow (resolva o TODO).",
                errors,
            )

    vault_mock = ROOT / "src" / "node_modules" / "@corp" / "payment-vault"
    if vault_mock.exists():
        ok("Mock corporativo src/node_modules/@corp/payment-vault preservado para CI/CD.")
    else:
        fail(
            "Pasta src/node_modules/@corp/payment-vault ausente! Necessaria para build no GitHub Actions.",
            errors,
        )

    pkg = ROOT / "src" / "package.json"
    if pkg.exists():
        pdata = json.loads(pkg.read_text(encoding="utf-8-sig"))
        if "gpl-math-lib" in pdata.get("dependencies", {}):
            warn(
                "'gpl-math-lib' ainda esta em src/package.json (na Trilha 3, remova-a apos registrar o bloqueio da 1a run)."
            )
        else:
            ok("'gpl-math-lib' removida de src/package.json (pronto para run verde).")

    check_vex_customizado(errors)
    check_rego_openvex(errors, min_active_rules=2)

    tpl3 = ROOT / "docs" / "trilha_3" / "TEMPLATE_ENTREGA_TRILHA_3.md"
    txt3 = tpl3.read_text(encoding="utf-8-sig", errors="replace") if tpl3.exists() else ""
    inc = is_incremental_template(txt3, cli_incremental)
    check_template_gaps(tpl3, inc, extra_markers=["<usuario>"])


def main():
    parser = argparse.ArgumentParser(description="Self-check do Projeto Final Capstone (v2)")
    parser.add_argument(
        "--trilha",
        type=int,
        choices=[1, 2, 3],
        required=True,
        help="Numero da trilha escolhida (1, 2 ou 3)",
    )
    parser.add_argument(
        "--incremental",
        action="store_true",
        help="Ativa validacao em Modo Incremental (dispensa Bloco Express se ja concluiu trilha anterior)",
    )
    args = parser.parse_args()

    errors = []
    print("=" * 68)
    print(f" SELF-CHECK CAPSTONE v2 — TRILHA {args.trilha}")
    print("=" * 68)
    check_common(errors)

    if args.trilha == 1:
        check_trilha_1(errors)
    elif args.trilha == 2:
        check_trilha_2(errors, args.incremental)
    elif args.trilha == 3:
        check_trilha_3(errors, args.incremental)

    print("=" * 68)
    if errors:
        print(
            f"[RESULTADO] {len(errors)} pendencia(s) critica(s) encontrada(s). Corrija antes da entrega."
        )
        sys.exit(1)
    print("[RESULTADO] Verificacao estrutural concluida sem erros criticos!")
    sys.exit(0)


if __name__ == "__main__":
    main()
