from datetime import datetime, UTC
from sqlalchemy import Column, String, BigInteger, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from app.db.sesion import Base
from app.modules.usuarios.schemas.validaciones import UsuarioValidacionConstantes
from app.modules.ubicacion.schemas.validaciones import UbicacionValidacionConstantes
from app.modules.ubicacion.models.distrito import Distrito

class UsuarioDireccion(Base):
    __tablename__ = 'usuario_direcciones'
    __table_args__ = {'schema': 'autenticacion'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    usuario_id = Column(BigInteger, ForeignKey('autenticacion.usuarios.id'), nullable=False, unique=True)
    distrito_id = Column(String(UbicacionValidacionConstantes.DISTRITO_ID_MAX), ForeignKey('ubicacion.ubigeo_peru_distritos.id'))
    
    direccion_exacta = Column(String(UsuarioValidacionConstantes.DIRECCION_MAX))
    referencia = Column(String(UsuarioValidacionConstantes.REFERENCIA_MAX))
    codigo_postal = Column(String(UsuarioValidacionConstantes.CODIGO_POSTAL_MAX))
    
    fecha_creacion = Column(DateTime, default=lambda: datetime.now(UTC).replace(tzinfo=None))
    fecha_actualizacion = Column(
        DateTime,
        default=lambda: datetime.now(UTC).replace(tzinfo=None),
        onupdate=lambda: datetime.now(UTC).replace(tzinfo=None)
    )

    usuario = relationship('Usuario', back_populates='direccion')
    distrito = relationship(Distrito, backref=backref('usuario_direcciones', lazy='dynamic'))

    def __repr__(self):
        return f'<UsuarioDireccion {self.usuario_id}>'
