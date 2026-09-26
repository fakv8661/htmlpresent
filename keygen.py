import secrets
import string
import re




def generate_login(name: str) -> str:
    TRANSLIT_MAP = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e',
        'ё': 'e', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k',
        'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
        'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts',
        'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': '', 'ы': 'y', 'ь': '',
        'э': 'e', 'ю': 'yu', 'я': 'ya',
        'і': 'i', 'ї': 'yi', 'є': 'ye', 'ґ': 'g', 'ў': 'u',
    }
    words = []
    for word in re.split(r'[\s\-]+', name.strip().lower()):
        latin = ''.join(
            TRANSLIT_MAP.get(ch, ch if re.match(r'[a-z]', ch) else '')
            for ch in word
        )
        if latin:
            words.append(latin)
    return ''.join(w.capitalize() for w in words)


def generate_password(length: int = 12) -> str:
    password = ''
    possible = string.ascii_letters + string.digits
    for i in range(length):
        password += secrets.choice(possible)

    return password

print(generate_password())
