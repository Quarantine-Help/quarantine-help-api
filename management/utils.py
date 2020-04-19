import phonenumbers as phonenumbers


def mask_phone_number(phone_number):
    if not phone_number:
        return ""

    phone_number_parsed = phonenumbers.parse(phone_number)
    local_part_len = len(str(phone_number_parsed.national_number))
    return f"+{phone_number_parsed.country_code}-" + f"X" * local_part_len
