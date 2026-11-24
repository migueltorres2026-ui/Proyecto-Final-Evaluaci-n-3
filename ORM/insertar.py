from sqlalchemy.exc import IntegrityError
from ORM.conexion import Session
from ORM.modelos import Categoria, Equipo, Cliente
from ORM import validaciones
from ORM.factory_method import obtener_creador


def registrar_categoria(nombre, descripcion=''):
    nombre = validaciones.texto(nombre, 'Nombre')
    descripcion = validaciones.texto(descripcion, 'Descripción', 300, obligatorio=False)

    try:
        with Session.begin() as session:
            categoria = Categoria(nombre=nombre, descripcion=descripcion)
            session.add(categoria)
    except IntegrityError:
        raise ValueError('Ya existe una categoría con ese nombre.') from None

    return categoria


def registrar_equipo(nombre, categoria_id, precio_diario, stock_total):
    nombre = validaciones.texto(nombre, 'Nombre')
    validaciones.entero(categoria_id, 'ID de categoría')
    precio_diario = validaciones.precio(precio_diario)
    validaciones.entero(stock_total, 'Stock total', minimo=0)

    with Session.begin() as session:
        categoria = session.get(Categoria, categoria_id)
        if categoria is None:
            raise ValueError('La categoría no existe.')
        creador = obtener_creador(categoria.nombre)

        equipo = creador.crear_equipo(
            nombre=nombre,
            categoria_id=categoria_id,
            precio_diario=precio_diario,
            stock_total=stock_total,
        )
        session.add(equipo)

    return equipo


def registrar_cliente(nombre, correo, telefono):
    nombre = validaciones.texto(nombre, 'Nombre')
    correo = validaciones.correo(correo)
    telefono = validaciones.texto(telefono, 'Teléfono', 30)

    try:
        with Session.begin() as session:
            cliente = Cliente(nombre=nombre, correo=correo, telefono=telefono)
            session.add(cliente)
    except IntegrityError:
        raise ValueError('Ya existe un cliente con ese correo.') from None

    return cliente
