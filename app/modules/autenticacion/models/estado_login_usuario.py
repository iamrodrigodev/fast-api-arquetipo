from sqlalchemy import Column, BigInteger, DateTime, ForeignKey, SmallInteger, String
from sqlalchemy.orm import relationship
from app.db.sesion import Base


class EstadoLoginUsuario(Base):
    __tablename__ = "estado_login_usuario"
    __table_args__ = {"schema": "autenticacion"}

    usuario_id = Column(BigInteger, ForeignKey("autenticacion.usuarios.id"), primary_key=True)
    intentos_fallidos = Column(SmallInteger, nullable=False, default=0)
    bloqueado_hasta = Column(DateTime, nullable=True)
    ultimo_login_ok = Column(DateTime, nullable=True)
    ultimo_login_ip = Column(String(64), nullable=True)

    usuario = relationship("Usuario")
