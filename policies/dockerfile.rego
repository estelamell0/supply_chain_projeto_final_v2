package main

import rego.v1

# Regra 1: Proibir tags mutaveis :latest na instrucao FROM
deny contains msg if {
	some step in input
	step.Cmd == "from"
	image := step.Value[0]
	endswith(image, ":latest")
	msg := sprintf("VIOLACAO DOCKERFILE: Imagem base '%v' utiliza tag mutavel :latest. Fixe uma versao especifica ou digest SHA-256.", [image])
}

# Regra 2: Proibir execucao explicita como USER root
deny contains msg if {
	some step in input
	step.Cmd == "user"
	step.Value[0] == "root"
	msg := "VIOLACAO DOCKERFILE: Container configurado explicitamente para rodar como 'USER root'. Utilize um usuario nao-privilegiado (ex: USER node)."
}

# Regra 3: Exigir que exista pelo menos uma instrucao USER definida
has_user_instruction if {
	some step in input
	step.Cmd == "user"
}

deny contains msg if {
	not has_user_instruction
	msg := "VIOLACAO DOCKERFILE: Nenhuma instrucao 'USER' encontrada. Containers sem usuario explicito executam como root por padrao."
}

