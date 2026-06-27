def perfil_padrao():
    return {
        "nome": "",
        "pais": "Brasil",
        "cidade": "",
        "idioma_nativo": "Português",
        "idioma_estudando": "Inglês",
        "nivel": "Iniciante",
        "objetivo": "",
        "interesses": [],
        "profissao": "",
        "tempo_disponivel": 20,
        "estilo_aprendizado": "Exemplos práticos",
        "personalidade_alex": "Amigável"
    }


def atualizar_perfil(perfil_atual, novos_dados):
    perfil = perfil_atual or perfil_padrao()

    for chave, valor in novos_dados.items():
        perfil[chave] = valor

    return perfil


def resumo_perfil(perfil):
    if not perfil:
        perfil = perfil_padrao()

    return f"""
Nome: {perfil.get("nome", "")}
País: {perfil.get("pais", "")}
Cidade: {perfil.get("cidade", "")}
Idioma nativo: {perfil.get("idioma_nativo", "")}
Idioma estudando: {perfil.get("idioma_estudando", "")}
Nível: {perfil.get("nivel", "")}
Objetivo: {perfil.get("objetivo", "")}
Interesses: {", ".join(perfil.get("interesses", []))}
Estilo de aprendizado: {perfil.get("estilo_aprendizado", "")}
Personalidade desejada do Alex: {perfil.get("personalidade_alex", "")}
"""
