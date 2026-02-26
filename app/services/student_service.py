from app.repositories.student_repository import StudentRepository


class StudentService:

    @staticmethod
    def list_students():
        students = StudentRepository.get_all()

        if not students:
            return []

        return [
            (
                s["numero_control"],  # 0
                s["nombre"],          # 1
                s["correo"],          # 2
                s["telefono"]         # 3
            )
            for s in students
        ]

    @staticmethod
    def add_student(numero_control, nombre, correo, telefono):
        StudentRepository.create(
            numero_control,
            nombre,
            correo,
            telefono
        )

    @staticmethod
    def update_student(numero_control, nombre, correo, telefono):
        StudentRepository.update(
            numero_control,
            nombre,
            correo,
            telefono
        )

    @staticmethod
    def delete_student(numero_control):
        StudentRepository.delete(numero_control)