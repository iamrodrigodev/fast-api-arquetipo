from enum import Enum
from sqlalchemy import Column, Integer, String, BigInteger, SmallInteger, DateTime, ForeignKey, Boolean, Float, Text
from sqlalchemy.orm import relationship, backref
from app.db.sesion import Base
from app.modules.autenticacion.schemas.validaciones import SeguridadValidacionConstantes

class NombreRol(Enum):
    ADMINISTRADOR = "ADMINISTRADOR"
    USUARIO = "USUARIO"

class Rol(Base):
    __tablename__ = 'roles'
    __table_args__ = {'schema': 'autenticacion'}

    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    nombre = Column(String(SeguridadValidacionConstantes.NOMBRE_ROL_MAX), nullable=False, unique=True)

    def __repr__(self):
        return f'<Rol {self.nombre}>'
