from sqlalchemy import Column, String, SmallInteger
from app.db.sesion import Base
from app.modules.autenticacion.schemas.validaciones import SeguridadValidacionConstantes

class Rol(Base):
    __tablename__ = 'roles'
    __table_args__ = {'schema': 'autenticacion'}

    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    nombre = Column(String(SeguridadValidacionConstantes.NOMBRE_ROL_MAX), nullable=False, unique=True)

    def __repr__(self):
        return f'<Rol {self.nombre}>'
