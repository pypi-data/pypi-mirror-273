from wheelz_idp_validations.sanitizers.plate import sanitize_plate
from wheelz_idp_validations.sanitizers.vin import sanitize_vin
from wheelz_idp_validations.sanitizers.date import sanitize_dates

def sanitize_pcv2(response_dict):
    # Sanitize número de matrícula. Campo A
    if "A" in response_dict:
        try:
            response_dict["A"] = sanitize_plate(response_dict["A"])
        except Exception as e:
            response_dict["A"] = ""
            print("Error sanitizing field A:", str(e))
    else:
        print("Warning: 'A' has not been validated because not found in the response dictionary.")

    # Sanitize número de bastidor o VIN. Campo E
    if "E" in response_dict:
        try:
            response_dict["E"] = sanitize_vin(response_dict["E"])
        except Exception as e:
            response_dict["E"] = ""
            print("Error sanitizing field E:", str(e))
    else:
        print("Warning: 'E' has not been validated because not found in the response dictionary.")
    
    # Sanitize field fecha de primera matriculación. Campo B
    if "B" in response_dict:
        try:
            response_dict["B"] = sanitize_dates(response_dict["B"], multiple = False)
        except Exception as e:
            response_dict["B"] = ""
            print("Error sanitizing field B:", str(e))
    else:
        print("Warning: 'B' has not been validated because not found in the response dictionary.")

    # Sanitize field periodo de validez del permiso. Campo H
    if "H" in response_dict:
        try:
            response_dict["H"] = sanitize_dates(response_dict["H"], multiple = False)
        except Exception as e:
            response_dict["H"] = ""
            print("Error sanitizing field H:", str(e))
    else:
        print("Warning: 'H' has not been validated because not found in the response dictionary.")

    # Sanitize field fecha de matriculación a la que se refiere el presente permiso. Campo I
    if "I" in response_dict:
        try:
            response_dict["I"] = sanitize_dates(response_dict["I"], multiple = False)
        except Exception as e:
            response_dict["I"] = ""
            print("Error sanitizing field I:", str(e))
    else:
        print("Warning: 'I' has not been validated because not found in the response dictionary.")

    # Sanitize field fecha de expedición. Campo I.1
    if "I.1" in response_dict:
        try:
            response_dict["I.1"] = sanitize_dates(response_dict["I.1"], multiple = False)
        except Exception as e:
            response_dict["I.1"] = ""
            print("Error sanitizing field I.1:", str(e))
    else:
        print("Warning: 'I.1' has not been validated because not found in the response dictionary.")

    return response_dict

