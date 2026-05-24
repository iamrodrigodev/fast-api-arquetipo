from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from app.db.sesion import Base
from app.modules.ubicacion.schemas.validaciones import UbicacionValidacionConstantes
from app.modules.ubicacion.models.departamento import Departamento

class Provincia(Base):
    __tablename__ = 'ubigeo_peru_provincias'
    __table_args__ = {'schema': 'ubicacion'}

    id = Column(String(UbicacionValidacionConstantes.PROVINCIA_ID_MAX), primary_key=True)
    nombre = Column(String(UbicacionValidacionConstantes.NOMBRE_UBICACION_MAX), nullable=False)
    departamento_id = Column(String(UbicacionValidacionConstantes.DEPARTAMENTO_ID_MAX), ForeignKey('ubicacion.ubigeo_peru_departamentos.id'), nullable=False)
    
    departamento = relationship(Departamento, backref=backref('provincias', lazy='dynamic'))

    def __repr__(self):
        return f'<Provincia {self.nombre}>'
