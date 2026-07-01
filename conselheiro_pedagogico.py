def reunir_conselho(
    mentor_resumo="",
    estrategia_resumo="",
    coordenador_resumo="",
    supervisor_resumo="",
    missao_resumo="",
    plano_resumo="",
    roteiro_resumo=""
):
    decisao = f"""
Conselho Pedagógico do Super Alex:

Mentor:
{mentor_resumo}

Estratégia:
{estrategia_resumo}

Coordenador:
{coordenador_resumo}

Supervisor:
{supervisor_resumo}

Missão:
{missao_resumo}

Plano:
{plano_resumo}

Roteiro:
{roteiro_resumo}

Decisão final:
Responda como um professor humano, claro, paciente e estratégico.
Use a missão, o plano e o roteiro como prioridade.
Se houver conflito entre módulos, siga esta ordem:
1. Segurança emocional do aluno.
2. Clareza da explicação.
3. Objetivo da aula.
4. Pequeno avanço pedagógico.
5. Motivação para continuar.
"""
    return decisao
