import streamlit as st

# Dados das áreas de BI (focados no essencial)
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
    page_title="Habilidades em BI",
    page_icon="📊",
    layout="centered"
)

# Título
st.title("📊 Principais Áreas de BI")
st.markdown("Selecione uma área para ver **requisitos**, **diferenciais** e **soft skills**:")

# Seleção da área
area = st.selectbox("", list(bi_areas.keys()))

# Exibição dos cards
if area:
    st.subheader(f"🔍 {area}")
    
    cols = st.columns(3)
    
    for i, (categoria, itens) in enumerate(bi_areas[area].items()):
        with cols[i]:
            st.markdown(f"**{categoria}**")
            for item in itens:
                st.markdown(f"- {item}")

# Rodapé
st.markdown("---")
st.caption("Projeto desenvolvido por Rodrigo Aiosa | Pesquisa de Habilidades em BI")
