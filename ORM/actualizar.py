from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from ORM.conexion import Session
from ORM.modelos import Categoria, Equipo, Cliente, Arriendo
from ORM import validaciones


def actualizar_categoria(id_categoria, nombre, descripcion=''):
    validaciones.entero(id_categoria, 'ID de categoría')
    nombre = validaciones.texto(nombre, 'Nombre')
    descripcion = validaciones.texto(descripcion, 'Descripción', 300, obligatorio=False)

    try:
        with Session.begin() as session:
            categoria = session.get(Categoria, id_categoria)
            if categoria is None:
                return False
            categoria.nombre = nombre
            categoria.descripcion = descripcion
    except IntegrityError:
        raise ValueError("Ya existe una categoría con ese nombre.") from None
    return True


def actualizar_equipo(id_equipo, nombre, categoria_id, precio_diario, stock_total):
    validaciones.entero(id_equipo, 'ID de equipo')
    nombre = validaciones.texto(nombre, 'Nombre')
    validaciones.entero(categoria_id, 'ID de categoría')
    precio_diario = validaciones.precio(precio_diario)
    validaciones.entero(stock_total, 'Stock total', minimo=0)

    with Session.begin() as session:
        equipo = session.get(Equipo, id_equipo)
        if equipo is None:
            return False
        categoria = session.get(Categoria, categoria_id)
        if categoria is None:
            raise ValueError('La categoría no existe.')

        consulta = select(func.coalesce(func.sum(Arriendo.cantidad), 0)).where(
            Arriendo.equipo_id == id_equipo,
            Arriendo.estado == 'ACTIVO',
        )
        unidades_arrendadas = session.scalar(consulta)
        if stock_total < unidades_arrendadas:
            raise ValueError(
                f'Hay {unidades_arrendadas} unidades arrendadas. '
                'El stock total debe ser al menos esa cantidad.'
            )

        equipo.nombre = nombre
        equipo.categoria_id = categoria_id
        equipo.precio_diario = precio_diario
        equipo.stock_total = stock_total
        equipo.stock_disponible = stock_total - unidades_arrendadas

    return True


def actualizar_cliente(id_cliente, nombre, correo, telefono):
    validaciones.entero(id_cliente, 'ID de cliente')
    nombre = validaciones.texto(nombre, 'Nombre')
    correo = validaciones.correo(correo)
    telefono = validaciones.texto(telefono, 'Teléfono', 30)

    try:
        with Session.begin() as session:
            cliente = session.get(Cliente, id_cliente)
            if cliente is None:
                return False
            cliente.nombre = nombre
            cliente.correo = correo
            cliente.telefono = telefono
    except IntegrityError:
        raise ValueError('Ya existe un cliente con ese correo.') from None

    return True
