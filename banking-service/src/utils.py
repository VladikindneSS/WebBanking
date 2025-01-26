import random

def generate_account_number() -> str:
    """
    Генерирует уникальный номер счёта с контрольной цифрой по алгоритму Луна.
    """
    base_number = ''.join(str(random.randint(0, 9)) for _ in range(15))
    
    def luhn_checksum(number: str) -> int:
        digits = [int(d) for d in number]
        for i in range(len(digits) - 1, -1, -2):
            digits[i] *= 2
            if digits[i] > 9:
                digits[i] -= 9
        return sum(digits) % 10

    check_digit = (10 - luhn_checksum(base_number + "0")) % 10
    return f"{base_number}{check_digit}"