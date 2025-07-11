from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from APP.db import Base
from datetime import datetime, timezone

class dispositivo(Base):
    __tablename__ = "dispositivo" #NOTEBOOKS, TABLEST, CELULARES, CARGADORES, ETC
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    cantidad = Column(Integer, nullable=False)
    accesorio = Column(Boolean, default=False, nullable=False)
    organismo = Column(String(50), nullable=False)


class formulario_de_entrega(Base):
    __tablename__ = "formulario_de_entrega"
    
    id = Column(Integer, primary_key=True, index=True)
    dispositivo = relationship("dispositivo")
    cant_dispositivo = Column(Integer, nullable=False)
    accesorio1 = Column(String(50), nullable=True)
    cant_accesorio1 = Column(Integer, nullable=True)
    accesorio2 = Column(String(50), nullable=True)
    cant_accesorio2 = Column(Integer, nullable=True)
    accesorio3 = Column(String(50), nullable=True)
    cant_accesorio3 = Column(Integer, nullable=True)
    etiqueta = Column(String(50), nullable=True)
    modelo = Column(String(50), nullable=True)
    dispositivo_id = Column(Integer, ForeignKey("dispositivo.id"), nullable=False)
    organismo = Column(String(50),default="stock_1", nullable=False)
    usuario = Column(String(50), nullable=False)
    nroTicket = Column(String(50), nullable=True)
    tecnico = Column(String(50), nullable=False)
    fecha = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    observaciones = Column(String(100), nullable=True)
    leasing = Column(Boolean,default=False, nullable=True)
    devuelto = Column(Boolean, default=False, nullable=False)

class consumible(Base): 
    __tablename__ = "consumible"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    cantidad = Column(Integer, nullable=False)
    organismo = Column(String(50), nullable=False)  

class formulario_de_devolucion(Base):
    __tablename__ = "formulario_de_devolucion"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    nombre = Column(String(100), nullable=False)
    legajo = Column(String(50), nullable=True) 
    marca = Column(String(50), nullable=True) #LENOVO DELL HP
    nro_etiqueta = Column(String(50), nullable=True)
    otros_articulos = Column(String(200), nullable=True)
    aclaracion_empleado = Column(String(100), nullable=True)
    aclaracion_receptor = Column(String(100), nullable=True)

class stock_leasing(Base):
    __tablename__ = "stock_leasing"
    id = Column(Integer, primary_key=True, index=True)
    cantidad = Column(Integer, nullable=False)

class user(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True)
    user = Column(String(150), unique=True)     
    password = Column(String(150))
    superuser = Column(Boolean, default=False, nullable=False)
   