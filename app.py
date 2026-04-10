import streamlit as st
import pandas as pd
from io import BytesIO
from validators import validar_email, validar_celular

# Configuração da página
st.set_page_config(
    page_title="Avaliação de Habilidades em BI",
    page_icon="📊",
    layout="centered"
)

# Carrega CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Dados das áreas de BI (exemplo reduzido)
bi_areas = {
    "Análise de Dados": {
        "📌 Requisitos": ["SQL", "Python", "Power BI"],
        "🚀 Diferenciais": ["Machine Learning", "ETL"],
        "🧠 Soft Skills": ["Comunicação", "Liderança"]
    }
}

# Inicialização da sessão
if 'dados_candidato' not in st.session_state:
    st.session_state.dados_candidato = {}

if 'habilidades_selecionadas' not in st.session_state:
    st.session_state.habilidades_selecionadas = {}

if 'etapa' not in st.session_state:
    st.session_state.etapa = 1

def gerar_excel():
    dados = st.session_state.dados_candidato
    habilidades = st.session_state.habilidades_selecionadas
    
    # Detalhes
    detalhes = []
    for categoria, itens in habilidades.items():
        for item in itens:
            detalhes.append({"Categoria": categoria, "Habilidade": item})
    
    # Resumo
    total = sum(len(v) for v in bi_areas[st.session_state.area_selecionada].values())
    marcadas = sum(len(v) for v in habilidades.values())
    porcentagem = (marcadas / total) * 100
    
    # Criar Excel
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        pd.DataFrame(detalhes).to_excel(writer, sheet_name='Detalhes', index=False)
        pd.DataFrame({
            "Nome": [dados["nome"]],
            "Área": [st.session_state.area_selecionada],
            "Habilidades Marcadas": [marcadas],
            "Total": [total],
            "Conclusão": [f"{porcentagem:.1f}%"]
        }).to_excel(writer, sheet_name='Resumo', index=False)
    
    return output.getvalue()

# Tela 1 - Cadastro
if st.session_state.etapa == 1:
    st.title("📝 Cadastro")
    
    with st.form("cadastro"):
        nome = st.text_input("Nome completo*")
        sexo = st.selectbox("Sexo*", ["Masculino", "Feminino", "Outro"])
        email = st.text_input("E-mail*")
        celular = st.text_input("Celular (opcional)", placeholder="(99) 99999-9999")
        
        if st.form_submit_button("Continuar"):
            erros = []
            if not nome.strip(): erros.append("Nome obrigatório")
            if not validar_email(email): erros.append("E-mail inválido")
            if celular and not validar_celular(celular): erros.append("Celular inválido")
            
            if erros:
                for e in erros: st.error(e)
            else:
                st.session_state.dados_candidato = {
                    "nome": nome, "sexo": sexo,
                    "email": email, "celular": celular
                }
                st.session_state.etapa = 2
                st.rerun()

# Tela 2 - Habilidades
elif st.session_state.etapa == 2:
    st.title("📊 Habilidades")
    st.markdown(f"Candidato: **{st.session_state.dados_candidato['nome']}**")
    
    area = st.selectbox(
        "Selecione sua área:",
        list(bi_areas.keys()),
        key="area_selecionada"
    )
    
    # Inicializa seleções
    if area not in st.session_state.habilidades_selecionadas:
        st.session_state.habilidades_selecionadas = {cat: [] for cat in bi_areas[area].keys()}
    
    # Mostra checkboxes
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
    
    # Botões
    if st.button("Voltar"):
        st.session_state.etapa = 1
        st.rerun()
    
    if st.button("Gerar Relatório"):
        excel = gerar_excel()
        st.download_button(
            "⬇️ Baixar Excel",
            excel,
            "relatorio_habilidades.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
