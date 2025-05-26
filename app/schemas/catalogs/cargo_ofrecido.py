"""Esquemas Pydantic para la entidad Cargo Ofrecido."""

from pydantic import BaseModel


class CargoOfrecidoBase(BaseModel):
    """
    Base común para creación y respuesta de cargos ofrecidos.

    Atributos:
        nombre_cargo (str): Nombre del cargo ofrecido.
    """
    nombre_cargo: str
    # id_categoria: int  # Comentado: incluir si se implementa relación con categorías


class CargoOfrecidoCreate(CargoOfrecidoBase):
    """
    Esquema para crear un nuevo cargo ofrecido.
    """
    pass


class CargoOfrecidoResponse(CargoOfrecidoBase):
    """
    Esquema de respuesta al consultar un cargo ofrecido.

    Atributos:
        id_cargo (int): Identificador único del cargo.
    """
    id_cargo: int

    class Config:
        from_attributes = True  # Habilita la conversión desde modelos ORM
