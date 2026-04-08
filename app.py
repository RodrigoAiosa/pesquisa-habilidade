import io

output = io.BytesIO()

# -----------------------------
# DADOS DETALHADOS
# -----------------------------
dados = {
    "Nome": st.session_state.nome,
    "Email": st.session_state.email,
    "Celular": st.session_state.celular,
    "Data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "Score Final (%)": round(score_final * 100, 2),
    "Score Requisitos (%)": round(req_score * 100, 2),
    "Score Diferenciais (%)": round(dif_score * 100, 2),
    "Score Soft Skills (%)": round(soft_score * 100, 2),
    "Classificação": classificacao
}

# Respostas individuais
for i, item in enumerate(requisitos):
    dados[f"REQ - {item}"] = "Sim" if req_checks[i] else "Não"

for i, item in enumerate(diferenciais):
    dados[f"DIF - {item}"] = "Sim" if dif_checks[i] else "Não"

for i, item in enumerate(soft_skills):
    dados[f"SOFT - {item}"] = "Sim" if soft_checks[i] else "Não"

df_detalhado = pd.DataFrame([dados])

# -----------------------------
# RESUMO EXECUTIVO
# -----------------------------
resumo = {
    "Indicador": [
        "Nome do Candidato",
        "Score Geral (%)",
        "Aderência Requisitos (%)",
        "Aderência Diferenciais (%)",
        "Aderência Soft Skills (%)",
        "Total Requisitos Atendidos",
        "Total Diferenciais",
        "Total Soft Skills",
        "Classificação Final",
        "Status"
    ],
    "Valor": [
        st.session_state.nome,
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

# -----------------------------
# GERAR EXCEL COM 2 ABAS
# -----------------------------
with pd.ExcelWriter(output, engine="openpyxl") as writer:
    df_detalhado.to_excel(writer, index=False, sheet_name="Dados")
    df_resumo.to_excel(writer, index=False, sheet_name="Resumo")

output.seek(0)

# -----------------------------
# DOWNLOAD
# -----------------------------
file_name = f"avaliacao_{st.session_state.nome.replace(' ', '_')}.xlsx"

st.download_button(
    label="📥 Baixar Relatório Completo",
    data=output,
    file_name=file_name,
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
