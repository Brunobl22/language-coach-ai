def decidir_direcao(
    conselho=None,
    memoria=None,
    perfil=None,
    evolucao=None,
    objetivo=None,
    plano=None,
    roteiro=None,
    missao=None,
    mentor=None,
    coordenador=None,
    supervisor=None
):
    conselho = conselho or {}
    memoria = memoria or {}
    perfil = perfil or {}
    evolucao = evolucao or {}
    objetivo = objetivo or {}
    plano = plano or {}
    roteiro = roteiro or {}
    missao = missao or {}
    mentor = mentor or {}
    coordenador = coordenador or {}
    supervisor = supervisor or {}

    texto = " ".join([
        str(conselho),
        str(memoria),
        str(perfil),
        str(evolucao),
        str(objetivo),
        str(plano),
        str(roteiro),
        str(missao),
        str(mentor),
        str(coordenador),
        str(supervisor)
    ]).lower()

    direcao = {
        "decisao_final": "conduzir_com_leveza",
        "prioridade": "clareza",
        "tom": "paciente_e_natural",
        "nivel_dificuldade": "facil",
        "acao": "ensinar_uma_coisa_pequena",
        "usar_memoria": True,
        "revisar": False,
        "avancar": False,
        "motivar": True,
        "regra_final": "Responda como professor humano, simples, claro e acolhedor.",
        "observacao": "Seguir o plano, mas adaptar conforme a necessidade do aluno."
    }

    if "dificuldade" in texto or "desmotivado" in texto or "confuso" in texto:
        direcao.update({
            "decisao_final": "acolher_e_simplificar",
            "prioridade": "seguranca_emocional",
            "tom": "acolhedor_e_calmo",
            "nivel_dificuldade": "muito_facil",
            "acao": "explicar_com_exemplo_simples",
            "revisar": True,
            "avancar": False,
            "observacao": "O aluno precisa se sentir seguro antes de avançar."
        })

    elif "dúvida" in texto or "duvida" in texto or "explicar" in texto:
        direcao.update({
            "decisao_final": "explicar_antes_de_avancar",
            "prioridade": "clareza",
            "tom": "paciente",
            "nivel_dificuldade": "facil",
            "acao": "dar_exemplo_curto_e_confirmar_entendimento",
            "revisar": True,
            "avancar": False,
            "observacao": "O aluno precisa entender antes de receber novo desafio."
        })

    elif "acerto" in texto or "avançar" in texto or "avancar" in texto:
        direcao.update({
            "decisao_final": "elogiar_e_avancar",
            "prioridade": "pequeno_avanco",
            "tom": "positivo",
            "nivel_dificuldade": "facil",
            "acao": "dar_um_mini_desafio",
            "revisar": False,
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

    if supervisor and str(supervisor).lower().find("problema") != -1:
        direcao["revisar"] = True
        direcao["avancar"] = False
        direcao["observacao"] += " O supervisor encontrou ponto de atenção."

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

Regra final:
{direcao.get("regra_final", "")}

Observação:
{direcao.get("observacao", "")}
"""
