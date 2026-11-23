import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

from ORM import insertar, consultar, actualizar, eliminar
from ORM.conexion import engine
from ORM.modelos import Base

try:
    from ORM import services as servicio_arriendos_mod
except ImportError:
    servicio_arriendos_mod = None


class AplicacionArriendos(tk.Tk):
    def __init__(self, servicio_arriendos=None, graficos=None):
        super().__init__()
        self.servicio_arriendos = servicio_arriendos or servicio_arriendos_mod
        self.graficos = graficos
        Base.metadata.create_all(engine)

        self.title("Gestión de Arriendo Deportivo")
        self.geometry("1100x660")
        ttk.Style(self).theme_use("clam")

        self._armar_barra_superior()
        self._armar_pestanas()
        self.refrescar_todo()

    def _armar_barra_superior(self):
        top = ttk.Frame(self, padding=8)
        top.pack(fill="x")
        ttk.Label(top, text="Arriendo de Equipamiento Deportivo", font=("Segoe UI", 13, "bold")).pack(side="left")
        ttk.Button(top, text="Gráfico Categorías", command=lambda: self._ver_grafico("grafico_arriendos_por_categoria", 0)).pack(side="right", padx=3)
        ttk.Button(top, text="Gráfico Top Equipos", command=lambda: self._ver_grafico("grafico_top_equipos", 1)).pack(side="right", padx=3)
        ttk.Button(top, text="Refrescar", command=self.refrescar_todo).pack(side="right", padx=3)

    def _armar_pestanas(self):
        nb = ttk.Notebook(self, padding=6)
        nb.pack(fill="both", expand=True)

        self.tab_arr = ttk.Frame(nb, padding=8)
        self.tab_eq = ttk.Frame(nb, padding=8)
        self.tab_cat = ttk.Frame(nb, padding=8)
        self.tab_cli = ttk.Frame(nb, padding=8)
        self.tab_con = ttk.Frame(nb, padding=8)

        for tab, title in [
            (self.tab_arr, "Arriendos"),
            (self.tab_eq, "Equipos"),
            (self.tab_cat, "Categorías"),
            (self.tab_cli, "Clientes"),
            (self.tab_con, "Consultas"),
        ]:
            nb.add(tab, text=title)

        self._form_arriendos()
        self._form_equipos()
        self._form_categorias()
        self._form_clientes()
        self._form_consultas()

    
    def _form_arriendos(self):
        f = ttk.LabelFrame(self.tab_arr, text="Nuevo Arriendo", padding=8)
        f.pack(fill="x", pady=(0, 8))
        hoy = date.today().isoformat()

        self.cb_arr_cli = self._campo_combo(f, "Cliente:", 0, 0, 26)
        self.cb_arr_eq = self._campo_combo(f, "Equipo:", 0, 2, 30)
        self.e_arr_cant = self._campo_entry(f, "Cantidad:", 0, 4, 8)
        self.e_arr_ini = self._campo_entry(f, "Inicio:", 1, 0, 14, hoy)
        self.e_arr_fin = self._campo_entry(f, "Fin prev.:", 1, 2, 14, hoy)
        ttk.Button(f, text="Registrar", command=self._registrar_arriendo).grid(row=1, column=4, columnspan=2, padx=6)

        self.tree_arr = self._crear_tabla(self.tab_arr, ["ID", "Cliente", "Equipo", "Cant.", "Inicio", "Fin", "Estado"])
        ttk.Button(self.tab_arr, text="Devolver Seleccionado", command=self._devolver_arriendo).pack(anchor="w", pady=6)

    
    def _form_equipos(self):
        f = ttk.LabelFrame(self.tab_eq, text="Equipo", padding=8)
        f.pack(fill="x", pady=(0, 8))

        self.e_eq_nom = self._campo_entry(f, "Nombre:", 0, 0, 22)
        self.cb_eq_cat = self._campo_combo(f, "Categoría:", 0, 2, 24)
        self.e_eq_pre = self._campo_entry(f, "Precio/día:", 1, 0, 12)
        self.e_eq_stk = self._campo_entry(f, "Stock total:", 1, 2, 12)
        self._botones_crud(f, 1, 4, self._crear_eq, self._act_eq, self._elim_eq)

        self.tree_eq = self._crear_tabla(self.tab_eq, ["ID", "Nombre", "Categoría", "Precio", "Total", "Disp."])
        self.tree_eq.bind("<<TreeviewSelect>>", lambda _: self._llenar_entradas(self.tree_eq, [(self.e_eq_nom, 1), (self.e_eq_pre, 3), (self.e_eq_stk, 4)]))

    
    def _form_categorias(self):
        f = ttk.LabelFrame(self.tab_cat, text="Categoría", padding=8)
        f.pack(fill="x", pady=(0, 8))

        self.e_cat_nom = self._campo_entry(f, "Nombre:", 0, 0, 22)
        self.e_cat_desc = self._campo_entry(f, "Descripción:", 0, 2, 34)
        self._botones_crud(f, 0, 4, self._crear_cat, self._act_cat, self._elim_cat)

        self.tree_cat = self._crear_tabla(self.tab_cat, ["ID", "Nombre", "Descripción"])
        self.tree_cat.bind("<<TreeviewSelect>>", lambda _: self._llenar_entradas(self.tree_cat, [(self.e_cat_nom, 1), (self.e_cat_desc, 2)]))

    
    def _form_clientes(self):
        f = ttk.LabelFrame(self.tab_cli, text="Cliente", padding=8)
        f.pack(fill="x", pady=(0, 8))

        self.e_cli_nom = self._campo_entry(f, "Nombre:", 0, 0, 20)
        self.e_cli_cor = self._campo_entry(f, "Correo:", 0, 2, 24)
        self.e_cli_tel = self._campo_entry(f, "Teléfono:", 0, 4, 16)
        self._botones_crud(f, 1, 2, self._crear_cli, self._act_cli, self._elim_cli)

        self.tree_cli = self._crear_tabla(self.tab_cli, ["ID", "Nombre", "Correo", "Teléfono"])
        self.tree_cli.bind("<<TreeviewSelect>>", lambda _: self._llenar_entradas(self.tree_cli, [(self.e_cli_nom, 1), (self.e_cli_cor, 2), (self.e_cli_tel, 3)]))

    
    def _form_consultas(self):
        top = ttk.Frame(self.tab_con)
        top.pack(fill="x", pady=(0, 6))
        ttk.Button(top, text="Equipos Disponibles", command=lambda: self._cargar_consulta("disp")).pack(side="left", padx=3)
        ttk.Button(top, text="Arriendos Activos", command=lambda: self._cargar_consulta("act")).pack(side="left", padx=3)
        ttk.Button(top, text="Historial", command=lambda: self._cargar_consulta("hist")).pack(side="left", padx=3)
        self.tree_con = self._crear_tabla(self.tab_con, ["C1", "C2", "C3", "C4", "C5"])

    
    def refrescar_todo(self):
        cats = consultar.consultar_categorias()
        self._rellenar_tree(self.tree_cat, [(c.id, c.nombre, c.descripcion or "") for c in cats])
        self._rellenar_combo(self.cb_eq_cat, [f"{c.id} - {c.nombre}" for c in cats])

        eqs = consultar.consultar_equipos(solo_disponibles=False)
        self._rellenar_tree(
            self.tree_eq,
            [(e.id, e.nombre, e.categoria.nombre if e.categoria else e.categoria_id, e.precio_diario, e.stock_total, e.stock_disponible) for e in eqs],
        )
        self._rellenar_combo(self.cb_arr_eq, [f"{e.id} - {e.nombre} (Disp: {e.stock_disponible})" for e in eqs])

        clis = consultar.consultar_clientes()
        self._rellenar_tree(self.tree_cli, [(c.id, c.nombre, c.correo, c.telefono or "") for c in clis])
        self._rellenar_combo(self.cb_arr_cli, [f"{c.id} - {c.nombre}" for c in clis])

        try:
            arrs = consultar.consultar_arriendos(solo_activos=False)
            self._rellenar_tree(
                self.tree_arr,
                [(a.id, a.cliente.nombre if a.cliente else a.cliente_id, a.equipo.nombre if a.equipo else a.equipo_id, a.cantidad, a.fecha_inicio, a.fecha_fin_prevista, a.estado) for a in arrs],
            )
        except Exception:
            pass

        self._cargar_consulta("disp")

    def _ejecutar(self, accion, ok_msg="Operación exitosa."):
        try:
            res = accion()
            if res is False:
                messagebox.showwarning("Aviso", "Registro no encontrado.")
                return
            messagebox.showinfo("Éxito", ok_msg)
            self.refrescar_todo()
        except ValueError as e:
            messagebox.showerror("Dato inválido", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _crear_cat(self):
        self._ejecutar(lambda: insertar.registrar_categoria(self.e_cat_nom.get(), self.e_cat_desc.get()), "Categoría creada.")

    def _act_cat(self):
        cid = self._id_sel(self.tree_cat)
        if cid:
            self._ejecutar(lambda: actualizar.actualizar_categoria(cid, self.e_cat_nom.get(), self.e_cat_desc.get()), "Categoría actualizada.")

    def _elim_cat(self):
        cid = self._id_sel(self.tree_cat)
        if cid:
            self._ejecutar(lambda: eliminar.eliminar_categoria(cid), "Categoría eliminada.")

    def _crear_eq(self):
        def accion():
            cat_id = self._id_combo(self.cb_eq_cat.get())
            precio = float(self.e_eq_pre.get().strip())
            stock = int(self.e_eq_stk.get().strip())
            return insertar.registrar_equipo(self.e_eq_nom.get(), cat_id, precio, stock)

        self._ejecutar(accion, "Equipo creado.")

    def _act_eq(self):
        eid = self._id_sel(self.tree_eq)
        if eid:
            def accion():
                cat_id = self._id_combo(self.cb_eq_cat.get())
                precio = float(self.e_eq_pre.get().strip())
                stock = int(self.e_eq_stk.get().strip())
                return actualizar.actualizar_equipo(eid, self.e_eq_nom.get(), cat_id, precio, stock)

            self._ejecutar(accion, "Equipo actualizado.")

    def _elim_eq(self):
        eid = self._id_sel(self.tree_eq)
        if eid:
            self._ejecutar(lambda: eliminar.eliminar_equipo(eid), "Equipo eliminado.")

    def _crear_cli(self):
        self._ejecutar(lambda: insertar.registrar_cliente(self.e_cli_nom.get(), self.e_cli_cor.get(), self.e_cli_tel.get()), "Cliente creado.")

    def _act_cli(self):
        cid = self._id_sel(self.tree_cli)
        if cid:
            self._ejecutar(lambda: actualizar.actualizar_cliente(cid, self.e_cli_nom.get(), self.e_cli_cor.get(), self.e_cli_tel.get()), "Cliente actualizado.")

    def _elim_cli(self):
        cid = self._id_sel(self.tree_cli)
        if cid:
            self._ejecutar(lambda: eliminar.eliminar_cliente(cid), "Cliente eliminado.")

    def _registrar_arriendo(self):
        fn = getattr(self.servicio_arriendos, "registrar_arriendo", None)
        if not callable(fn):
            messagebox.showwarning("Servicio no disponible", "No se encontró registrar_arriendo en ORM.services.")
            return

        def accion():
            equipo_id = self._id_combo(self.cb_arr_eq.get())
            cliente_id = self._id_combo(self.cb_arr_cli.get())
            fecha_inicio = date.fromisoformat(self.e_arr_ini.get().strip())
            fecha_fin_prevista = date.fromisoformat(self.e_arr_fin.get().strip())
            cantidad = int(self.e_arr_cant.get().strip())
            return fn(equipo_id, cliente_id, fecha_inicio, fecha_fin_prevista, cantidad)

        self._ejecutar(accion, "Arriendo registrado.")

    def _devolver_arriendo(self):
        aid = self._id_sel(self.tree_arr)
        if not aid:
            return
        fn = getattr(self.servicio_arriendos, "devolver_arriendo", None)
        if not callable(fn):
            messagebox.showwarning("Servicio no disponible", "No se encontró devolver_arriendo en ORM.services.")
            return
        self._ejecutar(lambda: fn(aid), "Arriendo devuelto.")

    def _cargar_consulta(self, tipo):
        if tipo == "disp":
            eqs = consultar.consultar_equipos(solo_disponibles=True)
            self._set_headers(self.tree_con, ["ID", "Equipo", "Categoría", "Precio", "Disponible"])
            self._rellenar_tree(self.tree_con, [(e.id, e.nombre, e.categoria.nombre if e.categoria else e.categoria_id, e.precio_diario, e.stock_disponible) for e in eqs])
        else:
            arrs = consultar.consultar_arriendos(solo_activos=(tipo == "act"))
            self._set_headers(self.tree_con, ["ID", "Cliente", "Equipo", "Cantidad", "Estado"])
            self._rellenar_tree(self.tree_con, [(a.id, a.cliente.nombre if a.cliente else a.cliente_id, a.equipo.nombre if a.equipo else a.equipo_id, a.cantidad, a.estado) for a in arrs])

    def _ver_grafico(self, metodo, idx_estadistica):
        fn = getattr(self.graficos, metodo, None)
        if callable(fn):
            fn()
        else:
            datos = consultar.consultar_estadisticas()[idx_estadistica]
            messagebox.showinfo("Estadísticas", "\n".join(f"{nom}: {cant}" for _, nom, cant in datos) or "Sin datos.")

    
    def _campo_entry(self, parent, label, r, c, w, inicial=""):
        ttk.Label(parent, text=label).grid(row=r, column=c, sticky="w", padx=3, pady=3)
        e = ttk.Entry(parent, width=w)
        if inicial:
            e.insert(0, inicial)
        e.grid(row=r, column=c + 1, padx=3, pady=3)
        return e

    def _campo_combo(self, parent, label, r, c, w):
        ttk.Label(parent, text=label).grid(row=r, column=c, sticky="w", padx=3, pady=3)
        cb = ttk.Combobox(parent, state="readonly", width=w)
        cb.grid(row=r, column=c + 1, padx=3, pady=3)
        return cb

    def _botones_crud(self, parent, r, c, f_crear, f_act, f_elim):
        box = ttk.Frame(parent)
        box.grid(row=r, column=c, columnspan=2, padx=4)
        ttk.Button(box, text="Crear", command=f_crear).pack(side="left", padx=2)
        ttk.Button(box, text="Actualizar", command=f_act).pack(side="left", padx=2)
        ttk.Button(box, text="Eliminar", command=f_elim).pack(side="left", padx=2)

    def _crear_tabla(self, parent, headers):
        tv = ttk.Treeview(parent, show="headings")
        self._set_headers(tv, headers)
        tv.pack(fill="both", expand=True)
        return tv

    def _set_headers(self, tv, headers):
        cols = tuple(f"c{i}" for i in range(len(headers)))
        tv["columns"] = cols
        for c, h in zip(cols, headers):
            tv.heading(c, text=h)
            tv.column(c, width=130, anchor="center")

    def _rellenar_tree(self, tv, filas):
        tv.delete(*tv.get_children())
        for f in filas:
            tv.insert("", "end", values=f)

    def _rellenar_combo(self, cb, valores):
        actual = cb.get()
        cb["values"] = valores
        if valores and actual not in valores:
            cb.current(0)

    def _llenar_entradas(self, tv, pares):
        sel = tv.selection()
        if not sel:
            return
        vals = tv.item(sel[0], "values")
        for entry, idx in pares:
            entry.delete(0, "end")
            entry.insert(0, vals[idx])

    def _id_sel(self, tv):
        sel = tv.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Seleccione un registro de la tabla.")
            return None
        return int(tv.item(sel[0], "values")[0])

    def _id_combo(self, texto):
        if not texto or "-" not in texto:
            raise ValueError("Seleccione una opción válida.")
        return int(texto.split("-", 1)[0].strip())


if __name__ == "__main__":
    AplicacionArriendos().mainloop()