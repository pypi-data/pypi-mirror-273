import re
from datetime import datetime
from ..exceptions.date_exceptions import *

def sanitize_dates(received_date, multiple=False):
    # Comprobar si la entrada es una cadena vacía o solo contiene espacios
    if not received_date.strip():
        raise EmptyDateException(received_date)

    # Patrón para encontrar la fecha en distintos formatos comunes
    date_pattern = r'\b(\d{2})[\/\s-](\d{2})[\/\s-](\d{4})\b'
    
    try:
        matches = re.findall(date_pattern, received_date)
        if matches:
            formatted_dates = []
            for match in matches:
                day, month, year = match
                iso_formatted_date = f"{year}-{month}-{day}"
                # Validar fecha convertida
                datetime.strptime(iso_formatted_date, "%Y-%m-%d")
                formatted_dates.append(iso_formatted_date)
                
            if multiple:
                return formatted_dates  # Devuelve todas las fechas formateadas
            else:
                return formatted_dates[0] if formatted_dates else None  # Devuelve solo la primera fecha formateada
        else:
            # Lanzar una excepción si no se encuentra una fecha válida
            raise InvalidDateException(received_date)
    except ValueError as e:
        # Lanzar una excepción si la fecha es inválida o hay un error lógico
        raise InvalidDateException(received_date)
