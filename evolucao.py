def analisar_evolucao(memoria):
    memoria = memoria or {}

    palavras = memoria.get("palavras_aprendidas", [])
    erros = memoria.get("erros_comuns", [])
    fortes = memoria.get("pontos_fortes", [])
    melhorar = memoria.get("pontos_para_melhorar", [])

    total_palavras = len(palavras)
    total_erros = len(erros)

    if total_palavras >= 20 and total_erros <= 3:
        nivel_sugerido = "Intermediário"
    elif total_palavras >= 60 and total_erros <= 5:
        nivel_sugerido = "Avançado"
    else:
        nivel_sugerido = "Iniciante"

    return {
        "total_palavras_aprendidas": total_palavras,
        "total_erros_comuns": total_erros,
        "pontos_fortes": fortes,
        "pontos_para_melhorar": melhorar,
        "nivel_sugerido": nivel_sugerido
    }


def resumo_evolucao(memoria):
    evolucao = analisar_evolucao(memoria)

    return f"""
Palavras aprendidas: {evolucao["total_palavras_aprendidas"]}
Erros comuns: {evolucao["total_erros_comuns"]}
Nível sugerido: {evolucao["nivel_sugerido"]}
Pontos fortes: {", ".join(evolucao["pontos_fortes"])}
Pontos para melhorar: {", ".join(evolucao["pontos_para_melhorar"])}
"""
