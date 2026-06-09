from sqlalchemy.orm import Session
from app.database import get_db
from app.models.productos import Producto
from app.schemas.productos import ProductoCrear, ProductoActualizar
from app.seguridad import obtener_usuario_actual 
from fastapi import HTTPException
from fastapi import Depends, APIRouter

router = APIRouter()

@router.get("/productos")
def listar_productos(usuario: dict = Depends(obtener_usuario_actual), db: Session = Depends(get_db)):
    return db.query(Producto).all()

@router.get("/productos/buscar/nombre/{name}")
def buscar_nombre_producto(name : str, usuario: dict = Depends(obtener_usuario_actual), db: Session = Depends(get_db)):
    #all no devuelve None si no encuentra nada, devuelve lista vacia
    nombre_db = db.query(Producto).filter(Producto.nombre.like(f"%{name}%")).all() 
    if not nombre_db: # lista vacia es false
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return nombre_db

@router.get("/productos/buscar/codigo/{code}")
def buscar_codigo_producto(code: str, usuario: dict = Depends(obtener_usuario_actual), db: Session = Depends(get_db)):
    codigo_db = db.query(Producto).filter(Producto.codigo == code).first()
    if not codigo_db: # lista vacia es false
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return codigo_db
    
@router.post("/productos/crear")
def crear_producto(producto: ProductoCrear,usuario: dict = Depends(obtener_usuario_actual), db: Session = Depends(get_db)):
    if usuario["rol"] != "admin":
        raise HTTPException(status_code=403, detail="No tenés permiso")
    nuevo_producto = Producto(nombre = producto.nombre, categoria = producto.categoria, stock = producto.stock, stock_min = producto.stock_min, precio = producto.precio, codigo = producto.codigo)
    db.add(nuevo_producto) # porque no existía en la base de datos
    db.commit() # guardo
    return nuevo_producto

@router.put("/productos/{id}")
def actualizar_producto(id: int, producto: ProductoActualizar,usuario: dict = Depends(obtener_usuario_actual), db: Session = Depends(get_db)):
    if usuario["rol"] != "admin":
        raise HTTPException(status_code=403, detail="No tenés permiso")
    producto_db = db.query(Producto).filter(Producto.id == id).first() # trae el objeto con ese id
    if producto_db is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    producto_dicc = producto.model_dump() # lo convierte a diccionario
    for campo, valor in producto_dicc.items():
        if valor is not None:
            setattr(producto_db, campo, valor)
    db.commit() # guardo
    return producto_db

@router.delete("/productos/{id}")
def eliminar_producto(id: int,usuario: dict = Depends(obtener_usuario_actual), db: Session = Depends(get_db)):
    if usuario["rol"] != "admin":
        raise HTTPException(status_code=403, detail="No tenés permiso")
    producto_db = db.query(Producto).filter(Producto.id == id).first() # trae el objeto con ese id
    if producto_db is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(producto_db)
    db.commit()
    return {"mensaje":"Producto eliminado!" }

