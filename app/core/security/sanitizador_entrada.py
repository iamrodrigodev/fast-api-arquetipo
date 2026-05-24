import bleach
from typing import Optional

class SanitizadorDeEntrada:

    @staticmethod
    def sanitizar(texto: Optional[str]) -> Optional[str]:
        if texto is None:
            return None
        return bleach.clean(texto, tags=[], attributes={}, strip=True).strip()
