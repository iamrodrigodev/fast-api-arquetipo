from sqlalchemy import Column, String, BigInteger, DateTime, JSON
from app.db.sesion import Base
from app.utils.tiempo_util import TiempoUtil

class RegistroAuditoria(Base):
    __tablename__ = 'registros_auditoria'
    __table_args__ = {'schema': 'estado'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    evento = Column(String(100), nullable=False)
    resultado = Column(String(50), nullable=False)
    campos = Column(JSON, nullable=True)
    fecha_registro = Column(DateTime, default=TiempoUtil.ahora_utc_sin_tz, nullable=False)

    def __repr__(self):
        return f'<RegistroAuditoria {self.evento}:{self.resultado}>'
