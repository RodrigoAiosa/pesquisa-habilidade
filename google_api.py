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
# RESUMO CORRIGIDO
# ==============================
def salvar_resumo_google_sheets(resumo: dict):

    habilidades = resumo.get("habilidades_lista", [])

    habilidades_str = ", ".join(habilidades)
    contagem = len(habilidades)

    # percentual (ex: "88.9%")
    percentual_str = resumo.get("conclusao", "0%").replace("%", "")

    try:
        percentual = float(percentual_str)
    except:
        percentual = 0

    # 🔥 regra final
    conclusao = "Apto" if percentual >= 75 else "Não Apto"

    payload = {
        "tipo": "resumo",
        "nome": resumo.get("nome"),
        "area": resumo.get("area"),
        "habilidades_marcadas": habilidades_str,
        "contagem_habilidades_marcada": contagem,
        "total_habilidade": contagem,              
        "conclusao": resumo.get("total")                     
    }

    try:
        requests.post(GOOGLE_SCRIPT_URL, json=payload, timeout=10)
        return True
    except:
        return False
