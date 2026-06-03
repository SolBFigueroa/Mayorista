from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
# La base de datos solo entiende lo que tiene Column
# relationship → es solo para Python.
# ForeignKey tiene el nombre de la TABLA.
class Usuario(Base):
    __tablename__ = "usuarios"
    #atributos:
    id = Column(Integer, primary_key = True, index=True)
    nombre = Column(String, nullable = False) 
    apellido = Column(String, nullable = False) 
    email = Column(String, nullable = False, unique = True)
    password = Column(String, nullable = False)
    activo = Column(Boolean, default = True) # es o ya no empleado
    rol = Column(String, nullable = False)
    # relationship (conexion entre tablas):
    # primer campo = clase con la que se conecta
    # segundo campo = cómo se llama el atributo en la otra clase que apunta de vuelta.
    # back_populates SIEMPRE tiene que ser el nombre de un relationship.
    # un vendedor -> tiene muchas ventas
    ventas = relationship("Venta", back_populates = "usuario")











