import streamlit as st

st.set_page_config(page_title="AI Language Coach")

st.title("🌎 AI Language Coach")
st.write("Aprenda inglês e espanhol com exercícios simples.")

idioma = st.selectbox("Idioma:", ["Inglês", "Espanhol"])
nivel = st.selectbox("Seu nível:", ["Iniciante", "Intermediário", "Avançado"])
objetivo = st.selectbox("Objetivo:", ["Viagem", "Trabalho", "Conversação", "Entrevista"])

frase = st.text_input("Traduza: bom dia")

respostas = {
    "Inglês": "good morning",
    "Espanhol": "buenos días"
}

if st.button("Corrigir"):
    resposta_correta = respostas[idioma]

    if frase.lower().strip() == resposta_correta:
        st.success("✅ Correto! +10 pontos")
    else:
        st.error("❌ Ainda não.")
        st.info(f"Resposta correta: {resposta_correta}")

    st.write(f"📚 Idioma: {idioma}")
    st.write(f"🎯 Objetivo: {objetivo}")
    st.write(f"📈 Nível: {nivel}")
