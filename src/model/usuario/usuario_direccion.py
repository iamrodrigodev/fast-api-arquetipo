from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, BigInteger, SmallInteger, DateTime, ForeignKey, Boolean, Float, Text
from sqlalchemy.orm import relationship, backref
from src.config.base_de_datos import Base
from src.constants.validaciones.usuario_validacion_constantes import UsuarioValidacionConstantes
from src.constants.validaciones.ubicacion_validacion_constantes import UbicacionValidacionConstantes

class UsuarioDireccion(Base):
    __tablename__ = 'usuario_direcciones'
    __table_args__ = {'schema': 'autenticacion'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    usuario_id = Column(BigInteger, ForeignKey('autenticacion.usuarios.id'), nullable=False, unique=True)
    distrito_id = Column(String(UbicacionValidacionConstantes.DISTRITO_ID_MAX), ForeignKey('ubicacion.ubigeo_peru_distritos.id'))
    
    direccion_exacta = Column(String(UsuarioValidacionConstantes.DIRECCION_MAX))
    referencia = Column(String(UsuarioValidacionConstantes.REFERENCIA_MAX))
    codigo_postal = Column(String(UsuarioValidacionConstantes.CODIGO_POSTAL_MAX))
    
    fecha_creacion = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    fecha_actualizacion = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    usuario = relationship('Usuario', back_populates='direccion')
    distrito = relationship('src.model.ubicacion.distrito.Distrito', backref=backref('usuario_direcciones', lazy='dynamic'))

    def __repr__(self):
        return f'<UsuarioDireccion {self.usuario_id}>'
