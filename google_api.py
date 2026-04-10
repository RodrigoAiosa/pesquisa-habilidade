import requests

GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzbWDJx_2TuXXtPnMdn3507XPkcQha_AImQ_lRn14Y3y1Ii_mdTs_ZsdV64vYc6UxWs2w/exec"


def salvar_google_sheets(dados: dict):
    payload = {
        "tipo": "cadastro",
        "nome": dados.get("nome"),
        "sexo": dados.get("sexo"),
        "email": dados.get("email"),
        "celular": dados.get("celular")
    }

    try:
        requests.post(GOOGLE_SCRIPT_URL, json=payload, timeout=5)
    except Exception as e:
        print(f"Erro cadastro: {e}")


# 🔥 NOVA FUNÇÃO: SALVAR RESUMO
def salvar_resumo_google_sheets(resumo: dict):
    payload = {
        "tipo": "resumo",
        "nome": resumo.get("nome"),
        "area": resumo.get("area"),
        "habilidades_marcadas": resumo.get("habilidades_marcadas"),
        "total": resumo.get("total"),
        "conclusao": resumo.get("conclusao")
    }

    try:
        requests.post(GOOGLE_SCRIPT_URL, json=payload, timeout=5)
    except Exception as e:
        print(f"Erro resumo: {e}")
