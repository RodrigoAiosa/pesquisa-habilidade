import streamlit as st
import pandas as pd
from datetime import datetime
import io
from pathlib import Path

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(
    page_title="Avaliação de Engenheiro de IA",
    page_icon="🚀",
    layout="wide"
)

# -----------------------------
# CSS (SAFE LOAD)
# -----------------------------
def load_css():
    try:
        css_path = Path(__file__).parent / "assets" / "style.css"
        if css_path.exists():
            with open(css_path) as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except:
        pass

load_css()

# -----------------------------
# SESSION STATE (SAFE INIT)
# -----------------------------
if "step" not in st.session_state:
    st.session_state.step = 1

if "nome" not in st.session_state:
    st.session_state.nome = ""

if "email" not in st.session_state:
    st.session_state.email = ""

if "celular" not in st.session_state:
    st.session_state.celular = ""

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

    st.markdown(f"### 👋 Olá, {st.session_state.get('nome', '')}")
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

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("📊 Calcular Meu Nível"):

        # Segurança extra
        if not st.session_state.get("nome"):
            st.error("Preencha seus dados antes de continuar")
            st.stop()

        # -----------------------------
        # SCORE
        # -----------------------------
        req_score = sum(req_checks) / len(requisitos)
        dif_score = sum(dif_checks) / len(diferenciais)
        soft_score = sum(soft_checks) / len(soft_skills)

        score_final = (req_score * 0.6) + (dif_score * 0.25) + (soft_score * 0.15)

        # -----------------------------
        # RESULTADO UI
        # -----------------------------
        st.progress(score_final)
        st.write(f"### 🎯 Score Final: {score_final*100:.1f}%")

        colA, colB, colC = st.columns(3)
        colA.metric("Requisitos", f"{req_score*100:.1f}%")
        colB.metric("Diferenciais", f"{dif_score*100:.1f}%")
        colC.metric("Soft Skills", f"{soft_score*100:.1f}%")

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
        # EXCEL (2 ABAS)
        # -----------------------------
        output = io.BytesIO()

        dados = {
            "Nome": st.session_state.get("nome"),
            "Email": st.session_state.get("email"),
            "Celular": st.session_state.get("celular"),
            "Data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Score Final (%)": round(score_final * 100, 2),
            "Score Requisitos (%)": round(req_score * 100, 2),
            "Score Diferenciais (%)": round(dif_score * 100, 2),
            "Score Soft Skills (%)": round(soft_score * 100, 2),
            "Classificação": classificacao
        }

        # respostas
        for i, item in enumerate(requisitos):
            dados[f"REQ - {item}"] = "Sim" if req_checks[i] else "Não"

        for i, item in enumerate(diferenciais):
            dados[f"DIF - {item}"] = "Sim" if dif_checks[i] else "Não"

        for i, item in enumerate(soft_skills):
            dados[f"SOFT - {item}"] = "Sim" if soft_checks[i] else "Não"

        df_detalhado = pd.DataFrame([dados])

        resumo = {
            "Indicador": [
                "Nome do Candidato",
                "Score Geral (%)",
                "Aderência Requisitos (%)",
                "Aderência Diferenciais (%)",
                "Aderência Soft Skills (%)",
                "Total Requisitos",
                "Total Diferenciais",
                "Total Soft Skills",
                "Classificação Final",
                "Status"
            ],
            "Valor": [
                st.session_state.get("nome"),
                f"{score_final*100:.1f}%",
                f"{req_score*100:.1f}%",
                f"{dif_score*100:.1f}%",
                f"{soft_score*100:.1f}%",
                f"{sum(req_checks)}/{len(requisitos)}",
                f"{sum(dif_checks)}/{len(diferenciais)}",
                f"{sum(soft_checks)}/{len(soft_skills)}",
                classificacao,
                "Aprovado" if score_final >= 0.7 and req_score >= 0.7 else "Reprovado"
            ]
        }

        df_resumo = pd.DataFrame(resumo)

        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df_detalhado.to_excel(writer, index=False, sheet_name="Dados")
            df_resumo.to_excel(writer, index=False, sheet_name="Resumo")

        output.seek(0)

        file_name = f"avaliacao_{st.session_state.get('nome').replace(' ', '_')}.xlsx"

        st.download_button(
            label="📥 Baixar Relatório Completo",
            data=output,
            file_name=file_name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("""
<hr>
<div style="text-align: center; color: gray; font-size: 13px;">
Avaliação técnica • Desenvolvido com Streamlit
</div>
""", unsafe_allow_html=True)
