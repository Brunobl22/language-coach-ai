def observar_aluno(mensagem, analise):
    mensagem = (mensagem or "").lower()

    observacoes = {
        "palavras_aprendidas": [],
        "erros_comuns": [],
        "assuntos_favoritos": [],
        "pontos_fortes": [],
        "pontos_para_melhorar": [],
        "observacoes_do_alex": []
    }

    if analise.get("tem_ingles"):
        observacoes["pontos_fortes"].append("Tentou responder em inglês")

    if analise.get("parece_acerto"):
        observacoes["observacoes_do_alex"].append("Aluno demonstrou confiança ao responder em inglês")

    if analise.get("emocao") == "dificuldade":
        observacoes["pontos_para_melhorar"].append("Precisa de explicações mais simples")
        observacoes["observacoes_do_alex"].append("Aluno demonstrou dificuldade e precisa de incentivo")

    if analise.get("assunto"):
        observacoes["assuntos_favoritos"].append(analise["assunto"])

    palavras = ["hello", "thank you", "thanks", "good morning", "good night", "please", "sorry"]

    for palavra in palavras:
        if palavra in mensagem:
            observacoes["palavras_aprendidas"].append(palavra)

    return observacoes
