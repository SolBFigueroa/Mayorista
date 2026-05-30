from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
# La base de datos solo entiende lo que tiene Column. Se guarda en la base de datos.
# relationship → es solo para Python.
# ForeignKey tiene el nombre de la TABLA.
class Venta (Base):
    __tablename__ = "ventas"
    #atributos:
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column (DateTime, default = datetime.utcnow, nullable = False)
    user_id = Column(Integer, ForeignKey("usuarios.id"), nullable = False) 
    usuario = relationship("Usuario", back_populates ="ventas") # una venta -> tiene un vendedor
    tipo_entrega = Column(String, nullable = True) # puede existir o no (venta en el local)
    total = Column (Float, nullable = False, default = 0.0)
    detalles = relationship("DetalleVenta", back_populates = "venta") #todos los productos de la venta

class DetalleVenta (Base):
    __tablename__ = "detalle_venta"

    id = Column(Integer, primary_key=True, index=True)
    producto = relationship("Producto", back_populates = "detalles_venta")
    cantidad = Column(Integer, default = 0)
    precio_unitario = Column(Float, default = 0.0)
    subtotal = Column(Float, default = 0.0)
    venta = relationship("Venta", back_populates = "detalles")
    venta_id = Column(Integer, ForeignKey("ventas.id"), nullable = False)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable = False)






















