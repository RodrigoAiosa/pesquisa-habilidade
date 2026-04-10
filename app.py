import streamlit as st
import pandas as pd
import json
from io import BytesIO
from validators import validar_email, validar_celular

# ==============================
# CONFIG
# ==============================
st.set_page_config(
    page_title="Diagnóstico de Carreira em Dados",
    page_icon="🚀",
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
# SESSÃO
# ==============================
if "dados_candidato" not in st.session_state:
    st.session_state.dados_candidato = {}

if "habilidades_selecionadas" not in st.session_state:
    st.session_state.habilidades_selecionadas = {}

if "etapa" not in st.session_state:
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


def analisar_resultado(area, habilidades):
    faltantes_alta = []
    faltantes_media = []

    for categoria, itens in bi_areas[area].items():
        for item in itens:
            if item["nome"] not in habilidades.get(categoria, []):
                if item["prioridade"] == "alta":
                    faltantes_alta.append(item["nome"])
                else:
                    faltantes_media.append(item["nome"])

    return faltantes_alta, faltantes_media


def gerar_excel(area, porcentagem, nivel, faltantes_alta, faltantes_media):
    dados = st.session_state.dados_candidato

    output = BytesIO()

    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:

        pd.DataFrame({
            "Nome": [dados["nome"]],
            "Área": [area],
            "Score (%)": [f"{porcentagem:.1f}%"],
            "Nível": [nivel]
        }).to_excel(writer, sheet_name="Resumo", index=False)

        pd.DataFrame({
            "Prioridade Alta": faltantes_alta
        }).to_excel(writer, sheet_name="Focar Agora", index=False)

        pd.DataFrame({
            "Prioridade Média": faltantes_media
        }).to_excel(writer, sheet_name="Próximos Passos", index=False)

    return output.getvalue()


# ==============================
# TELA 1 (LANDING)
# ==============================
if st.session_state.etapa == 1:

    st.markdown("""
    <h1 style='text-align:center;'>🚀 Descubra seu nível em Dados</h1>
    <p style='text-align:center; color:#ccc;'>
    Receba um diagnóstico completo da sua carreira em Data Analytics, BI, Engenharia ou Ciência de Dados.
    </p>
    """, unsafe_allow_html=True)

    st.title("📝 Começar avaliação")

    with st.form("cadastro"):
        nome = st.text_input("Nome completo*")
        sexo = st.selectbox("Sexo*", ["Masculino", "Feminino", "Outro"])
        email = st.text_input("E-mail*")
        celular = st.text_input("Celular (opcional)")

        if st.form_submit_button("🚀 Iniciar diagnóstico"):
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
# TELA 2 (AVALIAÇÃO)
# ==============================
elif st.session_state.etapa == 2:

    st.title("📊 Avaliação de Habilidades")
    st.markdown(f"👤 **{st.session_state.dados_candidato['nome']}**")

    area = st.selectbox("Escolha sua área:", list(bi_areas.keys()))

    # Reset ao trocar área
    if "area_atual" not in st.session_state or st.session_state.area_atual != area:
        st.session_state.area_atual = area
        st.session_state.habilidades_selecionadas = {
            cat: [] for cat in bi_areas[area].keys()
        }

    cols = st.columns(3)

    categorias_map = {
        "requisitos": "📌 Requisitos",
        "diferenciais": "🚀 Diferenciais",
        "soft_skills": "🧠 Soft Skills"
    }

    for i, (cat_json, itens) in enumerate(bi_areas[area].items()):
        cat_nome = categorias_map.get(cat_json, cat_json)

        with cols[i]:
            st.subheader(cat_nome)

            for item in itens:
                nome_item = item["nome"]
                key = f"{area}_{cat_json}_{nome_item}"

                selecionado = st.checkbox(nome_item, key=key)

                if selecionado:
                    if nome_item not in st.session_state.habilidades_selecionadas[cat_json]:
                        st.session_state.habilidades_selecionadas[cat_json].append(nome_item)
                else:
                    if nome_item in st.session_state.habilidades_selecionadas[cat_json]:
                        st.session_state.habilidades_selecionadas[cat_json].remove(nome_item)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅️ Voltar"):
            st.session_state.etapa = 1
            st.rerun()

    with col2:
        if st.button("🚀 Ver Resultado"):

            total = sum(len(v) for v in bi_areas[area].values())
            marcadas = sum(len(v) for v in st.session_state.habilidades_selecionadas.values())
            porcentagem = (marcadas / total) * 100

            nivel = calcular_nivel(porcentagem)

            faltantes_alta, faltantes_media = analisar_resultado(
                area,
                st.session_state.habilidades_selecionadas
            )

            # ======================
            # RESULTADO
            # ======================
            st.success(f"🎯 Seu nível: **{nivel}**")
            st.progress(int(porcentagem))

            st.markdown("### 🚧 O que você precisa aprender AGORA:")
            for item in faltantes_alta[:5]:
                st.write(f"• {item}")

            st.markdown("### 📈 Próximos passos:")
            for item in faltantes_media[:5]:
                st.write(f"• {item}")

            # CTA (Landing)
            st.markdown("""
            ---
            ### 🚀 Quer acelerar sua carreira em dados?

            Receba um plano completo com:
            ✔ trilha personalizada  
            ✔ roadmap de estudos  
            ✔ skills mais valorizadas pelo mercado  

            👉 Em breve disponível
            """)

            # Excel
            excel = gerar_excel(area, porcentagem, nivel, faltantes_alta, faltantes_media)

            st.download_button(
                "⬇️ Baixar diagnóstico em Excel",
                excel,
                "diagnostico_dados.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
