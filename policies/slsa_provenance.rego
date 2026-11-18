package main

import rego.v1

allowed_builders := {
	"https://github.com/actions/runner/slsa-builder-l2",
	"https://github.com/slsa-framework/slsa-github-generator/.github/workflows/generator_container_slsa3.yml",
}

# Extrai o predicado independentemente de estar envelopado em Statement in-toto ou direto
slsa_pred := object.get(input, "predicate", input)

# Regra 1: Validar que o Builder eh oficial e autorizado
deny contains msg if {
	run_details := object.get(slsa_pred, "runDetails", {})
	builder := object.get(run_details, "builder", {})
	builder_id := object.get(builder, "id", "")
	not builder_id in allowed_builders
	msg := sprintf("VIOLACAO SLSA: Builder '%v' nao pertence a lista de construtores oficiais autorizados.", [builder_id])
}

# Regra 2: Exigir que o build tenha sido gerado exclusivamente a partir da branch main
deny contains msg if {
	build_def := object.get(slsa_pred, "buildDefinition", {})
	ext_params := object.get(build_def, "externalParameters", {})
	workflow := object.get(ext_params, "workflow", {})
	ref := object.get(workflow, "ref", "")
	ref != "refs/heads/main"
	msg := sprintf("VIOLACAO SLSA: Artefato compilado na referencia '%v'. Apenas builds da branch 'refs/heads/main' sao permitidos para producao.", [ref])
}
