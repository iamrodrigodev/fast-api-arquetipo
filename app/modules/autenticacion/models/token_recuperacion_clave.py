from app.utils.tiempo_util import TiempoUtil
from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.sesion import Base


class TokenRecuperacionClave(Base):
    __tablename__ = "tokens_recuperacion_clave"
    __table_args__ = {"schema": "autenticacion"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    usuario_id = Column(BigInteger, ForeignKey("autenticacion.usuarios.id"), nullable=False, index=True)
    token_hash = Column(String(255), nullable=False, unique=True)
    expira_en = Column(DateTime, nullable=False)
    usado = Column(Boolean, nullable=False, default=False)
    fecha_uso = Column(DateTime, nullable=True)
    ip_solicitud = Column(String(64), nullable=True)
    fecha_creacion = Column(DateTime, default=lambda: TiempoUtil.ahora_utc_sin_tz())

    usuario = relationship("Usuario")

