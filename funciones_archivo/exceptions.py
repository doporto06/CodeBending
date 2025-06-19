class CarpetaError(Exception):
    """Excepción base para errores relacionados con carpetas."""
    pass

class CarpetaYaExisteError(CarpetaError):
    """Se lanza cuando una carpeta ya existe."""
    pass

class CarpetaCreacionError(CarpetaError):
    """Se lanza cuando ocurre un error al crear una carpeta."""
    pass