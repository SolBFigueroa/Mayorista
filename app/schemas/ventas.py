from pydantic import BaseModel
from typing import Optional

class VentaCrear(BaseModel):
    user_id: int
    tipo_entrega : Optional[str]= None

class DetalleCrear(BaseModel):
    codigo: str
    cantidad: int



















