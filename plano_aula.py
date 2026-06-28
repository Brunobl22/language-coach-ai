def escolher_plano(acao, memoria=None, perfil=None):
    memoria = memoria or {}
    perfil = perfil or {}

    if acao == "motivar_e_simplificar":
        return {
            "tipo": "apoio",
            "instrucao": "O aluno demonstrou dificuldade. Explique de forma mais simples, com calma e incentivo."
        }

    if acao == "explicar_com_exemplo":
        return {
            "tipo": "explicacao",
            "instrucao": "O aluno fez uma pergunta. Responda com explicação curta, exemplo em inglês e tradução."
        }

    if acao == "elogiar_e_avancar":
        return {
            "tipo": "avanco",
            "instrucao": "O aluno tentou usar inglês. Elogie, corrija se necessário e dê um pequeno desafio."
        }

    if acao == "ensinar_por_interesse":
        return {
            "tipo": "interesse",
            "instrucao": "Use o assunto de interesse do aluno para criar um exemplo prático."
        }

    return {
        "tipo": "conversa",
        "instrucao": "Continue a conversa de forma natural e ensine uma coisa pequena de inglês."
    }


def resumo_plano(plano):
    return f"""
Tipo de aula: {plano.get("tipo", "")}
Instrução pedagógica: {plano.get("instrucao", "")}
"""
