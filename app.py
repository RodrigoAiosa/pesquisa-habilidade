import streamlit as st
import pandas as pd
from io import BytesIO
import hashlib

from validators import validar_email, validar_celular
from google_api import salvar_google_sheets, salvar_resumo_google_sheets, buscar_email_existente


# ==============================
# CONFIG
# ==============================
st.set_page_config(
    page_title="Diagnóstico de Carreira em Dados",
    page_icon="📊",
    layout="centered"
)


# ==============================
# CSS
# ==============================
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# ==============================
# ÁREAS
# ==============================
bi_areas = {
    "Análise de Dados": {
        "📌 Requisitos": ["SQL", "Python", "Excel Avançado", "Power BI"],
        "🚀 Diferenciais": ["Estatística", "Storytelling com Dados", "ETL"],
        "🧠 Soft Skills": ["Comunicação", "Pensamento Analítico"]
    },
    "Business Intelligence (BI)": {
        "📌 Requisitos": ["Power BI", "Modelagem de Dados", "DAX", "SQL"],
        "🚀 Diferenciais": ["Data Warehouse", "ETL", "Governança de Dados"],
        "🧠 Soft Skills": ["Visão de Negócio", "Organização"]
    },
    "Engenharia de Dados": {
        "📌 Requisitos": ["Python", "SQL", "ETL", "Banco de Dados"],
        "🚀 Diferenciais": ["Spark", "Airflow", "Cloud"],
        "🧠 Soft Skills": ["Lógica", "Resolução de Problemas"]
    },
    "Ciência de Dados": {
        "📌 Requisitos": ["Python", "Estatística", "ML"],
        "🚀 Diferenciais": ["Deep Learning", "NLP", "MLOps"],
        "🧠 Soft Skills": ["Curiosidade", "Pensamento Crítico"]
    },
    "Analytics Engineer": {
        "📌 Requisitos": ["SQL", "dbt", "Modelagem"],
        "🚀 Diferenciais": ["Data Warehouse", "Git"],
        "🧠 Soft Skills": ["Organização", "Documentação"]
    }
}


# ==============================
# SESSION STATE
# ==============================
if "etapa" not in st.session_state:
    st.session_state.etapa = 1

if "dados" not in st.session_state:
    st.session_state.dados = {}

if "skills" not in st.session_state:
    st.session_state.skills = {}

if "finalizado" not in st.session_state:
    st.session_state.finalizado = False

if "processando" not in st.session_state:
    st.session_state.processando = False


# ==============================
# SCORE
# ==============================
def calcular_score(area, skills):
    total = sum(len(v) for v in bi_areas[area].values())
    marcadas = sum(len(v) for v in skills.values())
    porcentagem = (marcadas / total) * 100 if total > 0 else 0
    return total, marcadas, porcentagem


# ==============================
# EXCEL
# ==============================
def gerar_excel(area, dados, skills):

    detalhes = []
    for cat, itens in skills.items():
        for item in itens:
            detalhes.append({"Categoria": cat, "Habilidade": item})

    total, marcadas, porcentagem = calcular_score(area, skills)

    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:

        pd.DataFrame(detalhes).to_excel(writer, sheet_name="Detalhes", index=False)

        pd.DataFrame({
            "Nome": [dados["nome"]],
            "Área": [area],
            "Marcadas": [marcadas],
            "Total": [total],
            "Conclusão": [f"{porcentagem:.1f}%"]
        }).to_excel(writer, sheet_name="Resumo", index=False)

    return output.getvalue(), total, marcadas, porcentagem


# ==============================
# TELAS
# ==============================
if st.session_state.etapa == 1:

    st.title("🚀 Diagnóstico de Carreira")

    with st.form("form"):

        nome = st.text_input("Nome")
        sexo = st.selectbox("Sexo", ["Masculino", "Feminino", "Outro"])
        email = st.text_input("Email")
        celular = st.text_input("Celular")

        ok = st.form_submit_button("Iniciar")

        if ok:

            if not validar_email(email):
                st.error("Email inválido")
            else:

                # 🔥 CHECK ANTI DUPLICAÇÃO REAL (EMAIL = CHAVE)
                if buscar_email_existente(email):
                    st.warning("Esse email já foi registrado. Apenas 1 envio permitido.")
                else:

                    st.session_state.dados = {
                        "nome": nome,
                        "sexo": sexo,
                        "email": email,
                        "celular": celular
                    }

                    st.session_state.etapa = 2
                    st.rerun()


elif st.session_state.etapa == 2:

    st.title("📊 Avaliação")

    dados = st.session_state.dados

    area = st.selectbox("Área", list(bi_areas.keys()))

    if area not in st.session_state.skills:
        st.session_state.skills = {k: [] for k in bi_areas[area]}

    cols = st.columns(3)

    for i, (cat, itens) in enumerate(bi_areas[area].items()):
        with cols[i]:
            st.subheader(cat)

            for item in itens:
                key = f"{area}_{cat}_{item}"
                checked = st.checkbox(item, key=key)

                if checked:
                    if item not in st.session_state.skills[cat]:
                        st.session_state.skills[cat].append(item)
                else:
                    if item in st.session_state.skills[cat]:
                        st.session_state.skills[cat].remove(item)

    if st.button("📥 Gerar Relatório") and not st.session_state.finalizado:

        if st.session_state.processando:
            st.stop()

        st.session_state.processando = True

        try:
            excel, total, marcadas, porcentagem = gerar_excel(area, dados, st.session_state.skills)

            resumo = {
                "nome": dados["nome"],
                "email": dados["email"],  # 🔥 chave única
                "area": area,
                "habilidades": marcadas,
                "total": total,
                "conclusao": f"{porcentagem:.1f}%"
            }

            # 🔥 SALVA APENAS 1 LINHA (GARANTIDO NO BACKEND)
            salvar_google_sheets(dados)
            salvar_resumo_google_sheets(resumo)

            st.session_state.finalizado = True

            st.success("Registro salvo com sucesso!")

            st.download_button(
                "Baixar Excel",
                excel,
                "relatorio.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        finally:
            st.session_state.processando = False

        st.rerun()
