from datetime import datetime, UTC, timedelta

class TiempoUtil:
    @staticmethod
    def ahora_utc_sin_tz():
        return datetime.now(UTC).replace(tzinfo=None)

    @staticmethod
    def esta_en_periodo_de_bloqueo(ahora, fecha_bloqueo, minutos_bloqueo):
        if not fecha_bloqueo:
            return False
        return ahora < fecha_bloqueo + timedelta(minutes=minutos_bloqueo)

    @staticmethod
    def calcular_minutos_restantes(ahora, fecha_bloqueo, minutos_bloqueo):
        if not fecha_bloqueo:
            return 0
        fin_bloqueo = fecha_bloqueo + timedelta(minutes=minutos_bloqueo)
        diferencia = fin_bloqueo - ahora
        return max(0, int(diferencia.total_seconds() / 60))
