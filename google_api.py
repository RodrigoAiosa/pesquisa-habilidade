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

DB_LOCK = threading.Lock()
WORKER_STARTED = False


# ==============================
# CONEXÃO SEGURA + WAL MODE
# ==============================
def get_conn():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False, timeout=30)
    conn.execute("PRAGMA journal_mode=WAL")  # 🔥 ESSENCIAL para Streamlit
    return conn


# ==============================
# INIT DB
# ==============================
def init_db():
    with DB_LOCK:
        conn = get_conn()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT,
                payload TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        conn.close()


# ==============================
# DUPLICIDADE
# ==============================
def is_duplicate(email: str):
    if not email:
        return False

    email = email.strip().lower()

    with DB_LOCK:
        conn = get_conn()
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
# ENQUEUE
# ==============================
def enqueue(payload: dict):
    email = payload.get("email")

    if email:
        email = email.strip().lower()
        payload["email"] = email

    if is_duplicate(email):
        print(f"[SKIP] duplicado: {email}")
        return False

    try:
        with DB_LOCK:
            conn = get_conn()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO queue (email, payload, status)
                VALUES (?, ?, 'pending')
            """, (email, json.dumps(payload)))

            conn.commit()
            conn.close()

        return True

    except sqlite3.OperationalError as e:
        print(f"[SQLITE ERROR] {e}")
        return False

    except sqlite3.IntegrityError:
        print(f"[SKIP] integrity duplicate: {email}")
        return False


# ==============================
# WORKER
# ==============================
def process_queue():
    while True:
        try:
            with DB_LOCK:
                conn = get_conn()
                cursor = conn.cursor()

                cursor.execute("""
                    SELECT id, payload FROM queue
                    WHERE status = 'pending'
                    ORDER BY id ASC
                    LIMIT 5
                """)

                rows = cursor.fetchall()
                conn.close()

            for row in rows:
                row_id, payload = row
                payload = json.loads(payload)

                try:
                    response = requests.post(
                        GOOGLE_SCRIPT_URL,
                        json=payload,
                        timeout=10
                    )

                    with DB_LOCK:
                        conn = get_conn()
                        cursor = conn.cursor()

                        cursor.execute("""
                            UPDATE queue
                            SET status = ?
                            WHERE id = ?
                        """, ("sent" if response.status_code == 200 else "error", row_id))

                        conn.commit()
                        conn.close()

                except Exception as e:
                    print(f"[SEND ERROR] {e}")

        except Exception as e:
            print(f"[WORKER ERROR] {e}")

        time.sleep(3)


# ==============================
# START WORKER (SINGLETON)
# ==============================
def start_worker():
    global WORKER_STARTED

    if WORKER_STARTED:
        return

    WORKER_STARTED = True

    thread = threading.Thread(target=process_queue, daemon=True)
    thread.start()


# ==============================
# API
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
# INIT (SAFE)
# ==============================
init_db()
start_worker()
