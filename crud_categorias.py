from sqlalchemy.orm import Session
from models import Categoria
from schemas import CategoriaCreate, CategoriaUpdate

def crear_categoria(db: Session, categoria: CategoriaCreate):
    nueva = Categoria(nombre=categoria.nombre, descripcion=categoria.descripcion)
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def listar_categorias(db: Session):
    return db.query(Categoria).all()

def obtener_categoria(db: Session, categoria_id: int):
    return db.query(Categoria).filter(Categoria.id == categoria_id).first()

def actualizar_categoria(db: Session, categoria_id: int, datos: CategoriaUpdate):
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        return None
    for campo, valor in datos.dict(exclude_unset=True).items():
        setattr(categoria, campo, valor)
    db.commit()
    db.refresh(categoria)
    return categoria

def desactivar_categoria(db: Session, categoria_id: int):
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        return None
    categoria.activa = False
    db.commit()
    db.refresh(categoria)
    return categoria


def buscar_categorias_por_nombre(db: Session, nombre: str):
    return db.query(Categoria).filter(
        Categoria.nombre.ilike(f"%{nombre}%")
    ).all()
