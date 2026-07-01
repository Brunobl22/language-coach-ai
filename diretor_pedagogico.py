def decidir_direcao(
    conselho,
    memoria=None,
    perfil=None,
    evolucao=None,
    objetivo=None,
    plano=None,
    roteiro=None,
    missao=None
):
    memoria = memoria or {}
    perfil = perfil or {}
    evolucao = evolucao or {}
    objetivo = objetivo or {}
    plano = plano or {}
    roteiro = roteiro or {}
    missao = missao or {}

    direcao = {
        "decisao_final": "conduzir_com_leveza",
        "prioridade": "clareza",
        "tom": "paciente",
        "nivel_dificuldade": "facil",
        "acao": "ensinar_uma_coisa_pequena",
        "usar_memoria": False,
        "revisar": False,
        "avancar": False,
        "motivar": True,
        "observacao": "Seguir o conselho pedagógico com equilíbrio."
    }

    texto_conselho = str(conselho).lower()

    if "dificuldade" in texto_conselho or "desmotivado" in texto_conselho:
        direcao.update({
            "decisao_final": "acolher_e_simplificar",
            "prioridade": "seguranca_emocional",
            "tom": "acolhedor",
            "nivel_dificuldade": "muito_facil",
            "acao": "explicar_com_exemplo_simples",
            "motivar": True,
            "observacao": "O aluno precisa se sentir seguro antes de avançar."
        })

    elif "dúvida" in texto_conselho or "duvida" in texto_conselho or "explicar" in texto_conselho:
        direcao.update({
            "decisao_final": "explicar_antes_de_avancar",
            "prioridade": "clareza",
            "tom": "paciente",
            "nivel_dificuldade": "facil",
            "acao": "dar_exemplo_curto_e_confirmar_entendimento",
            "observacao": "O aluno precisa entender antes de receber novo desafio."
        })

    elif "acerto" in texto_conselho or "avançar" in texto_conselho or "avancar" in texto_conselho:
        direcao.update({
            "decisao_final": "elogiar_e_avancar",
            "prioridade": "pequeno_avanco",
            "tom": "positivo",
            "nivel_dificuldade": "facil",
            "acao": "dar_um_mini_desafio",
            "avancar": True,
            "observacao": "O aluno demonstrou compreensão e pode avançar um pouco."
        })

    if memoria.get("erros_frequentes"):
        direcao["usar_memoria"] = True
        direcao["revisar"] = True
        direcao["observacao"] += " Revisar erros frequentes do aluno."

    if evolucao.get("precisa_revisao"):
        direcao["revisar"] = True
        direcao["avancar"] = False
        direcao["acao"] = "revisar_antes_de_avancar"
        direcao["observacao"] += " A evolução indica necessidade de revisão."

    return direcao


def resumo_diretor(direcao):
    return f"""
Direção pedagógica final:

Decisão:
{direcao.get("decisao_final", "")}

Prioridade:
{direcao.get("prioridade", "")}

Tom:
{direcao.get("tom", "")}

Nível de dificuldade:
{direcao.get("nivel_dificuldade", "")}

Ação:
{direcao.get("acao", "")}

Usar memória:
{direcao.get("usar_memoria", False)}

Revisar:
{direcao.get("revisar", False)}

Avançar:
{direcao.get("avancar", False)}

Motivar:
{direcao.get("motivar", True)}

Observação:
{direcao.get("observacao", "")}
"""
