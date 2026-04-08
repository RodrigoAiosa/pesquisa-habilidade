import streamlit as st
import pandas as pd
from datetime import datetime

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(
    page_title="Avaliação de Engenheiro de IA",
    page_icon="🚀",
    layout="wide"
)

# -----------------------------
# CSS
# -----------------------------
def load_css():
    try:
        with open("assets/style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except:
        pass

load_css()

# -----------------------------
# SESSION STATE
# -----------------------------
if "step" not in st.session_state:
    st.session_state.step = 1

# -----------------------------
# DADOS
# -----------------------------
requisitos = [
    "LLMs em produção",
    "Arquitetura de agentes",
    "RAG",
    "Python avançado",
    "APIs REST",
    "Integração de sistemas",
    "Banco de dados",
    "Bancos vetoriais",
    "Git"
]

diferenciais = [
    "Cloud (Azure)",
    "Docker",
    "Observabilidade",
    "Pipelines de dados",
    "RAG em escala"
]

soft_skills = [
    "Pensamento analítico",
    "Traduz negócio",
    "Perfil investigativo",
    "Autonomia",
    "Comunicação"
]

# -----------------------------
# STEP 1 - FORMULÁRIO
# -----------------------------
if st.session_state.step == 1:

    st.markdown("## 🚀 Avaliação de Engenheiro de IA")
    st.markdown("Preencha seus dados para iniciar:")

    with st.form("form_usuario"):
        nome = st.text_input("Nome")
        email = st.text_input("E-mail")
        celular = st.text_input("Celular")

        submitted = st.form_submit_button("Continuar")

        if submitted:
            if nome and email:
                st.session_state.nome = nome
                st.session_state.email = email
                st.session_state.celular = celular
                st.session_state.step = 2
                st.rerun()
            else:
                st.warning("Preencha pelo menos nome e e-mail")

# -----------------------------
# STEP 2 - AVALIAÇÃO
# -----------------------------
elif st.session_state.step == 2:

    st.markdown(f"### 👋 Olá, {st.session_state.nome}")
    st.markdown("Marque suas habilidades:")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### ✅ Requisitos")
        req_checks = [st.checkbox(item, key=f"req_{i}") for i, item in enumerate(requisitos)]

    with col2:
        st.markdown("### 🚀 Diferenciais")
        dif_checks = [st.checkbox(item, key=f"dif_{i}") for i, item in enumerate(diferenciais)]

    with col3:
        st.markdown("### 🧠 Soft Skills")
        soft_checks = [st.checkbox(item, key=f"soft_{i}") for i, item in enumerate(soft_skills)]

    if st.button("📊 Calcular Meu Nível"):

        # -----------------------------
        # SCORE
        # -----------------------------
        req_score = sum(req_checks) / len(requisitos)
        dif_score = sum(dif_checks) / len(diferenciais)
        soft_score = sum(soft_checks) / len(soft_skills)

        score_final = (req_score * 0.6) + (dif_score * 0.25) + (soft_score * 0.15)

        st.progress(score_final)
        st.write(f"### 🎯 Score Final: {score_final*100:.1f}%")

        # -----------------------------
        # CLASSIFICAÇÃO
        # -----------------------------
        if req_score < 0.7:
            classificacao = "Reprovado"
            st.error("❌ Não atende requisitos mínimos")
        elif score_final >= 0.85:
            classificacao = "Forte candidato"
            st.success("🔥 Forte candidato!")
        elif score_final >= 0.7:
            classificacao = "Bom candidato"
            st.warning("👍 Bom candidato")
        else:
            classificacao = "Mediano"
            st.info("🤔 Perfil intermediário")

        # -----------------------------
        # GERAR EXCEL
        # -----------------------------
        dados = {
            "Nome": st.session_state.nome,
            "Email": st.session_state.email,
            "Celular": st.session_state.celular,
            "Data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Score Final (%)": round(score_final * 100, 2),
            "Classificação": classificacao
        }

        # Adicionar respostas
        for i, item in enumerate(requisitos):
            dados[f"REQ - {item}"] = req_checks[i]

        for i, item in enumerate(diferenciais):
            dados[f"DIF - {item}"] = dif_checks[i]

        for i, item in enumerate(soft_skills):
            dados[f"SOFT - {item}"] = soft_checks[i]

        df = pd.DataFrame([dados])

        file_name = f"avaliacao_{st.session_state.nome.replace(' ', '_')}.xlsx"
        df.to_excel(file_name, index=False)

        # -----------------------------
        # DOWNLOAD
        # -----------------------------
        with open(file_name, "rb") as f:
            st.download_button(
                label="📥 Baixar Resultado em Excel",
                data=f,
                file_name=file_name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
