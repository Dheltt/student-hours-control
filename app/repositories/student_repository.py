from app.core.database import get_connection

class StudentRepository:

    @staticmethod
    def get_all():
        with get_connection() as conn:
            if not conn:
                # Retornamos lista vacía si no hay conexión
                return []
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT numero_control,
                       nombre,
                       correo,
                       telefono
                FROM estudiantes
                ORDER BY nombre
            """)
            students = cursor.fetchall()
            cursor.close()
            return students

    @staticmethod
    def get_by_id(numero_control: str):
        with get_connection() as conn:
            if not conn:
                return None
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT numero_control,
                       nombre,
                       correo,
                       telefono
                FROM estudiantes
                WHERE numero_control = %s
            """, (numero_control,))
            student = cursor.fetchone()
            cursor.close()
            return student

    @staticmethod
    def create(numero_control: str, nombre: str, correo: str = None, telefono: str = None):
        with get_connection() as conn:
            if not conn:
                print(f"[WARNING] No se pudo crear el estudiante {numero_control}, base de datos inactiva.")
                return
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO estudiantes
                (numero_control, nombre, correo, telefono)
                VALUES (%s, %s, %s, %s)
            """, (numero_control, nombre, correo, telefono))
            conn.commit()
            cursor.close()

    @staticmethod
    def update(numero_control: str, nombre: str, correo: str = None, telefono: str = None):
        with get_connection() as conn:
            if not conn:
                print(f"[WARNING] No se pudo actualizar el estudiante {numero_control}, base de datos inactiva.")
                return
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE estudiantes
                SET nombre = %s,
                    correo = %s,
                    telefono = %s
                WHERE numero_control = %s
            """, (nombre, correo, telefono, numero_control))
            conn.commit()
            cursor.close()

    @staticmethod
    def delete(numero_control: str):
        with get_connection() as conn:
            if not conn:
                print(f"[WARNING] No se pudo eliminar el estudiante {numero_control}, base de datos inactiva.")
                return
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM estudiantes
                WHERE numero_control = %s
            """, (numero_control,))
            conn.commit()
            cursor.close()