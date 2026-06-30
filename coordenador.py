def avaliar_resposta(analise, memoria=None, perfil=None):
    memoria = memoria or {}
    perfil = perfil or {}

    avaliacao = {
        "status": "continuar",
        "motivo": "A aula pode seguir normalmente.",
        "proximo_passo": "Ensinar o próximo conteúdo."
    }

    if analise.get("emocao") == "dificuldade":
        avaliacao = {
            "status": "reforcar",
            "motivo": "O aluno demonstrou dificuldade.",
            "proximo_passo": "Repetir com exemplos mais simples."
        }

    elif analise.get("parece_duvida"):
        avaliacao = {
            "status": "explicar",
            "motivo": "Ainda existe uma dúvida.",
            "proximo_passo": "Explicar novamente antes de avançar."
        }

    elif analise.get("parece_acerto"):
        avaliacao = {
            "status": "avancar",
            "motivo": "O aluno demonstrou compreensão.",
            "proximo_passo": "Aumentar um pouco a dificuldade."
        }

    return avaliacao


def resumo_coordenador(avaliacao):
    return f"""
Avaliação pedagógica:

Status:
{avaliacao.get("status", "")}

Motivo:
{avaliacao.get("motivo", "")}

Próximo passo:
{avaliacao.get("proximo_passo", "")}
"""
