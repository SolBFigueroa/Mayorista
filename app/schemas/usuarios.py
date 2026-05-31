from pydantic import BaseModel
from typing import Optional

class UsuarioCrear(BaseModel):
    nombre: str
    apellido: str
    email: str
    contraseña: str
    rol: str

class CambiarContraseña(BaseModel):
    contraseña_actual: str
    contraseña_nueva: str



















