from sqlalchemy.orm import Session
from models import Producto, Categoria
from schemas import ProductoCreate, ProductoUpdate

def crear_producto(db: Session, producto: ProductoCreate):
    categoria = db.query(Categoria).filter(
        Categoria.id == producto.categoria_id,
        Categoria.activa == True
    ).first()
    if not categoria:
        raise ValueError("La categoría no existe o está inactiva.")

    if producto.stock < 0:
        raise ValueError("El stock no puede ser negativo.")

    nuevo = Producto(**producto.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def listar_productos(db: Session):
    return db.query(Producto).filter(Producto.activa == True).all()


def obtener_producto(db: Session, producto_id: int):
    return db.query(Producto).filter(
        Producto.id == producto_id,
        Producto.activa == True
    ).first()


def actualizar_producto(db: Session, producto_id: int, datos: ProductoUpdate):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        return None

    if "stock" in datos.dict(exclude_unset=True) and datos.stock < 0:
        raise ValueError("El stock no puede ser negativo.")

    for key, value in datos.dict(exclude_unset=True).items():
        setattr(producto, key, value)

    db.commit()
    db.refresh(producto)
    return producto


def desactivar_producto(db: Session, producto_id: int):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        return None
    producto.activa = False
    db.commit()
    return producto


def restar_stock(db: Session, producto_id: int, cantidad: int):
    producto = db.query(Producto).filter(
        Producto.id == producto_id,
        Producto.activa == True
    ).first()

    if not producto:
        raise ValueError("El producto no existe o está inactivo.")

    if cantidad <= 0:
        raise ValueError("La cantidad a restar debe ser mayor que cero.")

    if producto.stock < cantidad:
        raise ValueError(f"No hay suficiente stock disponible ({producto.stock} unidades).")

    producto.stock -= cantidad
    db.commit()
    db.refresh(producto)
    return producto
