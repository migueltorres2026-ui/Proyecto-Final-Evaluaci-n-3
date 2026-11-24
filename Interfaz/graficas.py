import tkinter as tk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MaxNLocator
from ORM.consultar import consultar_estadisticas


def grafico_arriendos_por_categoria(padre):
    por_categoria, por_equipo = consultar_estadisticas()

    _mostrar_grafico(
        padre,
        por_categoria,
        "Arriendos por categoría",
    )


def grafico_top_equipos(padre):
    por_categoria, por_equipo = consultar_estadisticas()

    _mostrar_grafico(
        padre,
        por_equipo,
        "Top 10 equipos más arrendados",
    )


def _mostrar_grafico(padre, datos, titulo):
    if not datos:
        messagebox.showinfo(
            "Gráficos",
            "Todavía no hay arriendos registrados.",
            parent=padre,
        )
        return

    nombres = []
    cantidades = []

    for identificador, nombre, cantidad in datos:
        nombres.append(f"{nombre} (ID {identificador})")
        cantidades.append(cantidad)

    figura = Figure(figsize=(8, 5), dpi=100)
    eje = figura.add_subplot(111)
    eje.barh(nombres, cantidades, color="steelblue")
    eje.invert_yaxis()
    eje.set_title(titulo)
    eje.set_xlabel("Número de arriendos")
    eje.set_xlim(left=0)

    eje.xaxis.set_major_locator(MaxNLocator(integer=True))
    figura.tight_layout()

    ventana = tk.Toplevel(padre)
    ventana.title(titulo)
    ventana.geometry("850x550")

    lienzo = FigureCanvasTkAgg(figura, master=ventana)
    lienzo.draw()
    lienzo.get_tk_widget().pack(fill="both", expand=True)

    ventana.lienzo = lienzo