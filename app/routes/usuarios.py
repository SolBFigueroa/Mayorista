from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from app.database import get_db
from app.models.usuarios import Usuario
from app.schemas.usuarios import UsuarioCrear, CambiarPassword
from fastapi import HTTPException

router = APIRouter()

@router.get("/usuarios")
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()

@router.post("/usuarios")
def crear_usuario(usuario: UsuarioCrear, db: Session = Depends(get_db)):
    nuevo_usuario = Usuario(nombre = usuario.nombre, apellido = usuario.apellido, email = usuario.email, password = usuario.password, rol = usuario.rol)
    db.add(nuevo_usuario) 
    db.commit()
    return nuevo_usuario

@router.put("/usuarios/{id}/desactivar")
def desactivar_usuario(id: int, db: Session = Depends(get_db)):
    user_a_desactivar = db.query(Usuario).filter(Usuario.id == id).first()
    if user_a_desactivar is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    user_a_desactivar.activo = False
    db.commit()
    return user_a_desactivar

@router.get("/usuarios/buscar/{name}")
def buscar_nombre_usuario(name: str , db: Session = Depends(get_db)):
    nombre_db = db.query(Usuario).filter(Usuario.nombre.like(f"%{name}%")).all()
    if not nombre_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return nombre_db

@router.get("/usuarios/{id}/ventas")
def ventas_usuario(id: int, db: Session = Depends(get_db)):
    usuario_db = db.query(Usuario).filter(Usuario.id == id).first()
    if usuario_db is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario_db.ventas

@router.put("/usuarios/{id}/cambiar/password")
def cambiar_password_usuario(id: int, passwords: CambiarPassword, db: Session = Depends(get_db)):
    usuario_db = db.query(Usuario).filter(Usuario.id == id).first()
    if usuario_db is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    elif usuario_db.password == passwords.password_actual:
        usuario_db.password = passwords.password_nueva
        db.commit()
        return {"mensaje": "password cambiada"}
    else:
       raise HTTPException(status_code=400, detail="password incorrecta") 


