package main

import rego.v1

# Lista de licencas copyleft fortes proibidas para software proprietario comercial
forbidden_licenses := {"GPL-3.0", "GPL-3.0-only", "GPL-3.0-or-later", "AGPL-3.0", "AGPL-3.0-only"}

# Regra 1: Validar que o artefato é um CycloneDX válido
deny contains msg if {
	input.bomFormat != "CycloneDX"
	msg := sprintf("VIOLACAO SBOM: Formato invalido (%v). Exige-se padrao CycloneDX.", [object.get(input, "bomFormat", "desconhecido")])
}

# Regra 2: Bloquear componentes com licencas proibidas (ex: gpl-math-lib)
deny contains msg if {
	some comp in object.get(input, "components", [])
	some lic_entry in object.get(comp, "licenses", [])
	lic_obj := object.get(lic_entry, "license", {})
	lic_id := object.get(lic_obj, "id", object.get(lic_obj, "name", ""))
	lic_id in forbidden_licenses
	msg := sprintf("VIOLACAO DE LICENCA: O componente '%v@%v' possui licenca proibida '%v'. Remova ou substitua a dependencia.", [comp.name, comp.version, lic_id])
}
