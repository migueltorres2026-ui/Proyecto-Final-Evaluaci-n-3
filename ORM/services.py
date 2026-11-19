from sqlalchemy import update
from ORM.conexion import Session
from ORM.modelos import Equipo, Cliente, Arriendo
from ORM import validaciones


def registrar_arriendo(equipo_id, cliente_id, fecha_inicio, fecha_fin_prevista, cantidad):
    validaciones.entero(equipo_id, "ID de equipo")
    validaciones.entero(cliente_id, "ID de cliente")
    validaciones.entero(cantidad, "Cantidad")
    validaciones.fechas(fecha_inicio, fecha_fin_prevista)

    with Session.begin() as session:
        equipo = session.get(Equipo, equipo_id)
        if equipo is None:
            raise ValueError("El equipo no existe.")
        cliente = session.get(Cliente, cliente_id)
        if cliente is None:
            raise ValueError("El cliente no existe.")

        # El descuento exige que todavía queden unidades suficientes.
        descuento = (
            update(Equipo)
            .where(Equipo.id == equipo_id, Equipo.stock_disponible >= cantidad)
            .values(stock_disponible=Equipo.stock_disponible - cantidad)
        )
        resultado = session.execute(descuento)
        if resultado.rowcount != 1:
            raise ValueError('Stock insuficiente.')

        arriendo = Arriendo(
            equipo_id = equipo_id,
            cliente_id = cliente_id,
            fecha_inicio = fecha_inicio,
            fecha_fin_prevista = fecha_fin_prevista,
            cantidad = cantidad,
            estado = "ACTIVO",
        )
        session.add(arriendo)

    return arriendo


def devolver_arriendo(id_arriendo):
    validaciones.entero(id_arriendo, "ID de arriendo")

    with Session.begin() as session:
        arriendo = session.get(Arriendo, id_arriendo)
        if arriendo is None:
            raise ValueError('El arriendo no existe.')

        cambio_estado = (
            update(Arriendo)
            .where(Arriendo.id == id_arriendo, Arriendo.estado == "ACTIVO")
            .values(estado="DEVUELTO")
        )
        resultado = session.execute(cambio_estado)
        if resultado.rowcount != 1:
            raise ValueError("Ese arriendo ya fue devuelto.")

        reposicion = (
            update(Equipo)
            .where(
                Equipo.id == arriendo.equipo_id,
                Equipo.stock_disponible + arriendo.cantidad <= Equipo.stock_total,
            )
            .values(stock_disponible=Equipo.stock_disponible + arriendo.cantidad)
        )
        resultado = session.execute(reposicion)
        if resultado.rowcount != 1:
            raise ValueError("Stock inconsistente. La devolución se revirtió.")

    return arriendo
