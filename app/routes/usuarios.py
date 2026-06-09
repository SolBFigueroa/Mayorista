from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_db
from app.models.usuarios import Usuario
from app.schemas.usuarios import UsuarioCrear, CambiarPassword, UsuarioRespuesta, UsuarioLogin
from app.seguridad import hashear_password, crear_token, verificar_password,obtener_usuario_actual
from typing import List

router = APIRouter()

@router.get("/usuarios", response_model  = List[ UsuarioRespuesta])
def listar_usuarios(usuario: dict = Depends(obtener_usuario_actual),db: Session = Depends(get_db)):
    return db.query(Usuario).all()

@router.post("/usuarios", response_model  = UsuarioRespuesta)
def crear_usuario(new_user: UsuarioCrear,db: Session = Depends(get_db)): #el admin crea usuarios.
    usuario_db = db.query(Usuario).filter(Usuario.email == new_user.email).first()
    if usuario_db is not None:
        raise HTTPException(status_code=400, detail="Email ya existente")
    pwd_hasheada = hashear_password(new_user.password)
    nuevo_usuario = Usuario(nombre = new_user.nombre, apellido = new_user.apellido , email= new_user.email, password =pwd_hasheada ,rol = new_user.rol )
    db.add(nuevo_usuario)
    db.commit()
    return nuevo_usuario

@router.get("/usuarios/buscar/{name}")
def buscar_nombre_usuario(name: str ,usuario: dict = Depends(obtener_usuario_actual), db: Session = Depends(get_db)):
    nombre_db = db.query(Usuario).filter(Usuario.nombre.like(f"%{name}%")).all()
    if not nombre_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return nombre_db
    
@router.put("/usuarios/{id}/desactivar",response_model  = UsuarioRespuesta)
def desactivar_usuario(id: int, usuario: dict = Depends(obtener_usuario_actual),db: Session = Depends(get_db)):
    if usuario["rol"] != "admin":
        raise HTTPException(status_code=403, detail="No tenés permiso")
    user_a_desactivar = db.query(Usuario).filter(Usuario.id == id).first()
    if user_a_desactivar is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    user_a_desactivar.activo = False
    db.commit()
    return user_a_desactivar

@router.get("/usuarios/{id}/ventas")
def ventas_usuario(id: int,usuario: dict = Depends(obtener_usuario_actual), db: Session = Depends(get_db)):
    usuario_db = db.query(Usuario).filter(Usuario.id == id).first()
    if usuario_db is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario_db.ventas

@router.put("/usuarios/{id}/cambiar/password")
def cambiar_password_usuario(id: int, passwords: CambiarPassword,usuario: dict = Depends(obtener_usuario_actual), db: Session = Depends(get_db)):
    usuario_db = db.query(Usuario).filter(Usuario.id == id).first()
    if usuario_db is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    elif verificar_password(passwords.actual, usuario_db.password):
        pwd_hasheada = hashear_password(passwords.nueva)
        usuario_db.password = pwd_hasheada
        db.commit()
        return {"mensaje": "password cambiada"}
    else:
       raise HTTPException(status_code=400, detail="password incorrecta") 

@router.post("/usuarios/login")
def verificar_usuario(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario_db = db.query(Usuario).filter(Usuario.email == form.username).first()
    if usuario_db is None:
        raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")
    if not verificar_password(form.password, usuario_db.password):
        raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")
    if not usuario_db.activo:
        raise HTTPException(status_code=403, detail="Usuario inactivo, contacte al administrador")
    return {"access_token": crear_token({"id": usuario_db.id, "rol": usuario_db.rol}), "token_type": "bearer"}