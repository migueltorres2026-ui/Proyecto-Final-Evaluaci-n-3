from pathlib import Path
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker


CARPETA_PROYECTO = Path(__file__).resolve().parent
RUTA_BD = CARPETA_PROYECTO / 'deportes.db'


def configurar_bd(ruta=RUTA_BD):
    """Configura el motor y las sesiones para la ruta SQLite recibida."""
    ruta = Path(ruta).resolve()
    ruta.parent.mkdir(parents=True, exist_ok=True)
    engine = create_engine(
        f'sqlite:///{ruta.as_posix()}',
        echo=False,
        connect_args={'timeout': 15},
    )

    @event.listens_for(engine, 'connect')
    def activar_claves_foraneas(conexion, _):
        cursor = conexion.cursor()
        cursor.execute('PRAGMA foreign_keys=ON')
        cursor.close()

    Session = sessionmaker(bind=engine, expire_on_commit=False)
    return engine, Session


engine, Session = configurar_bd()
