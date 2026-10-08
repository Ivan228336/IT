import re


def validate_username(v: str) -> str:
    """Валидатор никнейма."""
    v = v.strip()

    allowed_pattern = r'^[A-Za-z0-9~!@#%^&*_\-+=`|\\(){}[\]:;"\'<>,.?/$]+$'

    if not v:
        raise ValueError("Никнейм не может быть пустым или состоять только из пробелов")

    if " " in v:
        raise ValueError("Никнейм не должен содержать пробелы")

    if not re.match(allowed_pattern, v):
        invalid_chars = []
        for char in v:
            if not re.match(r'^[A-Za-z0-9~!@#%^&*_\-+=`|\\(){}[\]:;"\'<>,.?/$]$', char):
                if char not in invalid_chars:
                    invalid_chars.append(char)

        if invalid_chars:
            raise ValueError(
                f"Никнейм содержит недопустимые символы: {', '.join(f"'{c}'" for c in invalid_chars)}. "
                "Разрешены только латинские буквы, цифры и символы: ~!@#%^&*_-+=`|\\(){{}}[]:;\"'<>,.?/$"
            )

    currency_pattern = r"[\u20AC\u00A3\u00A5\u20B9\u20BD\u20B4]|€|£|¥|₹|₽"
    if re.search(currency_pattern, v):
        raise ValueError("Никнейм не должен содержать символы валют (€, £, ¥, ₹, ₽ и др.)")

    if v and v[0] in r'~!@#%^&*_\-+=`|\\(){}[]:;"\'<>,.?/$':
        raise ValueError("Никнейм не должен начинаться со специального символа")

    if v and v[-1] in r'~!@#%^&*_\-+=`|\\(){}[]:;"\'<>,.?/$':
        raise ValueError("Никнейм не должен заканчиваться специальным символом")

    return v


def normalize_and_validate_email(v: str) -> str:
    """Приводим email к нижнему регистру и
    проверяем на соответствие паттерну
    """
    pattern = r"^[A-Za-z0-9][A-Za-z0-9._-]*[A-Za-z0-9]@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    if not re.match(pattern, v):
        raise ValueError("Пожалуйста, введите корректный email адрес")
    return v.strip().lower()


def validate_password(v: str) -> str:
    """Комплексная валидация пароля."""
    currency_pattern = r"[\u20AC\u00A3\u00A5\u20B9\u20BD\u20B4]|€|£|¥|₹|₽"
    if re.search(currency_pattern, v):
        raise ValueError("Пароль не должен содержать символы валют (€, £, ¥, ₹, ₽ и др.)")

    pattern = r"""
        ^                          # Начало строки
        (?=.*[A-Z])                # Хотя бы одна заглавная буква
        (?=.*[a-z])                # Хотя бы одна строчная буква  
        (?=.*[0-9])                # Хотя бы одна цифра
        (?=.*[~!@#%^&*_\-+=`|\\(){}[\]:;"'<>,.?/$])  # Хотя бы один спецсимвол
        [A-Za-z0-9~!@#%^&*_\-+=`|\\(){}[\]:;"'<>,.?/$]{8,128}  # Допустимые символы и длина
        $                          # Конец строки
    """

    if not re.match(pattern, v, re.VERBOSE):
        raise ValueError(
            "Пароль должен:\n"
            "1. Быть длиной 8-128 символов\n"
            "2. Содержать хотя бы одну заглавную букву (A-Z)\n"
            "3. Содержать хотя бы одну строчную букву (a-z)\n"
            "4. Содержать хотя бы одну цифру (0-9)\n"
            "5. Содержать хотя бы один специальный символ: ~!@#%^&*_-+=`|\\(){}[]:;\"'<>,.?/$"
        )

    return v
