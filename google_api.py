import requests

# ==============================
# GOOGLE SHEETS CONFIG
# ==============================
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzbWDJx_2TuXXtPnMdn3507XPkcQha_AImQ_lRn14Y3y1Ii_mdTs_ZsdV64vYc6UxWs2w/exec"


def salvar_google_sheets(dados: dict):
    """
    Envia os dados do candidato para o Google Sheets via Google Apps Script
    """

    payload = {
        "nome": dados.get("nome"),
        "sexo": dados.get("sexo"),
        "email": dados.get("email"),
        "celular": dados.get("celular")
    }

    try:
        response = requests.post(
            GOOGLE_SCRIPT_URL,
            json=payload,
            timeout=5
        )

        # opcional: validar resposta do script
        if response.status_code != 200:
            print(f"Erro ao salvar no Google Sheets: {response.text}")

    except Exception as e:
        print(f"Falha na integração Google Sheets: {str(e)}")
