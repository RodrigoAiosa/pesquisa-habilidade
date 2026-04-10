import requests
import sqlite3
import json
import threading
import time

# ==============================
# CONFIG
# ==============================
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycby9qXNnvoJDP6ghOq-z_vnEktGYnQ0cRmocmw7neYG7XCkt9NpMVxy1yntklTXzagTP/exec"

DB_FILE = "queue.db"


# ==============================
# BANCO (FILA PERSISTENTE)
# ==============================
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS queue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            payload TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# ==============================
# ADICIONAR NA FILA
# ==============================
def enqueue(payload: dict):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO queue (payload, status)
        VALUES (?, 'pending')
    """, (json.dumps(payload),))

    conn.commit()
    conn.close()


# ==============================
# PROCESSAR ENVIO
# ==============================
def process_queue():
    while True:
        try:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id, payload FROM queue
                WHERE status = 'pending'
                ORDER BY id ASC
                LIMIT 5
            """)

            rows = cursor.fetchall()

            for row in rows:
                row_id = row[0]
                payload = json.loads(row[1])

                try:
                    response = requests.post(
                        GOOGLE_SCRIPT_URL,
                        json=payload,
                        timeout=10
                    )

                    if response.status_code == 200:
                        cursor.execute("""
                            UPDATE queue
                            SET status = 'sent'
                            WHERE id = ?
                        """, (row_id,))

                    else:
                        print(f"Erro HTTP: {response.status_code}")

                except Exception as e:
                    print(f"Erro envio fila: {e}")

            conn.commit()
            conn.close()

        except Exception as e:
            print(f"Erro worker: {e}")

        time.sleep(3)


# ==============================
# START WORKER
# ==============================
def start_worker():
    thread = threading.Thread(target=process_queue, daemon=True)
    thread.start()


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

    enqueue(payload)


# ==============================
# RESUMO
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

    enqueue(payload)


# ==============================
# INICIALIZAÇÃO AUTOMÁTICA
# ==============================
init_db()
start_worker()
