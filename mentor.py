def orientar_professor(analise, memoria=None, perfil=None):
    memoria = memoria or {}
    perfil = perfil or {}

    orientacoes = []

    if analise.get("emocao") == "dificuldade":
        orientacoes.append(
            "Explique devagar, use palavras simples e incentive o aluno."
        )

    if analise.get("parece_duvida"):
        orientacoes.append(
            "Antes de responder, descubra exatamente onde está a dúvida."
        )

    if analise.get("parece_acerto"):
        orientacoes.append(
            "Elogie o esforço e aumente um pouco a dificuldade."
        )

    if analise.get("assunto"):
        orientacoes.append(
            f"Use exemplos relacionados a {analise['assunto']}."
        )

    if not orientacoes:
        orientacoes.append(
            "Conduza uma conversa leve e ensine algo novo naturalmente."
        )

    return orientacoes


def resumo_mentor(orientacoes):
    return "\n".join(f"- {item}" for item in orientacoes)
