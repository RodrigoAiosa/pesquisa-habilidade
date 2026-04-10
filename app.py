import streamlit as st
import pandas as pd
from io import BytesIO

from validators import validar_email, validar_celular
from google_api import salvar_google_sheets  # 🔥 nova integração

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
# ÁREAS DE DADOS
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
        "🚀 Diferenciais": ["Spark", "Airflow", "Cloud (AWS/GCP/Azure)"],
        "🧠 Soft Skills": ["Raciocínio Lógico", "Resolução de Problemas"]
    },
    "Ciência de Dados": {
        "📌 Requisitos": ["Python", "Estatística", "Machine Learning"],
        "🚀 Diferenciais": ["Deep Learning", "NLP", "MLOps"],
        "🧠 Soft Skills": ["Curiosidade", "Pensamento Crítico"]
    },
    "Analytics Engineer": {
        "📌 Requisitos": ["SQL", "dbt", "Modelagem de Dados"],
        "🚀 Diferenciais": ["Data Warehouse", "Versionamento (Git)"],
        "🧠 Soft Skills": ["Organização", "Documentação"]
    }
}

# ==============================
# SESSION STATE
# ==============================
if "etapa" not in st.session_state:
    st.session_state.etapa = 1

if "dados_candidato" not in st.session_state:
    st.session_state.dados_candidato = {}

if "habilidades_selecionadas" not in st.session_state:
    st.session_state.habilidades_selecionadas = {}

# ==============================
# FUNÇÃO EXCEL
# ==============================
def gerar_excel():
    dados = st.session_state.dados_candidato
    habilidades = st.session_state.habilidades_selecionadas

    detalhes = []
    for categoria, itens in habilidades.items():
        for item in itens:
            detalhes.append({
                "Categoria": categoria,
                "Habilidade": item
            })

    total = sum(len(v) for v in bi_areas[st.session_state.area_selecionada].values())
    marcadas = sum(len(v) for v in habilidades.values())
    porcentagem = (marcadas / total) * 100 if total > 0 else 0

    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        pd.DataFrame(detalhes).to_excel(writer, sheet_name="Detalhes", index=False)

        pd.DataFrame({
            "Nome": [dados.get("nome")],
            "Área": [st.session_state.area_selecionada],
            "Habilidades Marcadas": [marcadas],
            "Total": [total],
            "Conclusão": [f"{porcentagem:.1f}%"]
        }).to_excel(writer, sheet_name="Resumo", index=False)

    return output.getvalue()

# ==============================
# TELA 1 - FORMULÁRIO
# ==============================
if st.session_state.etapa == 1:

    st.title("🚀 Descubra seu nível em Dados")
    st.markdown("Receba um diagnóstico completo da sua carreira em Data Analytics, BI, Engenharia ou Ciência de Dados.")

    with st.form("cadastro"):
        nome = st.text_input("Nome completo*")
        sexo = st.selectbox("Sexo*", ["Masculino", "Feminino", "Outro"])
        email = st.text_input("E-mail*")
        celular = st.text_input("Celular (opcional)")

        submit = st.form_submit_button("🚀 Iniciar diagnóstico")

        if submit:

            erros = []

            if not nome.strip():
                erros.append("Nome obrigatório")

            if not validar_email(email):
                erros.append("E-mail inválido")

            if celular and not validar_celular(celular):
                erros.append("Celular inválido")

            if erros:
                for e in erros:
                    st.error(e)
            else:
                dados = {
                    "nome": nome,
                    "sexo": sexo,
                    "email": email,
                    "celular": celular
                }

                # 🔥 SALVA NO GOOGLE SHEETS (via módulo separado)
                salvar_google_sheets(dados)

                st.session_state.dados_candidato = dados
                st.session_state.etapa = 2
                st.rerun()

# ==============================
# TELA 2 - HABILIDADES
# ==============================
elif st.session_state.etapa == 2:

    st.title("📊 Avaliação de Habilidades")
    st.markdown(f"**Candidato:** {st.session_state.dados_candidato.get('nome', '')}")

    area = st.selectbox(
        "Selecione sua área:",
        list(bi_areas.keys()),
        key="area_selecionada"
    )

    if area not in st.session_state.habilidades_selecionadas:
        st.session_state.habilidades_selecionadas = {
            cat: [] for cat in bi_areas[area].keys()
        }

    cols = st.columns(3)

    for i, (cat, itens) in enumerate(bi_areas[area].items()):
        with cols[i]:
            st.subheader(cat)

            for item in itens:
                key = f"{cat}_{item}"

                if st.checkbox(item, key=key):
                    if item not in st.session_state.habilidades_selecionadas[cat]:
                        st.session_state.habilidades_selecionadas[cat].append(item)
                else:
                    if item in st.session_state.habilidades_selecionadas[cat]:
                        st.session_state.habilidades_selecionadas[cat].remove(item)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅️ Voltar"):
            st.session_state.etapa = 1
            st.rerun()

    with col2:
        if st.button("📥 Gerar Relatório"):
            excel = gerar_excel()

            st.download_button(
                "⬇️ Baixar Excel",
                excel,
                "relatorio_habilidades.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
