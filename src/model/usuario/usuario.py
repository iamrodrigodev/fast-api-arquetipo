from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, BigInteger, SmallInteger, DateTime, ForeignKey, Boolean, Float, Text
from sqlalchemy.orm import relationship, backref
from src.config.base_de_datos import Base
from src.constants.validaciones.usuario_validacion_constantes import UsuarioValidacionConstantes

class Usuario(Base):
    __tablename__ = 'usuarios'
    __table_args__ = {'schema': 'autenticacion'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nombre = Column(String(UsuarioValidacionConstantes.NOMBRE_MAX), nullable=False)
    apellidos = Column(String(UsuarioValidacionConstantes.APELLIDOS_MAX), nullable=False)
    correo = Column(String(UsuarioValidacionConstantes.CORREO_MAX), nullable=False, unique=True)
    clave = Column(String(UsuarioValidacionConstantes.CLAVE_MAX), nullable=False)
    telefono = Column(String(UsuarioValidacionConstantes.TELEFONO_MAX))
    foto_url = Column(String(UsuarioValidacionConstantes.FOTO_URL_MAX))
    
    estado = Column(SmallInteger, default=1)
    intentos_fallidos_login = Column(SmallInteger, default=0)
    fecha_bloqueo_login = Column(DateTime)
    
    fecha_creacion = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    fecha_actualizacion = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    rol_id = Column(SmallInteger, ForeignKey('autenticacion.roles.id'), nullable=False)
    rol = relationship('Rol', backref=backref('usuarios', lazy='dynamic'))

    direccion = relationship('UsuarioDireccion', back_populates='usuario', uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Usuario {self.correo}>'
