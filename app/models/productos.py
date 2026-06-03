from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
# La base de datos solo entiende lo que tiene Column
# relationship → es solo para Python.
# ForeignKey tiene el nombre de la TABLA.
class Producto(Base):
    __tablename__ = "productos"
    #atributos:
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable = False)
    stock = Column(Integer, default = 0)
    stock_min = Column(Integer, default = 0)
    precio = Column(Float,nullable=False)
    categoria = Column(String,nullable=False)
    codigo = Column(String, nullable=False, unique=True)
    detalles_venta = relationship("DetalleVenta", back_populates="producto") # todos los DetalleVenta donde ese producto fue vendido


   




















