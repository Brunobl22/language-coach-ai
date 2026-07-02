def escolher_proximo_passo(perfil=None, memoria=None, progresso=None):
    perfil = perfil or {}
    memoria = memoria or {}
    progresso = progresso or {}

    nivel = progresso.get("nivel", 0)

    etapas = [
        "Cumprimentos",
        "Palavras básicas",
        "Frases simples",
        "Perguntas",
        "Mini diálogos",
        "Conversação"
    ]

    if nivel >= len(etapas):
        nivel = len(etapas) - 1

    return {
        "nivel": nivel,
        "tema": etapas[nivel],
        "objetivo": f"Ensinar {etapas[nivel]}",
        "proximo_nivel": min(nivel + 1, len(etapas) - 1)
    }
