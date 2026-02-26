from mysql.connector import connect, Error
from contextlib import contextmanager
from app.core.config import settings
from app.exceptions.exceptions import DatabaseConnectionError

@contextmanager
def get_connection():
    connection = None
    try:
        connection = connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_NAME
        )
        yield connection
    except Error as e:
        # Solo imprime/loguea el error, no crashea
        print(f"[WARNING] No se pudo conectar a la base de datos: {e}")
        yield None  # Devuelve None para que los repositorios manejen que no hay conexión
    finally:
        if connection:
            try:
                connection.close()
            except:
                pass