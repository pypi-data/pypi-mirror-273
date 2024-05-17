import re
from ..exceptions.vin_exceptions import *

def calculate_check_digit(vin):
    # Mapeo de letras a valores para cálculo del VIN según la norma ISO 3779
    vin_values = {
        '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
        'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8,
        'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'P': 7, 'R': 9,
        'S': 2, 'T': 3, 'U': 4, 'V': 5, 'W': 6, 'X': 7, 'Y': 8, 'Z': 9
    }
    weights = [8, 7, 6, 5, 4, 3, 2, 10, 0, 9, 8, 7, 6, 5, 4, 3, 2]
    
    # Calcular el valor del VIN
    sum = 0
    for i in range(len(vin)):
        char = vin[i]
        if char in vin_values:
            value = vin_values[char]
            sum += value * weights[i]
    
    # Calcular dígito de verificación
    check_digit = sum % 11
    check_digit = 'X' if check_digit == 10 else str(check_digit)
    
    return check_digit

def sanitize_vin(received_vin):
    # Buscar VIN en el texto (17 caracteres, excluyendo I, O y Q)
    vin_pattern = r'[A-HJ-NPR-Z0-9]{17}'
    matches = re.findall(vin_pattern, received_vin.upper())

    for vin in matches:
        # Validar el dígito de verificación
        if vin[8] == calculate_check_digit(vin):
            return vin

    # Si no se encuentra ningún VIN válido, lanzar excepción
    raise InvalidVinException(received_vin)
