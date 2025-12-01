import re

NUM_WORDS = {
    "uno": 1, "una": 1, "un": 1,
    "dos": 2,
    "tres": 3,
    "cuatro": 4,
    "cinco": 5,
    "seis": 6,
    "siete": 7,
    "ocho": 8,
    "nueve": 9,
    "diez": 10
}


def word_to_number(word):
    """Convierte palabras como 'tres' → 3"""
    return NUM_WORDS.get(word.lower())

def extract_bathrooms(text):
    """Devuelve número de baños desde un texto en castellano o '' si no encuentra."""
    if not text:
        return ""

    text = text.lower()

    # INTENTO 1 → número explícito: “3 baños”
    m = re.search(r'(\d+)\s*bañ', text)
    if m:
        return int(m.group(1))

    # INTENTO 2 → número en palabra: “tres baños”
    m = re.search(r'(\w+)\s*bañ', text)
    if m:
        num = word_to_number(m.group(1))
        if num:
            return num

    # INTENTO 3 → menciona "baño" pero sin número
    if "baño" in text:
        return 1  # Asumes mínimo 1 si es ambiguo

    return ""