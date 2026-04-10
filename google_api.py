import requests

GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycby9qXNnvoJDP6ghOq-z_vnEktGYnQ0cRmocmw7neYG7XCkt9NpMVxy1yntklTXzagTP/exec"


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
        requests.post(GOOGLE_SCRIPT_URL, json=payload, timeout=10)
        return True
    except:
        return False


# ==============================
# RESUMO COM STATUS
# ==============================
def salvar_resumo_google_sheets(resumo: dict):

    habilidades = resumo.get("habilidades_lista", [])

    # lista → string
    habilidades_str = ", ".join(habilidades)

    # contagem
    contagem = len(habilidades)

    # extrair percentual (ex: "88.9%")
    percentual_str = resumo.get("conclusao", "0%").replace("%", "")

    try:
        percentual = float(percentual_str)
    except:
        percentual = 0

    # 🔥 REGRA DE NEGÓCIO
    status = "Apto" if percentual >= 75 else "Não Apto"

    payload = {
        "tipo": "resumo",
        "email": resumo.get("email"),
        "nome": resumo.get("nome"),
        "area": resumo.get("area"),
        "habilidades_marcadas": habilidades_str,
        "contagem_habilidades_marcadas": contagem,
        "total": resumo.get("total"),
        "conclusao_percentual": resumo.get("conclusao"),
        "status": status
    }

    try:
        requests.post(GOOGLE_SCRIPT_URL, json=payload, timeout=10)
        return True
    except:
        return False
