import requests

# URL ATUALIZADA com seu novo deployment
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzVNEOwWaiO7NozJ87VN_Yc_T6ApQFozaG8IHnv6zUmIZpkefGb82UMqYIjjEtHGFac5g/exec"


# ==============================
# CADASTRO
# ==============================
def salvar_google_sheets(dados: dict):
    payload = {
        "tipo": "cadastro",
        "nome": dados.get("nome"),
        "sexo": dados.get("sexo"),
        "email": dados.get("email"),
        "celular": dados.get("celular")
    }

    try:
        response = requests.post(GOOGLE_SCRIPT_URL, json=payload, timeout=10)
        print(f"Cadastro - Status: {response.status_code}, Resposta: {response.text}")
        return True
    except Exception as e:
        print(f"Erro no cadastro: {e}")
        return False


# ==============================
# RESUMO
# ==============================
def salvar_resumo_google_sheets(resumo: dict):
    habilidades = resumo.get("habilidades_lista", [])
    habilidades_str = ", ".join(habilidades)
    contagem = len(habilidades)
    total = resumo.get("total", 0)

    percentual = 0
    if total > 0:
        percentual = (contagem / total) * 100

    percentual_formatado = f"{percentual:.2f}%".replace(".", ",")
    conclusao = "Apto" if percentual >= 75 else "Não Apto"

    payload = {
        "tipo": "resumo",
        "nome": resumo.get("nome"),
        "area": resumo.get("area"),
        "habilidades_marcadas": habilidades_str,
        "contagem_habilidades_marcada": contagem,
        "total_habilidades": total,
        "Resultado": percentual_formatado,
        "conclusao": conclusao
    }

    print(f"Enviando resumo: {payload}")  # Debug

    try:
        response = requests.post(GOOGLE_SCRIPT_URL, json=payload, timeout=10)
        print(f"Resumo - Status: {response.status_code}, Resposta: {response.text}")
        return True
    except Exception as e:
        print(f"Erro no resumo: {e}")
        return False
