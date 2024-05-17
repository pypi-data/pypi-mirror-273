import re
from ..exceptions.cif_exceptions import *

# Cif algorithm documentation https://www.mapa.gob.es/app/materialvegetal/docs/CIF.pdf
def sanitize_cif(received_cif):
    cif_regexp_default = r"([ABCDEFGHQSKLM])(\d{7})(\d)"
    cif_regexp_special = r"(\d)(\d{7})([PX])"
    special = False

    # Intentar extraer el CIF usando el formato estándar
    match = re.search(cif_regexp_default, received_cif)

    # Si no hay coincidencia, intentar con el formato especial
    if not match:
        match = re.search(cif_regexp_special, received_cif)
        special = True
        if not match:
            raise NoCIFMatchFoundException(received_cif)

    # Preparar los componentes del CIF para validación
    digits = match.group(2).replace('O', '0')
    if not special:
        letter = match.group(1)
        control_digit = match.group(3).replace('O', '0')
    else:
        letter = match.group(3)
        control_digit = match.group(1).replace('O', '0')

    processed_cif = letter + digits + control_digit

    # Validar el CIF según el algoritmo especificado
    total_sum = 0
    for pos in range(len(digits)):
        num = int(digits[pos])
        if pos % 2 == 0:
            total_sum += sum(int(x) for x in str(num * 2))
        else:
            total_sum += num

    # Calcular el dígito de control esperado
    check_digit = str((10 - (total_sum % 10)) % 10)
    if (check_digit != control_digit and not (control_digit == 'P' and check_digit == '0')):
        raise InvalidCIFException(processed_cif)

    return processed_cif
