from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, crud_categorias, crud_productos, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Tienda - Categorías y Productos")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/categorias/", response_model=schemas.CategoriaResponse)
def crear_categoria(categoria: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    return crud_categorias.crear_categoria(db, categoria)

@app.get("/categorias/", response_model=list[schemas.CategoriaResponse])
def listar_categorias(db: Session = Depends(get_db)):
    return crud_categorias.listar_categorias(db)

@app.get("/categorias/{categoria_id}", response_model=schemas.CategoriaResponse)
def obtener_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = crud_categorias.obtener_categoria(db, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria

@app.put("/categorias/{categoria_id}", response_model=schemas.CategoriaResponse)
def actualizar_categoria(categoria_id: int, datos: schemas.CategoriaUpdate, db: Session = Depends(get_db)):
    categoria = crud_categorias.actualizar_categoria(db, categoria_id, datos)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria

@app.put("/categorias/{categoria_id}/desactivar", response_model=schemas.CategoriaResponse)
def desactivar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = crud_categorias.desactivar_categoria(db, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria

@app.post("/productos/", response_model=schemas.ProductoResponse)
def crear_producto(producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    try:
        return crud_productos.crear_producto(db, producto)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/productos/", response_model=list[schemas.ProductoResponse])
def listar_productos(db: Session = Depends(get_db)):
    return crud_productos.listar_productos(db)

@app.get("/productos/{producto_id}", response_model=schemas.ProductoResponse)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = crud_productos.obtener_producto(db, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@app.put("/productos/{producto_id}", response_model=schemas.ProductoResponse)
def actualizar_producto(producto_id: int, datos: schemas.ProductoUpdate, db: Session = Depends(get_db)):
    try:
        producto = crud_productos.actualizar_producto(db, producto_id, datos)
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return producto
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@app.put("/productos/{producto_id}/desactivar", response_model=schemas.ProductoResponse)
def desactivar_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = crud_productos.desactivar_producto(db, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@app.put("/productos/{producto_id}/restar-stock/{cantidad}", response_model=schemas.ProductoResponse)
def restar_stock(producto_id: int, cantidad: int, db: Session = Depends(get_db)):
    producto = crud_productos.restar_stock(db, producto_id, cantidad)
    if not producto:
        raise HTTPException(status_code=400, detail="No se pudo restar el stock (producto no encontrado o stock insuficiente)")
    return producto
