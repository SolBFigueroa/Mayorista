from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.ventas import Venta, DetalleVenta
from app.schemas.ventas import VentaCrear, DetalleCrear
from app.models.productos import Producto
from app.seguridad import obtener_usuario_actual 
from datetime import date
from fastapi import HTTPException
from fastapi import Depends, APIRouter

router = APIRouter()

@router.get("/ventas/")
def listar_ventas(usuario: dict = Depends(obtener_usuario_actual), db: Session = Depends(get_db)):
    lista = db.query(Venta).all()
    return lista

@router.post("/ventas/agregar/")
def agregar_venta(venta : VentaCrear,usuario: dict = Depends(obtener_usuario_actual), db: Session = Depends(get_db)):
    nueva_venta = Venta(user_id = venta.user_id, tipo_entrega= venta.tipo_entrega)
    db.add(nueva_venta)
    db.commit()
    return nueva_venta

@router.get("/ventas/detalles/{id_venta}")
def listar_detalles_venta(id_venta : int,usuario: dict = Depends(obtener_usuario_actual), db: Session = Depends(get_db)):
    venta_db = db.query(Venta).filter(Venta.id == id_venta).first()
    if venta_db is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return venta_db.detalles

@router.get("/ventas/buscar/{fecha_inicio}/{fecha_fin}")
def buscar_por_fechas_ventas(fecha_inicio: date, fecha_fin: date,usuario: dict = Depends(obtener_usuario_actual), db: Session = Depends(get_db)):
    ventas_db = db.query(Venta).filter(Venta.fecha >= fecha_inicio, Venta.fecha <= fecha_fin).all()
    return ventas_db

@router.get("/ventas/nombre/{name}/tickets/")
def buscar_ventas_por_producto(name: str,usuario: dict = Depends(obtener_usuario_actual), db: Session = Depends(get_db)):
    producto_db = db.query(Producto).filter(Producto.nombre == name).first()
    if not producto_db:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto_db.detalles_venta

@router.post("/ventas/nuevo/detalle/producto/{id_venta}")
def agregar_detalle(id_venta: int, nuevo_detalle : DetalleCrear,usuario: dict = Depends(obtener_usuario_actual), db: Session = Depends(get_db)):
    producto_db = db.query(Producto).filter(Producto.codigo == nuevo_detalle.codigo).first() #existe producto
    if producto_db is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    venta_db = db.query(Venta).filter(Venta.id == id_venta).first() #existe venta
    if venta_db is None:
        raise HTTPException(status_code=404, detail="VentaId no encontrado")
    
    for detalle in venta_db.detalles:
        if detalle.producto.codigo == nuevo_detalle.codigo:
            return {"mensaje": "Ya fue registrado el producto previamente."}
    stock_actual = producto_db.stock
    compra = nuevo_detalle.cantidad
    alertas = []
    if stock_actual >= compra:
        stock_actualizado = stock_actual - compra
        producto_db.stock = stock_actualizado
        nuevo_detalle = DetalleVenta(venta_id = id_venta, precio_unitario = producto_db.precio ,producto_id = producto_db.id, cantidad = nuevo_detalle.cantidad, subtotal = producto_db.precio * compra) #NO -> subtotal = precio * cantidad (SON ATRIBUTOS!)
        db.add(nuevo_detalle)
        if stock_actualizado <= producto_db.stock_min:
            alertas.append(f"{producto_db.nombre} llegó al stock mínimo")
            mensaje = "Stock actualizado con alerta"
        else:
            mensaje =  "Stock actualizado"
        venta_db.total += nuevo_detalle.subtotal
        db.commit()
    else:
        mensaje = "No hay stock suficiente"
    return {"mensaje": mensaje, "alertas": alertas}

@router.delete("/ventas/borrar/detalle/{detalle_id}")
def borrar_detalle(detalle_id: int, usuario: dict = Depends(obtener_usuario_actual),db: Session = Depends(get_db) ):
    detalle_db = db.query(DetalleVenta).filter(DetalleVenta.id == detalle_id).first()
    if detalle_db is None:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    #sacar el subtotal del producto de la venta_id
    detalle_db.venta.total -= detalle_db.subtotal
    #actualizar stock del producto
    detalle_db.producto.stock += detalle_db.cantidad
    #borrar objeto detalle_db
    db.delete(detalle_db)
    db.commit()
    return {"mensaje":"Detalle eliminado!" }

@router.put("/ventas/editar/detalle/{detalle_id}")
def editar_detalle(detalle_id: int, cantidad_nueva : int, usuario: dict = Depends(obtener_usuario_actual),db: Session = Depends(get_db)):
    detalle_db = db.query(DetalleVenta).filter(DetalleVenta.id == detalle_id).first()
    if detalle_db is None:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    detalle_db.cantidad = cantidad_nueva
    detalle_db.venta.total -= detalle_db.subtotal
    detalle_db.subtotal = detalle_db.precio_unitario * cantidad_nueva
    detalle_db.venta.total += detalle_db.subtotal
    db.commit()
    return detalle_db

# Solo admin
@router.get("/ventas/reporte/acumulacion/{fecha_inicio}/{fecha_fin}")
def reporte_por_periodo_ventas(fecha_inicio: date, fecha_fin: date,usuario: dict = Depends(obtener_usuario_actual), db: Session = Depends(get_db)):
    if usuario["rol"] != "admin":
        raise HTTPException(status_code=403, detail="No tenés permiso")
    ventas_db = db.query(Venta).filter(Venta.fecha >= fecha_inicio, Venta.fecha <= fecha_fin).all() # siempre devuelve una lista iterable
    total_periodo = 0
    if not ventas_db:
        raise HTTPException(status_code=404, detail="No hay ventas en ese período")
    for venta in ventas_db:
        total_periodo += venta.total
    return total_periodo

@router.get("/ventas/reporte/productos/{fecha_inicio}/{fecha_fin}") #admin elija cuantos quiere ver
def reporte_productos_mas_vendidos(fecha_inicio: date, fecha_fin: date,usuario: dict = Depends(obtener_usuario_actual),db: Session = Depends(get_db)):
    if usuario["rol"] != "admin":
        raise HTTPException(status_code=403, detail="No tenés permiso")
    ventas_db = db.query(Venta).filter(func.date(Venta.fecha) >= fecha_inicio, func.date(Venta.fecha) <= fecha_fin).all()
    dicc_producto_cantidad = {}
    for venta in ventas_db:
        detalles_db = venta.detalles
        for detalle in detalles_db:
            producto_nombre = detalle.producto.nombre
            if producto_nombre in dicc_producto_cantidad:
                dicc_producto_cantidad[producto_nombre] += detalle.cantidad
            else:
                dicc_producto_cantidad[producto_nombre] = detalle.cantidad
    ordenado = sorted(dicc_producto_cantidad.items(), key=lambda x: x[1], reverse=True)
    return ordenado
    
           











