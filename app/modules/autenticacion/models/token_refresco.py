from datetime import datetime, UTC
from sqlalchemy import Column, BigInteger, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.sesion import Base


class TokenRefresco(Base):
    __tablename__ = "tokens_refresco"
    __table_args__ = {"schema": "autenticacion"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    usuario_id = Column(BigInteger, ForeignKey("autenticacion.usuarios.id"), nullable=False, index=True)
    token_hash = Column(String(255), nullable=False, unique=True)
    expira_en = Column(DateTime, nullable=False)
    revocado = Column(Boolean, nullable=False, default=False)
    fecha_creacion = Column(DateTime, default=lambda: datetime.now(UTC).replace(tzinfo=None))
    fecha_revocacion = Column(DateTime, nullable=True)

    usuario = relationship("Usuario")
