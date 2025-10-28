API Tienda – FastAPI + SQLAlchemy

Esta API permite gestionar categorías y productos de una tienda.
Cada producto pertenece a una categoría (relación 1:N).
Incluye operaciones CRUD completas y control de stock.

Tecnologías utilizadas

Python 
FastAPI
SQLAlchemy
Uvicorn
SQLite (base de datos local)
Pydantic

Instalación y configuración
Clonar el proyecto

Abre tu terminal y ejecuta:

git clone https://github.com/Kevincue12/Parcial-Tiendas


Crear y activar entorno virtual
# Crear el entorno virtual
python -m venv venv

# Activar (Windows)
venv\Scripts\activate

# Activar (Linux / macOS)
source venv/bin/activate

Instalar dependencias
pip install -r requirements.txt


Archivo requirements.txt:

fastapi
uvicorn
sqlalchemy
pydantic

Estructura del proyecto

Asegúrate de tener la siguiente estructura de archivos:

Parcial Tiendas/
│
├── main.py
├── database.py
├── models.py
├── crud_categorias.py
├── crud_productos.py
├── schemas.py
├── requirements.txt
└── tienda.db   (se crea automáticamente al ejecutar el proyecto)

Ejecutar la aplicación
uvicorn main:app --reload

Probar la API

Abre en tu navegador:

http://127.0.0.1:8000/docs

Allí verás la documentación interactiva Swagger donde puedes:
Crear categorías
Listarlas
Actualizarlas
Desactivarlas
Crear productos
Restar stock
Ver la relación categoría-producto

Endpoints principales

Categorías
| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/categorias/` | Crear una nueva categoría |
| `GET`  | `/categorias/` | Listar todas las categorías |
| `GET`  | `/categorias/{id}` | Obtener una categoría por ID |
| `PUT`  | `/categorias/{id}` | Actualizar una categoría |
| `PUT`  | `/categorias/{id}/desactivar` | Desactivar una categoría |

Productos
| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/productos/` | Crear un nuevo producto |
| `GET`  | `/productos/` | Listar todos los productos activos |
| `GET`  | `/productos/{id}` | Obtener un producto por ID |
| `PUT`  | `/productos/{id}` | Actualizar un producto |
| `PUT`  | `/productos/{id}/desactivar` | Desactivar un producto |
| `PUT`  | `/productos/{id}/restar-stock/{cantidad}` | Restar una cantidad al stock del producto (sin permitir negativos) |

Validaciones importantes

No se puede crear ni actualizar un producto con stock < 0.
No se puede crear un producto si su categoría está inactiva.
Si intentas restar más stock del disponible, la API devuelve un error.
Al desactivar una categoría, sus productos permanecen activos (no se eliminan).

Ejemplo rápido
Crear categoría:
POST /categorias/
{
  "nombre": "Lácteos",
  "descripcion": "Productos derivados de la leche"
}

Crear producto:
POST /productos/
{
  "nombre": "Yogur natural",
  "precio": 3500,
  "stock": 20,
  "descripcion": "Yogur sin azucar",
  "categoria_id": 1
}