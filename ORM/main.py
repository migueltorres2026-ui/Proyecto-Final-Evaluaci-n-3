from ORM.conexion import engine
from ORM.tabla import crear_tablas
from Interfaz.ventana_principal import AplicacionArriendos
from Interfaz import graficas
    
def main():
    try:
        crear_tablas()

        ventana = AplicacionArriendos(graficos=graficas)
        ventana.mainloop()
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
