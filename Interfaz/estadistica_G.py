from matplotlib.ticker import MaxNLocator
from ORM.consultar import consultar_estadisticas


def dibujar_graficas(figura):
    figura.clear()

    datos = consultar_estadisticas()
    titulos = ["Arriendos por categoría", "Equipos más arrendados"]
    ejes = figura.subplots(1, 2)

    for eje, filas, titulo in zip(ejes, datos, titulos):
        nombres = [f"{nombre} (ID {id_})" for id_, nombre, total in filas]
        cantidades = [total for id_, nombre, total in filas]

        eje.barh(nombres, cantidades)
        eje.set_title(titulo)
        eje.set_xlabel("Número de arriendos")
        eje.invert_yaxis()
        eje.xaxis.set_major_locator(MaxNLocator(integer=True))

        if not filas:
            eje.text(
                0.5, 0.5, "Sin arriendos",
                transform=eje.transAxes, ha="center",
            )