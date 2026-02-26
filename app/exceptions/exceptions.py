class StudentAlreadyExistsException(Exception):
    pass


class StudentNotFoundException(Exception):
    pass


class InvalidStudentDataException(Exception):
    pass


class InvalidActivityDataException(Exception):
    pass

class DatabaseConnectionError(Exception):
    """Se lanza cuando no se puede conectar a la base de datos."""
    pass