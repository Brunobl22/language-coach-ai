def revisar_resposta(analise, estrategia=None, coordenador=None):
    estrategia = estrategia or {}
    coordenador = coordenador or {}

    revisao = {
        "foco": "clareza",
        "alerta": "Nenhum alerta importante.",
        "ajuste": "Responder de forma simples, natural e útil."
    }

    if analise.get("emocao") == "dificuldade":
        revisao = {
            "foco": "acolhimento",
            "alerta": "O aluno pode estar desmotivado.",
            "ajuste": "Comece com incentivo, reduza a dificuldade e evite explicação longa."
        }

    elif analise.get("parece_duvida"):
        revisao = {
            "foco": "compreensao",
            "alerta": "O aluno pode não ter entendido.",
            "ajuste": "Explique com exemplo curto e pergunte se ficou claro."
        }

    elif analise.get("parece_acerto"):
        revisao = {
            "foco": "progresso",
            "alerta": "O aluno está pronto para um pequeno avanço.",
            "ajuste": "Elogie e dê um desafio leve."
        }

    return revisao


def resumo_supervisor(revisao):
    return f"""
Revisão do Supervisor:

Foco:
{revisao.get("foco", "")}

Alerta:
{revisao.get("alerta", "")}

Ajuste final:
{revisao.get("ajuste", "")}
"""
