from pydantic import BaseModel
from typing import Optional

class ProductoCrear (BaseModel):
    # todos lo campos son obligatorios
    nombre : str
    categoria: str
    stock: int
    stock_min: int
    precio :float
    codigo: str

class ProductoActualizar (BaseModel):
    # campos opcionales
    nombre : Optional[str]= None
    categoria: Optional[str]= None
    stock: Optional[int]= None
    stock_min: Optional[int]= None
    precio: Optional[float]= None










