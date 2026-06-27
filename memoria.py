def memoria_padrao():
    return {
        "assuntos_favoritos": [],
        "palavras_aprendidas": [],
        "erros_comuns": [],
        "pontos_fortes": [],
        "pontos_para_melhorar": [],
        "estilo_aprendizado_detectado": "",
        "ultima_licao": "",
        "proxima_revisao": "",
        "observacoes_do_alex": []
    }


def atualizar_memoria(memoria_atual, novos_dados):
    memoria = memoria_atual or memoria_padrao()

    for chave, valor in novos_dados.items():
        memoria[chave] = valor

    return memoria


def adicionar_item(memoria_atual, categoria, item):
    memoria = memoria_atual or memoria_padrao()

    if categoria not in memoria:
        memoria[categoria] = []

    if item and item not in memoria[categoria]:
        memoria[categoria].append(item)

    return memoria


def resumo_memoria(memoria):
    if not memoria:
        memoria = memoria_padrao()

    return f"""
Assuntos favoritos: {", ".join(memoria.get("assuntos_favoritos", []))}
Palavras aprendidas: {", ".join(memoria.get("palavras_aprendidas", []))}
Erros comuns: {", ".join(memoria.get("erros_comuns", []))}
Pontos fortes: {", ".join(memoria.get("pontos_fortes", []))}
Pontos para melhorar: {", ".join(memoria.get("pontos_para_melhorar", []))}
Estilo de aprendizado detectado: {memoria.get("estilo_aprendizado_detectado", "")}
Última lição: {memoria.get("ultima_licao", "")}
Próxima revisão: {memoria.get("proxima_revisao", "")}
Observações do Alex: {", ".join(memoria.get("observacoes_do_alex", []))}
"""
