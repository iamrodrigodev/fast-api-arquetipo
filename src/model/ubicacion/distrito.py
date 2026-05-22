from sqlalchemy import Column, Integer, String, BigInteger, SmallInteger, DateTime, ForeignKey, Boolean, Float, Text
from sqlalchemy.orm import relationship, backref
from src.config.base_de_datos import Base
from src.constants.validaciones.ubicacion_validacion_constantes import UbicacionValidacionConstantes

class Distrito(Base):
    __tablename__ = 'ubigeo_peru_distritos'
    __table_args__ = {'schema': 'ubicacion'}

    id = Column(String(UbicacionValidacionConstantes.DISTRITO_ID_MAX), primary_key=True)
    nombre = Column(String(UbicacionValidacionConstantes.NOMBRE_UBICACION_MAX), nullable=False)
    provincia_id = Column(String(UbicacionValidacionConstantes.PROVINCIA_ID_MAX), ForeignKey('ubicacion.ubigeo_peru_provincias.id'), nullable=False)
    
    provincia = relationship('Provincia', backref=backref('distritos', lazy='dynamic'))

    def __repr__(self):
        return f'<Distrito {self.nombre}>'
