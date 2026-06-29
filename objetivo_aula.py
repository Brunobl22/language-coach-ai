 def escolher_objetivo_aula(analise, memoria=None, perfil=None, nivel="Iniciante", modo="Conversação"):
    memoria = memoria or {}
    perfil = perfil or {}

    aprendizado = memoria.get("aprendizado", {})
    palavras = aprendizado.get("palavras_dominadas", [])
    erros = aprendizado.get("erros_frequentes", [])
    assuntos = aprendizado.get("assuntos_preferidos", [])

    if analise.get("emocao") == "dificuldade":
        return {
            "objetivo": "recuperar_confiança",
            "descricao": "Ajudar o aluno a se sentir capaz antes de ensinar conteúdo novo.",
            "atividade": "Faça uma pergunta simples e elogie qualquer tentativa."
        }

    if analise.get("parece_duvida"):
        return {
            "objetivo": "resolver_duvida",
            "descricao": "Entender a dúvida do aluno e explicar com exemplo curto.",
            "atividade": "Pergunte qual parte ele não entendeu ou explique com uma frase simples."
        }

    if "hello" not in palavras and nivel == "Iniciante":
        return {
            "objetivo": "cumprimentos_basicos",
            "descricao": "Ensinar cumprimentos básicos em inglês.",
            "atividade": "Ensine Hello e Hi, depois peça para o aluno responder How are you?"
        }

    if erros:
        return {
            "objetivo": "revisar_erro_frequente",
            "descricao": f"Revisar um erro frequente do aluno: {erros[0]}.",
            "atividade": "Explique o erro de forma simples e peça uma nova tentativa."
        }

    if assuntos:
        return {
            "objetivo": "aprender_por_interesse",
            "descricao": f"Usar o interesse do aluno em {assuntos[0]} para ensinar inglês.",
            "atividade": "Crie uma frase simples em inglês usando esse assunto."
        }

    return {
        "objetivo": "conversa_guiada",
        "descricao": "Manter uma conversa leve e ensinar uma coisa pequena por vez.",
        "atividade": "Faça uma pergunta simples em inglês com tradução."
    }


def resumo_objetivo(objetivo):
    return f"""
Objetivo da aula: {objetivo.get("objetivo", "")}
Descrição: {objetivo.get("descricao", "")}
Atividade sugerida: {objetivo.get("atividade", "")}
"""
