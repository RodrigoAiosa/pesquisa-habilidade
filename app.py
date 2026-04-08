import streamlit as st

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(
    page_title="Avaliação de Engenheiro de IA",
    page_icon="🚀",
    layout="wide"
)

# -----------------------------
# LOAD CSS
# -----------------------------
def load_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# -----------------------------
# HEADER (Landing)
# -----------------------------
st.markdown("""
    <div style="text-align: center; padding: 40px 20px;">
        <h1>🚀 Avaliação de Engenheiro de IA</h1>
        <p>Descubra seu nível técnico com base em requisitos reais de mercado</p>
    </div>
""", unsafe_allow_html=True)

# -----------------------------
# DADOS
# -----------------------------
requisitos = [
    "Experiência com LLMs em produção",
    "Arquitetura de agentes (multiagentes, CrewAI ou similares)",
    "Experiência com RAG",
    "Python avançado (POO, clean code)",
    "APIs REST",
    "Integração de sistemas",
    "Banco de dados (SQL/NoSQL)",
    "Bancos vetoriais (Pinecone, FAISS, etc.)",
    "Git e versionamento"
]

diferenciais = [
    "Deploy em cloud (Azure ou similar)",
    "Docker e conteinerização",
    "Observabilidade (logs, tracing, monitoramento)",
    "Pipelines de dados (Airflow, Databricks)",
    "RAG em larga escala"
]

soft_skills = [
    "Pensamento analítico",
    "Traduz negócio em solução técnica",
    "Perfil investigativo",
    "Autonomia",
    "Boa comunicação"
]

# -----------------------------
# LAYOUT EM COLUNAS
# -----------------------------
col1, col2, col3 = st.columns(3)

# -----------------------------
# REQUISITOS
# -----------------------------
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("✅ Requisitos Obrigatórios")
    req_checks = [st.checkbox(item, key=f"req_{i}") for i, item in enumerate(requisitos)]
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# DIFERENCIAIS
# -----------------------------
with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🚀 Diferenciais")
    dif_checks = [st.checkbox(item, key=f"dif_{i}") for i, item in enumerate(diferenciais)]
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# SOFT SKILLS
# -----------------------------
with col3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🧠 Soft Skills")
    soft_checks = [st.checkbox(item, key=f"soft_{i}") for i, item in enumerate(soft_skills)]
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# BOTÃO
# -----------------------------
st.markdown("<br>", unsafe_allow_html=True)

if st.button("📊 Calcular Meu Nível"):

    # -----------------------------
    # SCORE
    # -----------------------------
    req_score = sum(req_checks) / len(requisitos)
    dif_score = sum(dif_checks) / len(diferenciais)
    soft_score = sum(soft_checks) / len(soft_skills)

    score_final = (req_score * 0.6) + (dif_score * 0.25) + (soft_score * 0.15)

    # -----------------------------
    # RESULTADO
    # -----------------------------
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📈 Resultado da Avaliação")

    st.progress(score_final)

    colA, colB, colC = st.columns(3)

    colA.metric("Requisitos", f"{req_score*100:.1f}%")
    colB.metric("Diferenciais", f"{dif_score*100:.1f}%")
    colC.metric("Soft Skills", f"{soft_score*100:.1f}%")

    st.markdown(f"### 🎯 Score Final: {score_final*100:.1f}%")

    # -----------------------------
    # CLASSIFICAÇÃO
    # -----------------------------
    if req_score < 0.7:
        st.error("❌ Você ainda não atende aos requisitos mínimos.")
    elif score_final >= 0.85:
        st.success("🔥 Forte candidato! Alto nível técnico.")
    elif score_final >= 0.7:
        st.warning("👍 Bom candidato, com potencial.")
    else:
        st.info("🤔 Perfil intermediário, pode evoluir mais.")

    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("""
    <hr>
    <div style="text-align: center; font-size: 14px; color: gray;">
        Projeto de avaliação técnica • Desenvolvido com Streamlit
    </div>
""", unsafe_allow_html=True)
