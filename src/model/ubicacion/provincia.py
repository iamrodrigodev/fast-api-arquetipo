from sqlalchemy import Column, Integer, String, BigInteger, SmallInteger, DateTime, ForeignKey, Boolean, Float, Text
from sqlalchemy.orm import relationship, backref
from src.config.base_de_datos import Base
from src.constants.validaciones.ubicacion_validacion_constantes import UbicacionValidacionConstantes

class Provincia(Base):
    __tablename__ = 'ubigeo_peru_provincias'
    __table_args__ = {'schema': 'ubicacion'}

    id = Column(String(UbicacionValidacionConstantes.PROVINCIA_ID_MAX), primary_key=True)
    nombre = Column(String(UbicacionValidacionConstantes.NOMBRE_UBICACION_MAX), nullable=False)
    departamento_id = Column(String(UbicacionValidacionConstantes.DEPARTAMENTO_ID_MAX), ForeignKey('ubicacion.ubigeo_peru_departamentos.id'), nullable=False)
    
    departamento = relationship('Departamento', backref=backref('provincias', lazy='dynamic'))

    def __repr__(self):
        return f'<Provincia {self.nombre}>'
