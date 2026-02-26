#from collections import defaultdict
from app.repositories.activity_repository import ActivityRepository


class ActivityService:

    @staticmethod
    def get_all_activities():
        activities = ActivityRepository.get_all()

        if not activities:
            return []

        # Convertimos diccionarios → tuplas
        return [
            (
                a["id_actividad"],
                a["nombre_actividad"]
            )
            for a in activities
        ]

    @staticmethod
    def add_activity(nombre):
        ActivityRepository.create(nombre)

    @staticmethod
    def update_activity(activity_id, nombre):
        ActivityRepository.update(activity_id, nombre)

    @staticmethod
    def delete_activity(activity_id):
        ActivityRepository.delete(activity_id)

    @staticmethod
    def get_registros_summary(start_date, end_date):
        raw_data = ActivityRepository.get_records_between(start_date, end_date)

        if not raw_data:
            return []

        from collections import defaultdict

        resumen = defaultdict(lambda: {"horas": 0, "alumnos": set()})

        for row in raw_data:
            key = (row["actividad"], row["fecha"])

            resumen[key]["horas"] += row["horas"]
            resumen[key]["alumnos"].add(row["numero_control"])

        return [
            (
                actividad,                 # 0
                fecha,                     # 1
                data["horas"],             # 2
                len(data["alumnos"])       # 3
            )
            for (actividad, fecha), data in resumen.items()
        ]

    @staticmethod
    def get_alumnos_por_registro(start_date, end_date):
        raw_data = ActivityRepository.get_records_between(start_date, end_date)

        if not raw_data:
            return []

        return [
            (
                row["alumno"],          # 0
                row["numero_control"],  # 1
                row["actividad"],       # 2
                row["fecha"]            # 3
            )
            for row in raw_data
        ]