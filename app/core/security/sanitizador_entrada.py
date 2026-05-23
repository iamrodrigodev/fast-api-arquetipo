import bleach
from typing import Optional

class SanitizadorDeEntrada:
    """
    Utilidad para sanitizar entradas de usuario y prevenir ataques XSS (Cross-Site Scripting).
    Utiliza la librería bleach para limpiar etiquetas HTML peligrosas.
    """

    @staticmethod
    def sanitizar(texto: Optional[str]) -> Optional[str]:
        if texto is None:
            return None
        
        # Bleach limpia etiquetas como <script>, <iframe>, etc., pero permite texto plano.
        return bleach.clean(texto, tags=[], attributes={}, strip=True).strip()
