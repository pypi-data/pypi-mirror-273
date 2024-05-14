import re
from datetime import datetime
from ..exceptions.date_exceptions import *

def sanitize_dates(received_date):
    # Comprobar si la entrada es una cadena vacía o solo contiene espacios
    if not received_date.strip():
        raise EmptyDateException(received_date)

    # Patrón para encontrar la fecha en distintos formatos comunes
    date_pattern = r'\b(\d{2})[\/\s-](\d{2})[\/\s-](\d{4})\b'
    
    try:
        match = re.search(date_pattern, received_date)
        if match:
            day, month, year = match.groups()
            iso_formatted_date = f"{year}-{month}-{day}"
            datetime.strptime(iso_formatted_date, "%Y-%m-%d")  # Validar fecha convertida
            return iso_formatted_date
        else:
            # Lanzar una excepción si no se encuentra una fecha válida
            raise InvalidDateException(received_date)
    except ValueError as e:
        # Lanzar una excepción si la fecha es inválida o hay un error lógico
        raise InvalidDateException(received_date)
