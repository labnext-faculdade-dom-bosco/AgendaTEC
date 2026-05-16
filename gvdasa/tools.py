import re


def phone_normalizer(phone_number: str) -> str:
    digits = re.sub(r'\D', '', phone_number)
    result = re.sub(r'^(?:55)?(\d{2})9?(\d{4})(\d{4})$', r'55\1\2\3', digits)
    return result if len(result) == 12 else ""


def extract_phone_number(student_data: list) -> str:
    phone_number_type = "Telef. Celular"
    for contact in student_data:
        if contact.get("TipoContatoDescricao", "") == phone_number_type:
            phone_number = contact.get("Contato", "")
            return phone_normalizer(phone_number)
    return ""
