import requests

# ==============================
# NOVA URL DO GOOGLE APPS SCRIPT
# ==============================
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycby9qXNnvoJDP6ghOq-z_vnEktGYnQ0cRmocmw7neYG7XCkt9NpMVxy1yntklTXzagTP/exec"


# ==============================
# SALVAR CADASTRO
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
        return response.json()
    except Exception as e:
        print(f"Erro cadastro: {e}")
        return {"status": "erro", "message": str(e)}


# ==============================
# SALVAR RESUMO
# ==============================
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
        response = requests.post(GOOGLE_SCRIPT_URL, json=payload, timeout=10)
        return response.json()
    except Exception as e:
        print(f"Erro resumo: {e}")
        return {"status": "erro", "message": str(e)}
