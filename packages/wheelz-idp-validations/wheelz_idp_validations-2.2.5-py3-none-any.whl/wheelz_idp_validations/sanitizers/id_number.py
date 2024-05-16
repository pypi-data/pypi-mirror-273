import re
from ..exceptions.id_exceptions import *

# Spanish ID algorithm
def validate_dni(dni):
    letters = "TRWAGMYFPDXBNJZSQVHLCKE"
    numeric_part = dni[:-1]
    letter = dni[-1]
    if letter == letters[int(numeric_part) % 23]:
        return True
    return False

# If we are looking to check only for the first match in a given text, we must use this function with
# keep_search=False, otherwise, it must be keep_searching=True
def sanitize_id_number(received_id, keep_searching=False):
    # Lista de DNIs explícitamente inválido
    not_valid = {"00000000T", "00000001R", "99999999R"}
    # Primera expresión regular
    dni_patterns = [
        r"\b([0-9]{8}[A-Z])\b",  # Patrón básico
        r"([0-9]{8})\s*([A-Z])",  # Patrón con espacio opcional
        r"\b([0-9O]{8})[A-Z]<<<<<<"  # Patrón para MRZ con caracteres especiales
    ]

    for pattern in dni_patterns:
        for match in re.finditer(pattern, received_id):
            dni_candidate = match.group().replace('O', '0').replace(' ', '').replace('<', '')
            if dni_candidate in not_valid:
                raise InvalidIDException(received_id)
            if validate_dni(dni_candidate):
                return dni_candidate
            elif not keep_searching:
                break

        if not keep_searching:
            raise NoIDMatchFoundException(received_id)

    # Si no se encuentra nada y keep_searching es True, intentamos con el siguiente patrón
    if keep_searching:
        # Implementar aquí transformaciones o búsqueda más complejas si es necesario
        # Por ejemplo, buscar en todo el received_ido secuencias de 8 dígitos seguidas por una letra, incluso con caracteres entre medio
        complex_pattern = r"([0-9]{7,8}).{0,5}([A-Z])"
        for match in re.finditer(complex_pattern, received_id):
            dni_candidate = re.sub(r"[^0-9A-Z]", '', match.group()).replace('O', '0')
            if len(dni_candidate) == 9 and validate_dni(dni_candidate):
                return dni_candidate

    raise NoValidIDFoundInMultipleSearchException(received_id)
