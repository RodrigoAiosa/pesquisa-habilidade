import streamlit as st
import pandas as pd
from io import BytesIO
from validators import validar_email, validar_celular

# ==============================
# CONFIGURAÇÃO DA PÁGINA
# ==============================
st.set_page_config(
    page_title="Avaliação de Carreira em Dados",
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
# SESSÃO
# ==============================
if 'dados_candidato' not in st.session_state:
    st.session_state.dados_candidato = {}

if 'habilidades_selecionadas' not in st.session_state:
    st.session_state.habilidades_selecionadas = {}

if 'etapa' not in st.session_state:
    st.session_state.etapa = 1

# ==============================
# FUNÇÕES
# ==============================
def calcular_nivel(porcentagem):
    if porcentagem < 40:
        return "Júnior"
    elif porcentagem < 70:
        return "Pleno"
    else:
        return "Sênior"


def gerar_excel():
    dados = st.session_state.dados_candidato
    habilidades = st.session_state.habilidades_selecionadas
    
    detalhes = []
    for categoria, itens in habilidades.items():
        for item in itens:
            detalhes.append({"Categoria": categoria, "Habilidade": item})
    
    total = sum(len(v) for v in bi_areas[st.session_state.area_selecionada].values())
    marcadas = sum(len(v) for v in habilidades.values())
    porcentagem = (marcadas / total) * 100
    nivel = calcular_nivel(porcentagem)
    
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        pd.DataFrame(detalhes).to_excel(writer, sheet_name='Detalhes', index=False)
        
        pd.DataFrame({
            "Nome": [dados["nome"]],
            "Área": [st.session_state.area_selecionada],
            "Habilidades Marcadas": [marcadas],
            "Total": [total],
            "Conclusão (%)": [f"{porcentagem:.1f}%"],
            "Nível": [nivel]
        }).to_excel(writer, sheet_name='Resumo', index=False)
    
    return output.getvalue(), porcentagem, nivel


# ==============================
# TELA 1 - CADASTRO
# ==============================
if st.session_state.etapa == 1:

    st.markdown("""
    <h1 style='text-align: center;'>🚀 Avaliação de Carreira em Dados</h1>
    <p style='text-align: center; color: #ccc;'>
    Descubra seu nível em Data Analytics, BI e Engenharia de Dados em poucos minutos.
    </p>
    """, unsafe_allow_html=True)

    st.title("📝 Cadastro")
    
    with st.form("cadastro"):
        nome = st.text_input("Nome completo*")
        sexo = st.selectbox("Sexo*", ["Masculino", "Feminino", "Outro"])
        email = st.text_input("E-mail*")
        celular = st.text_input("Celular (opcional)", placeholder="(99) 99999-9999")
        
        if st.form_submit_button("Continuar"):
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
                st.session_state.dados_candidato = {
                    "nome": nome,
                    "sexo": sexo,
                    "email": email,
                    "celular": celular
                }
                st.session_state.etapa = 2
                st.rerun()


# ==============================
# TELA 2 - HABILIDADES
# ==============================
elif st.session_state.etapa == 2:

    st.title("📊 Avaliação de Habilidades")
    st.markdown(f"Candidato: **{st.session_state.dados_candidato['nome']}**")
    
    area = st.selectbox(
        "Selecione sua área:",
        list(bi_areas.keys()),
        key="area_selecionada"
    )
    
    # Inicializa seleção corretamente
    if "area_atual" not in st.session_state or st.session_state.area_atual != area:
        st.session_state.area_atual = area
        st.session_state.habilidades_selecionadas = {
            cat: [] for cat in bi_areas[area].keys()
        }
    
    # Layout colunas
    cols = st.columns(3)
    
    for i, (cat, itens) in enumerate(bi_areas[area].items()):
        with cols[i]:
            st.subheader(cat)
            
            for item in itens:
                key = f"{area}_{cat}_{item}"
                
                selecionado = st.checkbox(item, key=key)
                
                if selecionado:
                    if item not in st.session_state.habilidades_selecionadas[cat]:
                        st.session_state.habilidades_selecionadas[cat].append(item)
                else:
                    if item in st.session_state.habilidades_selecionadas[cat]:
                        st.session_state.habilidades_selecionadas[cat].remove(item)
    
    # Botões
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("⬅️ Voltar"):
            st.session_state.etapa = 1
            st.rerun()
    
    with col2:
        if st.button("🚀 Gerar Relatório"):
            excel, porcentagem, nivel = gerar_excel()
            
            st.success(f"🎯 Nível identificado: **{nivel}**")
            st.progress(int(porcentagem))
            
            st.download_button(
                "⬇️ Baixar Excel",
                excel,
                "relatorio_habilidades.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
