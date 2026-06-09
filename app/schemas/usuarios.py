from pydantic import BaseModel
from typing import Optional

class UsuarioCrear(BaseModel):
    nombre: str
    apellido: str
    email: str
    password: str
    rol: str

class CambiarPassword(BaseModel):
    actual: str
    nueva: str

class UsuarioLogin(BaseModel):
    email : str
    password : str

class UsuarioRespuesta(BaseModel):
    id: int
    nombre: str
    apellido: str
    email: str
    activo:bool
    rol: str












