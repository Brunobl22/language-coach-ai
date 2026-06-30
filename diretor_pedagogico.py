def decidir_estrategia(analise, memoria=None, perfil=None, missao=None, plano=None):
    memoria = memoria or {}
    perfil = perfil or {}
    missao = missao or {}
    plano = plano or {}

    estrategia = {
        "tipo": "conversa_guiada",
        "decisao": "conduzir com leveza",
        "motivo": "Nenhum sinal forte detectado.",
        "proxima_acao": "Faça uma pergunta simples e ensine uma pequena coisa."
    }

    if analise.get("emocao") == "dificuldade":
        estrategia = {
            "tipo": "apoio_emocional",
            "decisao": "reduzir dificuldade",
            "motivo": "O aluno demonstrou dificuldade ou desmotivação.",
            "proxima_acao": "Acolha, simplifique e faça uma pergunta fácil."
        }

    elif analise.get("parece_duvida"):
        estrategia = {
            "tipo": "explicacao",
            "decisao": "explicar antes de avançar",
            "motivo": "O aluno parece ter uma dúvida.",
            "proxima_acao": "Explique com exemplo curto e confirme se entendeu."
        }

    elif analise.get("parece_acerto"):
        estrategia = {
            "tipo": "desafio",
            "decisao": "aumentar um pouco o nível",
            "motivo": "O aluno demonstrou acerto.",
            "proxima_acao": "Elogie e dê um pequeno desafio."
        }

    return estrategia


def resumo_estrategia(estrategia):
    return f"""
Estratégia pedagógica:
{estrategia.get("tipo", "")}

Decisão:
{estrategia.get("decisao", "")}

Motivo:
{estrategia.get("motivo", "")}

Próxima ação:
{estrategia.get("proxima_acao", "")}
"""
