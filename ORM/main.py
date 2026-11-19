from ORM.conexion import engine
from ORM.tabla import crear_tablas
from interfaz.ventana import iniciar_interfaz
    
def main():
    try:
        crear_tablas()
        iniciar_interfaz()
    finally:
        engine.dispose()


if __name__ == '__main__':
    main()
