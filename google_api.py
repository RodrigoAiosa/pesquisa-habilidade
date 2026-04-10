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

    # tabela com constraint UNIQUE direta (mais estável que índice separado)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS queue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            payload TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# ==============================
# VERIFICAR DUPLICIDADE
# ==============================
def is_duplicate(email: str):
    if not email:
        return False

    email = email.strip().lower()

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 1 FROM queue
        WHERE email = ?
        LIMIT 1
    """, (email,))

    exists = cursor.fetchone() is not None

    conn.close()
    return exists


# ==============================
# ADICIONAR NA FILA
# ==============================
def enqueue(payload: dict):
    email = payload.get("email")

    if email:
        email = email.strip().lower()
        payload["email"] = email

    # 🔒 BLOQUEIO DUPLICIDADE ANTES DE INSERIR
    if is_duplicate(email):
        print(f"[SKIP] Email duplicado: {email}")
        return False

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO queue (email, payload, status)
            VALUES (?, ?, 'pending')
        """, (email, json.dumps(payload)))

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        # segurança extra contra race condition
        print(f"[SKIP] IntegrityError duplicado: {email}")
        return False

    finally:
        conn.close()


# ==============================
# PROCESSAR FILA
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
                        print(f"[HTTP ERROR] {response.status_code}")

                except Exception as e:
                    print(f"[ENVIO ERROR] {e}")

            conn.commit()
            conn.close()

        except Exception as e:
            print(f"[WORKER ERROR] {e}")

        time.sleep(3)


# ==============================
# START WORKER
# ==============================
def start_worker():
    thread = threading.Thread(target=process_queue, daemon=True)
    thread.start()


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

    return enqueue(payload)


# ==============================
# SALVAR RESUMO
# ==============================
def salvar_resumo_google_sheets(resumo: dict):
    payload = {
        "tipo": "resumo",
        "email": resumo.get("email"),
        "nome": resumo.get("nome"),
        "area": resumo.get("area"),
        "habilidades_marcadas": resumo.get("habilidades_marcadas"),
        "total": resumo.get("total"),
        "conclusao": resumo.get("conclusao")
    }

    return enqueue(payload)


# ==============================
# INICIALIZAÇÃO AUTOMÁTICA
# ==============================
init_db()
start_worker()
