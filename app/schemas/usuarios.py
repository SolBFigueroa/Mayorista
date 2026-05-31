from pydantic import BaseModel
from typing import Optional

class UsuarioCrear(BaseModel):
    nombre: str
    apellido: str
    email: str
    password: str
    rol: str

class CambiarPassword(BaseModel):
    password_actual: str
    password_nueva: str



















