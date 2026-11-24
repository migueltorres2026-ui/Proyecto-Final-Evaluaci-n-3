from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from Interfaz.estadistica_G import dibujar_graficas


class FormularioEstadisticas(ttk.Frame):
    def __init__(self, padre):
        super().__init__(padre, padding=10)

        ttk.Button(
            self,
            text="Actualizar gráficas",
            command=self.actualizar,
        ).pack(pady=5)

        self.figura = Figure(figsize=(10, 5), layout="constrained")
        self.lienzo = FigureCanvasTkAgg(self.figura, master=self)
        self.lienzo.get_tk_widget().pack(fill="both", expand=True)

    def actualizar(self):
        dibujar_graficas(self.figura)
        self.lienzo.draw_idle()