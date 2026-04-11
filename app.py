import streamlit as st
import pandas as pd
import json
from io import BytesIO
import time
from validators import validar_email, validar_celular
from google_api import salvar_google_sheets, salvar_resumo_google_sheets


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
# CARREGAR JSON
# ==============================
with open("bi_areas.json", "r", encoding="utf-8") as f:
    bi_areas = json.load(f)


# ==============================
# SESSION
# ==============================
if "etapa" not in st.session_state:
    st.session_state.etapa = 1

if "dados_candidato" not in st.session_state:
    st.session_state.dados_candidato = {}

if "habilidades_selecionadas" not in st.session_state:
    st.session_state.habilidades_selecionadas = {}

if "relatorio_gerado" not in st.session_state:
    st.session_state.relatorio_gerado = False


# ==============================
# SCORE
# ==============================
def calcular_score(area, habilidades):
    total = sum(len(v) for v in bi_areas[area].values())
    marcadas = sum(len(v) for v in habilidades.values())
    porcentagem = (marcadas / total) * 100 if total > 0 else 0
    return total, marcadas, porcentagem


# ==============================
# EXCEL
# ==============================
def gerar_excel(area, dados, habilidades):

    detalhes = []
    for categoria, itens in habilidades.items():
        for item in itens:
            detalhes.append({
                "Categoria": categoria,
                "Habilidade": item
            })

    total, marcadas, porcentagem = calcular_score(area, habilidades)

    output = BytesIO()

    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:

        pd.DataFrame(detalhes).to_excel(writer, sheet_name="Detalhes", index=False)

        pd.DataFrame({
            "Nome": [dados.get("nome")],
            "Email": [dados.get("email")],
            "Área": [area],
            "Habilidades Marcadas": [marcadas],
            "Total": [total],
            "Resultado": [f"{porcentagem:.2f}%"],
        }).to_excel(writer, sheet_name="Resumo", index=False)

    return output.getvalue(), total, marcadas, porcentagem


# ==============================
# FUNÇÃO PARA EXTRAIR TEXTO
# ==============================
def get_nome_item(item):
    if isinstance(item, dict):
        return item.get("nome", "")
    return str(item)


# ==============================
# FUNÇÃO PARA RESETAR APP
# ==============================
def resetar_app():
    st.session_state.etapa = 1
    st.session_state.dados_candidato = {}
    st.session_state.habilidades_selecionadas = {}
    st.session_state.relatorio_gerado = False


# ==============================
# TELA 1
# ==============================
if st.session_state.etapa == 1:

    st.title("🚀 Descubra seu nível em Dados")

    with st.form("cadastro"):

        nome = st.text_input("Nome completo*")
        sexo = st.selectbox("Sexo*", ["Masculino", "Feminino", "Outro"])
        email = st.text_input("E-mail*")
        celular = st.text_input("Celular (opcional)")

        submit = st.form_submit_button("✅ Iniciar")

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

                sucesso = salvar_google_sheets(dados)

                if not sucesso:
                    st.error("Erro ao salvar cadastro.")
                    st.stop()

                st.session_state.dados_candidato = dados
                st.session_state.etapa = 2
                st.rerun()


# ==============================
# TELA 2
# ==============================
elif st.session_state.etapa == 2:

    st.title("📊 Avaliação de Habilidades")

    dados = st.session_state.dados_candidato
    st.markdown(f"**Candidato:** {dados.get('nome')}")

    area = st.selectbox("Selecione sua área:", list(bi_areas.keys()))

    if area not in st.session_state.habilidades_selecionadas:
        st.session_state.habilidades_selecionadas = {
            cat: [] for cat in bi_areas[area].keys()
        }

    cols = st.columns(3)

    for i, (cat, itens) in enumerate(bi_areas[area].items()):
        with cols[i]:
            st.subheader(cat)

            for item in itens:

                item_str = get_nome_item(item)

                key = f"{area}_{cat}_{item_str}"
                checked = st.checkbox(item_str, key=key)

                if checked:
                    if item_str not in st.session_state.habilidades_selecionadas[cat]:
                        st.session_state.habilidades_selecionadas[cat].append(item_str)
                else:
                    if item_str in st.session_state.habilidades_selecionadas[cat]:
                        st.session_state.habilidades_selecionadas[cat].remove(item_str)

    if st.button("📥 Enviar"):

        excel, total, marcadas, porcentagem = gerar_excel(
            area,
            st.session_state.dados_candidato,
            st.session_state.habilidades_selecionadas
        )

        todas_habilidades = []
        for categoria, itens in st.session_state.habilidades_selecionadas.items():
            todas_habilidades.extend(itens)

        resumo = {
            "nome": dados.get("nome"),
            "area": area,
            "habilidades_lista": todas_habilidades,
            "total": total
        }

        sucesso = salvar_resumo_google_sheets(resumo)

        if not sucesso:
            st.error("Erro ao salvar resumo.")
            st.stop()

        st.success("Dados enviados com sucesso!")

        st.download_button(
            "⬇️ Baixar Excel",
            excel,
            "relatorio.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        # VOLTA AUTOMATICAMENTE PARA TELA INICIAL
        time.sleep(3)
        resetar_app()
        st.rerun()
