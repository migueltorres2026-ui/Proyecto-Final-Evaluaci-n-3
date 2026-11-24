from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal

from ORM.modelos import Equipo


@dataclass
class ProductoEquipo:
    nombre: str
    categoria_id: int
    precio_diario: Decimal
    stock_total: int

    def a_modelo(self):
        return Equipo(
            nombre=self.nombre,
            categoria_id=self.categoria_id,
            precio_diario=self.precio_diario,
            stock_total=self.stock_total,
            stock_disponible=self.stock_total,
        )
class Balon(ProductoEquipo):
    pass


class Raqueta(ProductoEquipo):
    pass


class OtroEquipo(ProductoEquipo):
    pass


class CreadorEquipo(ABC):
    @abstractmethod
    def crear_producto(self, **datos):
        pass

    def crear_equipo(self, **datos):
        producto = self.crear_producto(**datos)
        return producto.a_modelo()


class CreadorBalon(CreadorEquipo):
    def crear_producto(self, **datos):
        return Balon(**datos)


class CreadorRaqueta(CreadorEquipo):
    def crear_producto(self, **datos):
        return Raqueta(**datos)


class CreadorOtroEquipo(CreadorEquipo):
    def crear_producto(self, **datos):
        return OtroEquipo(**datos)


def obtener_creador(nombre_categoria):
    nombre = nombre_categoria.strip().casefold()

    if nombre in ("balón", "balon", "balones"):
        return CreadorBalon()

    if nombre in ("raqueta", "raquetas"):
        return CreadorRaqueta()

    return CreadorOtroEquipo()