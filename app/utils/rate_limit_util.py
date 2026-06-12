import time
from collections import defaultdict, deque

class LimitadorMemoria:
    def __init__(self):
        self.eventos = defaultdict(deque)

    def permitido(self, clave: str, limite: int, ventana_segundos: int) -> bool:
        ahora = time.time()
        cola = self.eventos[clave]
        while cola and cola[0] <= ahora - ventana_segundos:
            cola.popleft()
        if len(cola) >= limite:
            return False
        cola.append(ahora)
        return True

limitador_memoria = LimitadorMemoria()
