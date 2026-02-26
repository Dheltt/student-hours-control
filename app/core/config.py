import os

class Settings:
    """
    Configuración de la base de datos que funciona tanto
    dentro de Docker como en la máquina local.
    """

    # Detectar si estamos dentro de Docker (opcional)
    DOCKERIZED = os.getenv("DOCKERIZED", "false").lower() == "true"

    if DOCKERIZED:
        DB_HOST = os.getenv("DB_HOST", "mysql")  # nombre del contenedor
        DB_USER = os.getenv("DB_USER", "appuser")
        DB_PASSWORD = os.getenv("DB_PASSWORD", "apppassword")
        DB_PORT = int(os.getenv("DB_PORT", 3306))
        DB_NAME = os.getenv("DB_NAME", "student_hours")
    else:
        # Valores para ejecutar localmente en Windows
        DB_HOST = os.getenv("DB_HOST", "localhost")
        DB_USER = os.getenv("DB_USER", "root")
        DB_PASSWORD = os.getenv("DB_PASSWORD", "rootpassword")
        DB_PORT = int(os.getenv("DB_PORT", 3306))
        DB_NAME = os.getenv("DB_NAME", "student_hours")

settings = Settings()