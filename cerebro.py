 def analisar_mensagem(mensagem):
    texto = (mensagem or "").lower()

    analise = {
        "tem_ingles": False,
         "parece_duvida": False,
        "parece_acerto": False,
        "assunto": "",
        "emocao": "neutra"
    }

    palavras_ingles = [
        "hello", "hi", "thank", "thanks", "good", "morning",
        "afternoon", "night", "you", "i am", "i'm", "fine",
        "yes", "no", "please", "sorry"
    ]

    if any(palavra in texto for palavra in palavras_ingles):
        analise["tem_ingles"] = True

    if "?" in texto or "como" in texto or "o que" in texto or "significa" in texto:
        analise["parece_duvida"] = True

    if analise["tem_ingles"] and not analise["parece_duvida"]:
        analise["parece_acerto"] = True

    if "viagem" in texto or "airport" in texto:
        analise["assunto"] = "viagem"
    elif "trabalho" in texto or "job" in texto or "work" in texto:
        analise["assunto"] = "trabalho"
    elif "jogo" in texto or "game" in texto:
        analise["assunto"] = "jogos"
    elif "comida" in texto or "food" in texto:
        analise["assunto"] = "comida"

    if "difícil" in texto or "nao consigo" in texto or "não consigo" in texto:
        analise["emocao"] = "dificuldade"
    elif "obrigado" in texto or "valeu" in texto:
        analise["emocao"] = "gratidao"

    return analise


def escolher_proxima_acao(analise, perfil=None, memoria=None):
    if analise.get("emocao") == "dificuldade":
        return "motivar_e_simplificar"

    if analise.get("parece_duvida"):
        return "explicar_com_exemplo"

    if analise.get("parece_acerto"):
        return "elogiar_e_avancar"

    if analise.get("assunto"):
        return "ensinar_por_interesse"

    return "continuar_conversa"


def montar_contexto_alex(perfil_resumo="", memoria_resumo="", acao="continuar_conversa"):
    return f"""
Contexto do aluno:
{perfil_resumo}

Memória pedagógica:
{memoria_resumo}

Ação recomendada para esta resposta:
{acao}

Use esse contexto para responder como Teacher Alex.
"""
