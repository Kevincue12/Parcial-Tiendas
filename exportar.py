from sqlalchemy.orm import Session
from openpyxl import Workbook
from models import Producto, Categoria

def exportar_datos_a_excel(db: Session, ruta_archivo: str = "datos_tienda.xlsx"):
    """
    Exporta los datos de categorías y productos a un archivo Excel (.xlsx).
    """
    wb = Workbook()

    ws_categorias = wb.active
    ws_categorias.title = "Categorias"
    ws_categorias.append(["ID", "Nombre", "Descripción", "Activa"])

    categorias = db.query(Categoria).all()
    for c in categorias:
        ws_categorias.append([c.id, c.nombre, c.descripcion, "Sí" if c.activa else "No"])

    ws_productos = wb.create_sheet("Productos")
    ws_productos.append(["ID", "Nombre", "Precio", "Stock", "Descripción", "Categoría ID", "Activa"])

    productos = db.query(Producto).all()
    for p in productos:
        ws_productos.append([
            p.id,
            p.nombre,
            p.precio,
            p.stock,
            p.descripcion,
            p.categoria_id,
            "Sí" if p.activa else "No"
        ])

    wb.save(ruta_archivo)
    return ruta_archivo
