from sqlalchemy import select, func
from sqlalchemy.orm import joinedload
from ORM.conexion import Session
from ORM.modelos import Categoria, Equipo, Cliente, Arriendo
from ORM.validaciones import entero


def consultar_categorias():
    with Session() as session:
        consulta = select(Categoria).order_by(Categoria.id)
        categorias = session.scalars(consulta).all()
    return categorias


def buscar_categoria(id_categoria):
    entero(id_categoria, 'ID de categoría')
    with Session() as session:
        categoria = session.get(Categoria, id_categoria)
    return categoria


def consultar_equipos(solo_disponibles=False):
    consulta = select(Equipo).options(joinedload(Equipo.categoria)).order_by(Equipo.id)
    if solo_disponibles:
        consulta = consulta.where(Equipo.stock_disponible > 0)
    with Session() as session:
        equipos = session.scalars(consulta).all()
    return equipos


def buscar_equipo(id_equipo):
    entero(id_equipo, 'ID de equipo')
    with Session() as session:
        consulta = select(Equipo).options(joinedload(Equipo.categoria)).where(Equipo.id == id_equipo)
        equipo = session.scalar(consulta)
    return equipo


def consultar_clientes():
    with Session() as session:
        consulta = select(Cliente).order_by(Cliente.id)
        clientes = session.scalars(consulta).all()
    return clientes


def buscar_cliente(id_cliente):
    entero(id_cliente, 'ID de cliente')
    with Session() as session:
        cliente = session.get(Cliente, id_cliente)
    return cliente


def consultar_arriendos(solo_activos=False):
    consulta = (
        select(Arriendo)
        .options(joinedload(Arriendo.equipo), joinedload(Arriendo.cliente))
        .order_by(Arriendo.id.desc())
    )
    if solo_activos:
        consulta = consulta.where(Arriendo.estado == 'ACTIVO')
    with Session() as session:
        arriendos = session.scalars(consulta).all()
    return arriendos


def buscar_arriendo(id_arriendo):
    entero(id_arriendo, 'ID de arriendo')
    with Session() as session:
        consulta = (
            select(Arriendo)
            .options(joinedload(Arriendo.equipo), joinedload(Arriendo.cliente))
            .where(Arriendo.id == id_arriendo)
        )
        arriendo = session.scalar(consulta)
    return arriendo


def consultar_estadisticas():
    with Session() as session:
        consulta_categorias = (
            select(Categoria.id, Categoria.nombre, func.count(Arriendo.id))
            .select_from(Categoria)
            .join(Equipo, Equipo.categoria_id == Categoria.id)
            .join(Arriendo, Arriendo.equipo_id == Equipo.id)
            .group_by(Categoria.id, Categoria.nombre)
            .order_by(Categoria.nombre)
        )
        consulta_equipos = (
            select(Equipo.id, Equipo.nombre, func.count(Arriendo.id))
            .join(Arriendo, Arriendo.equipo_id == Equipo.id)
            .group_by(Equipo.id, Equipo.nombre)
            .order_by(func.count(Arriendo.id).desc(), Equipo.id)
            .limit(10)
        )
        por_categoria = session.execute(consulta_categorias).all()
        por_equipo = session.execute(consulta_equipos).all()
    return por_categoria, por_equipo
