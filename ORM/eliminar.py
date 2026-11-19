from sqlalchemy import select, func
from ORM.conexion import Session
from ORM.modelos import Categoria, Equipo, Cliente, Arriendo
from ORM.validaciones import entero


def eliminar_categoria(id_categoria):
    entero(id_categoria, 'ID de categoría')
    with Session.begin() as session:
        categoria = session.get(Categoria, id_categoria)
        if categoria is None:
            return False
        cantidad = session.scalar(
            select(func.count(Equipo.id)).where(Equipo.categoria_id == id_categoria)
        )
        if cantidad > 0:
            raise ValueError('La categoría tiene equipos asociados.')
        session.delete(categoria)
    return True


def eliminar_equipo(id_equipo):
    entero(id_equipo, 'ID de equipo')
    with Session.begin() as session:
        equipo = session.get(Equipo, id_equipo)
        if equipo is None:
            return False
        cantidad = session.scalar(
            select(func.count(Arriendo.id)).where(Arriendo.equipo_id == id_equipo)
        )
        if cantidad > 0:
            raise ValueError('El equipo tiene historial de arriendos.')
        session.delete(equipo)
    return True


def eliminar_cliente(id_cliente):
    entero(id_cliente, 'ID de cliente')
    with Session.begin() as session:
        cliente = session.get(Cliente, id_cliente)
        if cliente is None:
            return False
        cantidad = session.scalar(
            select(func.count(Arriendo.id)).where(Arriendo.cliente_id == id_cliente)
        )
        if cantidad > 0:
            raise ValueError('El cliente tiene historial de arriendos.')
        session.delete(cliente)
    return True
