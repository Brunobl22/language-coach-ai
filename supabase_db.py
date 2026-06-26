def carregar_usuarios(supabase, tabela="usuarios", progresso_padrao=None):
    usuarios = {}

    try:
        resposta = supabase.table(tabela).select("*").execute()

        for item in resposta.data:
            usuarios[item["usuario"]] = {
                "senha": item["senha"],
                "progresso": item.get("progresso") or progresso_padrao()
            }

    except Exception:
        return {}

    return usuarios


def salvar_usuario(supabase, usuario, senha, progresso, tabela="usuarios"):
    supabase.table(tabela).upsert(
        {
            "usuario": usuario,
            "senha": senha,
            "progresso": progresso
        },
        on_conflict="usuario"
    ).execute()


def usuario_existe(usuarios, usuario):
    return usuario in usuarios


def senha_correta(usuarios, usuario, senha):
    return usuarios.get(usuario, {}).get("senha") == senha
