from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, backref
from app.db.sesion import Base
from app.modules.ubicacion.schemas.validaciones import UbicacionValidacionConstantes

class Departamento(Base):
    __tablename__ = 'ubigeo_peru_departamentos'
    __table_args__ = {'schema': 'ubicacion'}

    id = Column(String(UbicacionValidacionConstantes.DEPARTAMENTO_ID_MAX), primary_key=True)
    nombre = Column(String(UbicacionValidacionConstantes.NOMBRE_UBICACION_MAX), nullable=False)

    def __repr__(self):
        return f'<Departamento {self.nombre}>'
