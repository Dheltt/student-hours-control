from app.core.database import get_connection

class ActivityRepository:

    @staticmethod
    def get_all():
        with get_connection() as conn:
            if not conn:
                return []  # Retornamos lista vacía si no hay conexión
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT id_actividad,
                       nombre_actividad
                FROM actividades
                ORDER BY nombre_actividad
            """)
            data = cursor.fetchall()
            cursor.close()
            return data

    @staticmethod
    def create(nombre_actividad: str):
        with get_connection() as conn:
            if not conn:
                print(f"[WARNING] No se pudo crear la actividad '{nombre_actividad}', base de datos inactiva.")
                return
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO actividades (nombre_actividad)
                VALUES (%s)
            """, (nombre_actividad,))
            conn.commit()
            cursor.close()

    @staticmethod
    def update(id_actividad: int, nombre_actividad: str):
        with get_connection() as conn:
            if not conn:
                print(f"[WARNING] No se pudo actualizar la actividad ID {id_actividad}, base de datos inactiva.")
                return
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE actividades
                SET nombre_actividad = %s
                WHERE id_actividad = %s
            """, (nombre_actividad, id_actividad))
            conn.commit()
            cursor.close()

    @staticmethod
    def delete(id_actividad: int):
        with get_connection() as conn:
            if not conn:
                print(f"[WARNING] No se pudo eliminar la actividad ID {id_actividad}, base de datos inactiva.")
                return
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM actividades
                WHERE id_actividad = %s
            """, (id_actividad,))
            conn.commit()
            cursor.close()

    @staticmethod
    def get_records_between(start_date, end_date):
        with get_connection() as conn:
            if not conn:
                return []  # Lista vacía si no hay conexión
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT ra.fecha,
                       e.nombre AS alumno,
                       ra.numero_control,
                       a.nombre_actividad AS actividad,
                       ra.horas
                FROM registro_actividades ra
                JOIN estudiantes e ON ra.numero_control = e.numero_control
                JOIN actividades a ON ra.id_actividad = a.id_actividad
                WHERE ra.fecha BETWEEN %s AND %s
                ORDER BY ra.fecha
            """, (start_date, end_date))
            data = cursor.fetchall()
            cursor.close()
            return data