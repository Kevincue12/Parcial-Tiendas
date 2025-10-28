from fastapi import FastAPI, Depends, HTTPException, status
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



@app.post("/categorias/", response_model=schemas.CategoriaResponse, status_code=status.HTTP_201_CREATED)
def crear_categoria(categoria: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    # Evitar duplicados (409)
    existente = db.query(models.Categoria).filter(models.Categoria.nombre == categoria.nombre).first()
    if existente:
        raise HTTPException(status_code=409, detail="Ya existe una categoría con ese nombre.")

    nueva = crud_categorias.crear_categoria(db, categoria)
    return nueva


@app.get("/categorias/", response_model=list[schemas.CategoriaResponse])
def buscar_categorias_con_nombre (nombre: str | None = None, db: Session = Depends(get_db)):
    if nombre:
        categorias = crud_categorias.buscar_categorias_por_nombre(db, nombre)
        if not categorias:
            raise HTTPException(status_code=404, detail="No se encontraron categorías con ese nombre.")
        return categorias
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



@app.post("/productos/", response_model=schemas.ProductoResponse, status_code=status.HTTP_201_CREATED)
def crear_producto(producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    # Evitar duplicados (409)
    existente = db.query(models.Producto).filter(models.Producto.nombre == producto.nombre).first()
    if existente:
        raise HTTPException(status_code=409, detail="Ya existe un producto con ese nombre.")

    try:
        nuevo = crud_productos.crear_producto(db, producto)
        return nuevo
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/categorias/", response_model=list[schemas.CategoriaResponse])
def listar_categorias(db: Session = Depends(get_db)):
    return crud_categorias.listar_categorias(db)



@app.get("/productos/", response_model=list[schemas.ProductoResponse])
def buscar_productos_con_nombre (nombre: str | None = None, db: Session = Depends(get_db)):
    if nombre:
        productos = crud_productos.buscar_productos_por_nombre(db, nombre)
        if not productos:
            raise HTTPException(status_code=404, detail="No se encontraron productos con ese nombre.")
        return productos
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
    try:
        producto = crud_productos.restar_stock(db, producto_id, cantidad)
        return producto
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/productos/", response_model=list[schemas.ProductoResponse])
def listar_productos(db: Session = Depends(get_db)):
    return crud_productos.listar_productos(db)