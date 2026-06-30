def montar_roteiro_aula(analise, plano=None, estrategia=None, coordenador=None, supervisor=None):
    plano = plano or {}
    estrategia = estrategia or {}
    coordenador = coordenador or {}
    supervisor = supervisor or {}

    passos = [
        "1. Responda como professor humano, paciente e natural.",
        "2. Acolha o aluno em português simples.",
        "3. Se houver erro, corrija com calma e sem constranger.",
        "4. Ensine apenas uma coisa pequena por vez.",
        "5. Mostre 1 exemplo curto em inglês com tradução.",
        "6. Termine com uma pergunta simples ou mini desafio.",
    ]

    if analise.get("emocao") == "dificuldade":
        passos.append("7. Reduza a dificuldade e incentive o aluno.")

    if analise.get("parece_duvida"):
        passos.append("7. Explique de forma mais simples antes de avançar.")

    if analise.get("parece_acerto"):
        passos.append("7. Elogie e aumente só um pouco o desafio.")

    return "\n".join(passos)


def resumo_roteiro(roteiro):
    return f"""
Roteiro obrigatório da resposta:
{roteiro}
"""
