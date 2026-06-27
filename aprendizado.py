def atualizar_aprendizado(memoria, observacoes):
    memoria = memoria or {}

    aprendizado = memoria.get("aprendizado", {
        "palavras_dominadas": [],
        "erros_frequentes": [],
        "assuntos_preferidos": [],
        "dias_estudados": 0,
        "respostas_corretas": 0
    })

    if observacoes.get("palavras_aprendidas"):
        for palavra in observacoes["palavras_aprendidas"]:
            if palavra not in aprendizado["palavras_dominadas"]:
                aprendizado["palavras_dominadas"].append(palavra)

    if observacoes.get("erros_comuns"):
        aprendizado["erros_frequentes"] = observacoes["erros_comuns"]

    if observacoes.get("assuntos_favoritos"):
        for assunto in observacoes["assuntos_favoritos"]:
            if assunto not in aprendizado["assuntos_preferidos"]:
                aprendizado["assuntos_preferidos"].append(assunto)

    if observacoes.get("pontos_fortes"):
        aprendizado["respostas_corretas"] += 1

    aprendizado["dias_estudados"] += 1

    memoria["aprendizado"] = aprendizado

    return memoria


def resumo_aprendizado(memoria):
    memoria = memoria or {}

    aprendizado = memoria.get("aprendizado", {})

    return f"""
Dias estudados: {aprendizado.get('dias_estudados',0)}
Respostas corretas: {aprendizado.get('respostas_corretas',0)}
Palavras dominadas: {len(aprendizado.get('palavras_dominadas',[]))}
Assuntos favoritos: {', '.join(aprendizado.get('assuntos_preferidos',[]))}
"""
