from pydantic import BaseModel
from typing import Optional, List


class CategoriaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaUpdate(BaseModel):
    nombre: Optional[str]
    descripcion: Optional[str]
    activa: Optional[bool]

class CategoriaResponse(CategoriaBase):
    id: int
    activa: bool

    class Config:
        orm_mode = True


class ProductoBase(BaseModel):
    nombre: str
    precio: float
    stock: int
    descripcion: Optional[str] = None

class ProductoCreate(ProductoBase):
    categoria_id: int

class ProductoUpdate(BaseModel):
    nombre: Optional[str]
    precio: Optional[float]
    stock: Optional[int]
    descripcion: Optional[str]
    activa: Optional[bool]

class ProductoResponse(ProductoBase):
    id: int
    activa: bool
    categoria: Optional[CategoriaResponse]  # 

    class Config:
        orm_mode = True
