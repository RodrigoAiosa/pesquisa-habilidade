"""
Arquivo: validators.py
Função: Validar e-mail e celular com regex
"""
import re

def validar_email(email: str) -> bool:
    """
    Valida se o e-mail está no formato correto
    Exemplos válidos:
    - usuario@dominio.com
    - nome.sobrenome@empresa.com.br
    """
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}
