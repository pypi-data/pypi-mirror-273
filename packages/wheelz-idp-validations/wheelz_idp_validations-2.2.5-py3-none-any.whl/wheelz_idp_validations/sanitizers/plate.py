import re
from ..exceptions.plate_exceptions import *

def sanitize_plate(received_plate):
    # Quitamos los posibles guiones que pueden existir en el texto
    received_plate = re.sub(r'-', '', received_plate)
    # Definir patrones para los diferentes tipos de matrículas, incluyendo espacios opcionales donde sea necesario
    patterns = [
        r'\b\d{4}\s?[BCDFGHJKLMNPQRSTVWXYZ]{3}\b',  # Tipo 1: 4 números seguidos de 3 letras no vocales, con un espacio opcional
        r'\b[A-Z]{1,3}\s?\d{6}\b',                  # Tipo 2: Hasta 3 letras seguidas de 6 números con un espacio opcional
        r'\b[A-Z]{1,2}\s?\d{4}\s?[A-Z]{1,2}\b',     # Tipo 3: 1-2 letras, 4 números y 1-2 letras, con espacios opcionales
        r'\bR\s?\d{3}\s?[A-Z]{3}\b',                # Tipo 4: Una R, 3 números y 3 letras, con espacios opcionales
        r'\bH\s?\d{4}\s?[A-Z]{3}\b',                # Tipo 5: Una H, 4 números y 3 letras, con espacios opcionales
        r'\bC\s?\d{4}\s?[A-Z]{3}\b',                # Tipo 6: Una C, 4 números y 3 letras, con espacios opcionales
    ]

    # Comprobar si la entrada es una cadena vacía o solo contiene espacios
    if not received_plate.strip():
        raise EmptyInputException(received_plate)

    # Buscar la primera matrícula que coincida con alguno de los patrones en el received_plateo original
    for pattern in patterns:
        match = re.search(pattern, received_plate.upper())
        if match:
            # Normalizar la matrícula encontrada eliminando espacios internos para devolver un formato uniforme
            return re.sub(r'\s+', '', match.group(0))

    # Si no se encuentra ninguna matrícula válida, lanzar una excepción
    raise InvalidPlateException(received_plate)
