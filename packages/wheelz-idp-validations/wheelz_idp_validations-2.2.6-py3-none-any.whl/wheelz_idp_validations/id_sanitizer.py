from wheelz_idp_validations.sanitizers.id_number import sanitize_id_number
from wheelz_idp_validations.sanitizers.gender import sanitize_gender
from wheelz_idp_validations.sanitizers.date import sanitize_dates

def sanitize_id(response_dict):
    # Sanitize ID Number
    if "documentNumber" in response_dict:
        try: 
            response_dict["documentNumber"] = sanitize_id_number(response_dict["documentNumber"], True)
        except Exception as e:
            response_dict["documentNumber"] = ""
            print("Error sanitizing document number:", str(e))
    else:
        print("Warning: 'documentNumber' has not been validated because not found in the response dictionary.")

    # Sanitize MRZ to extract DNI
    if "mrz" in response_dict:
        try: 
            response_dict["documentNumber"] = sanitize_id_number(response_dict["mrz"], True)
        except Exception as e:
            response_dict["documentNumber"] = ""
            print("Error extracting document number from mrz:", str(e))
    else:
        print("Warning: 'mrz' has not been validated because not found in the response dictionary.")

    # Sanitize Gender
    if "gender" in response_dict:
        try:
            response_dict["gender"] = sanitize_gender(response_dict["gender"])
        except Exception as e:
            response_dict["gender"] = ""
            print("Error sanitizing gender:", str(e))
    else:
        print("Warning: 'gender' has not been validated because not found in the response dictionary.")

    # Sanitize Birth Date
    if "birthDate" in response_dict:
        try:
            response_dict["birthDate"] = sanitize_dates(response_dict["birthDate"], multiple = False)
        except Exception as e:
            response_dict["birthDate"] = ""
            print("Error sanitizing birth date:", str(e))
    else:
        print("Warning: 'birthDate' has not been validated because not found in the response dictionary.")

    # Sanitize Expiration Date
    if "expirationDate" in response_dict:
        try:
            response_dict["expirationDate"] = sanitize_dates(response_dict["expirationDate"], multiple = False)
        except Exception as e:
            response_dict["expirationDate"] = ""
            print("Error sanitizing expiration date:", str(e))
    else:
        print("Warning: 'expirationDate' has not been validated because not found in the response dictionary.")

    return response_dict
