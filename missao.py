def definir_missao(analise, memoria=None, perfil=None):
    memoria = memoria or {}
    perfil = perfil or {}

    if analise.get("emocao") == "dificuldade":
        return {
            "missao": "devolver_confianca",
            "descricao": "Fazer o aluno acreditar que consegue aprender."
        }

    if analise.get("parece_duvida"):
        return {
            "missao": "eliminar_duvida",
            "descricao": "Garantir que o aluno compreendeu antes de avançar."
        }

    if analise.get("parece_acerto"):
        return {
            "missao": "consolidar_conhecimento",
            "descricao": "Reforçar o acerto e aumentar um pouco o desafio."
        }

    return {
        "missao": "manter_evolucao",
        "descricao": "Ensinar uma pequena coisa nova naturalmente."
    }


def resumo_missao(missao):
    return f"""
Missão atual:
{missao.get("missao","")}

Objetivo:
{missao.get("descricao","")}
"""
