from datetime import datetime, UTC
from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.sesion import Base


class CredencialUsuario(Base):
    __tablename__ = "credenciales_usuario"
    __table_args__ = {"schema": "autenticacion"}

    usuario_id = Column(BigInteger, ForeignKey("autenticacion.usuarios.id"), primary_key=True)
    hash_clave = Column(String(255), nullable=False)
    algoritmo_hash = Column(String(50), nullable=False, default="argon2")
    ultimo_cambio_clave = Column(DateTime, default=lambda: datetime.now(UTC).replace(tzinfo=None))
    requiere_cambio = Column(Boolean, nullable=False, default=False)

    usuario = relationship("Usuario")
