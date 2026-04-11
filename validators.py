import re

def validar_email(email: str) -> bool:
    """
    Valida se o e-mail está no formato correto
    """
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(padrao, email) is not None

def validar_celular(celular: str) -> bool:
    """
    Valida celular no formato brasileiro
    Exemplos válidos:
    (11) 91234-5678
    11912345678
    """
    padrao = r'^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$'
    return re.match(padrao, celular) is not None
