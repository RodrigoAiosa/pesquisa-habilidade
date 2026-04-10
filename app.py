import streamlit as st
import pandas as pd
from io import BytesIO

# Dados das áreas de BI
bi_areas = {
    "Análise de Dados": {
        "📌 Requisitos": [
            "SQL avançado",
            "Python (Pandas, NumPy)",
            "Visualização de dados (Power BI, Tableau)",
            "Estatística descritiva"
        ],
        "🚀 Diferenciais": [
            "Machine Learning básico",
            "ETL/ELT (Apache Airflow)",
            "Cloud (AWS Redshift, BigQuery)"
        ],
        "🧠 Soft Skills": [
            "Comunicação clara de insights",
            "Pensamento analítico",
            "Adaptabilidade"
        ]
    },
    "Engenharia de Dados": {
        "📌 Requisitos": [
            "Python/Java/Scala",
            "SQL e bancos de dados (PostgreSQL, MongoDB)",
            "Arquitetura de pipelines (ETL/ELT)"
        ],
        "🚀 Diferenciais": [
            "Streaming de dados (Kafka, Spark Streaming)",
            "Infraestrutura como código (Terraform)",
            "Orquestração (Airflow, Prefect)"
        ],
        "🧠 Soft Skills": [
            "Resolução de problemas complexos",
            "Atenção a detalhes",
            "Colaboração com times multidisciplinares"
        ]
    },
    "Ciência de Dados": {
        "📌 Requisitos": [
            "Python/R (Scikit-learn, TensorFlow)",
            "Estatística inferencial",
            "Machine Learning"
        ],
        "🚀 Diferenciais": [
            "Deep Learning (PyTorch, Keras)",
            "NLP ou Visão Computacional",
            "Deploy de modelos (MLflow, Docker)"
        ],
        "🧠 Soft Skills": [
            "Curiosidade científica",
            "Capacidade de explicar modelos",
            "Resiliência"
        ]
    },
    "Business Intelligence (BI)": {
        "📌 Requisitos": [
            "Power BI/Tableau",
            "SQL intermediário",
            "Modelagem dimensional (Star Schema)"
        ],
        "🚀 Diferenciais": [
            "DAX avançado",
            "Automação de relatórios (Python)",
            "Integração com APIs"
        ],
        "🧠 Soft Skills": [
            "Orientação a negócios",
            "Storytelling com dados",
            "Empatia com usuários"
        ]
    },
    "Governança de Dados": {
        "📌 Requisitos": [
            "LGPD/Compliance",
            "Qualidade e catalogação de dados",
            "Ferramentas (Collibra, Alation)"
        ],
        "🚀 Diferenciais": [
            "MDM (Master Data Management)",
            "Linha de dados (Data Lineage)",
            "Metadados"
        ],
        "🧠 Soft Skills": [
            "Visão estratégica",
            "Habilidade de negociação",
            "Liderança"
        ]
    }
}

# Configuração do App
st.set_page_config(
    page_title="Avaliação de Habilidades em BI",
    page_icon="📊",
    layout="centered"
)

# Inicialização da sessão
if 'dados_candidato' not in st.session_state:
    st.session_state.dados_candidato = {}

if 'habilidades_selecionadas' not in st.session_state:
    st.session_state.habilidades_selecionadas = {}

# Função para gerar Excel
def gerar_excel():
    # Dados do candidato
    dados_candidato = st.session_state.dados_candidato
    
    # Habilidades selecionadas
    habilidades = st.session_state.habilidades_selecionadas
    
    # Criação do DataFrame de Detalhes
    detalhes = []
    for categoria, itens in habilidades.items():
        for item in itens:
            detalhes.append({
                "Categoria": categoria,
                "Habilidade": item
            })
    df_detalhes = pd.DataFrame(detalhes)
    
    # Criação do DataFrame de Resumo
    total_habilidades = sum(len(itens) for itens in bi_areas[st.session_state.area_selecionada].values())
    habilidades_marcadas = sum(len(itens) for itens in habilidades.values())
    porcentagem = (habilidades_marcadas / total_habilidades) * 100
    
    resumo = {
        "Nome": [dados_candidato["nome"]],
        "Área": [st.session_state.area_selecionada],
        "Habilidades Marcadas": [habilidades_marcadas],
        "Total de Habilidades": [total_habilidades],
        "Porcentagem": [f"{porcentagem:.2f}%"]
    }
    df_resumo = pd.DataFrame(resumo)
    
    # Salvando em Excel
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_detalhes.to_excel(writer, sheet_name='Detalhes', index=False)
        df_resumo.to_excel(writer, sheet_name='Resumo', index=False)
    
    return output.getvalue()

# Tela 1: Cadastro do Candidato
if 'etapa' not in st.session_state or st.session_state.etapa == 1:
    st.title("📝 Cadastro do Candidato")
    
    with st.form("form_cadastro"):
        nome = st.text_input("Nome completo:")
        sexo = st.selectbox("Sexo:", ["Masculino", "Feminino", "Outro"])
        email = st.text_input("E-mail:")
        celular = st.text_input("Celular:")
        
        if st.form_submit_button("Próximo"):
            st.session_state.dados_candidato = {
                "nome": nome,
                "sexo": sexo,
                "email": email,
                "celular": celular
            }
            st.session_state.etapa = 2
            st.rerun()

# Tela 2: Seleção de Habilidades
elif st.session_state.etapa == 2:
    st.title("📊 Habilidades em BI")
    st.markdown(f"**Candidato:** {st.session_state.dados_candidato['nome']}")
    
    area_selecionada = st.selectbox(
        "Selecione uma área para ver requisitos, diferenciais e soft skills:",
        list(bi_areas.keys()),
        key="area_selecionada"
    )
    
    st.subheader(f"🔍 {area_selecionada}")
    
    # Inicializa habilidades selecionadas
    if area_selecionada not in st.session_state.habilidades_selecionadas:
        st.session_state.habilidades_selecionadas = {categoria: [] for categoria in bi_areas[area_selecionada].keys()}
    
    # Exibe checkboxes para cada habilidade
    cols = st.columns(3)
    for i, (categoria, itens) in enumerate(bi_areas[area_selecionada].items()):
        with cols[i]:
            st.markdown(f"**{categoria}**")
            for item in itens:
                if st.checkbox(item, key=f"{categoria}_{item}"):
                    if item not in st.session_state.habilidades_selecionadas[categoria]:
                        st.session_state.habilidades_selecionadas[categoria].append(item)
                else:
                    if item in st.session_state.habilidades_selecionadas[categoria]:
                        st.session_state.habilidades_selecionadas[categoria].remove(item)
    
    # Botão para salvar em Excel
    if st.button("Salvar em Excel"):
        excel_data = gerar_excel()
        st.download_button(
            label="Baixar Excel",
            data=excel_data,
            file_name=f"habilidades_bi_{st.session_state.dados_candidato['nome']}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    if st.button("Voltar"):
        st.session_state.etapa = 1
        st.rerun()
