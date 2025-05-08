import os
import shutil
from .exceptions import CarpetaYaExisteError, CarpetaCreacionError

def agregarCarpetaEjercicioEstudiante(rutaSerie, ejercicio_id, ejercicio_path):
    # Validar parámetros
    if not os.path.exists(rutaSerie) or not os.path.exists(ejercicio_path):
        raise ValueError("Ruta de archivador o ejercicio no válida.")

    # Crear la ruta de la carpeta del ejercicio para el estudiante
    rutaEjercicioEstudiante = os.path.join(rutaSerie, f"Ejercicio_{ejercicio_id}")

    # Verificar si la carpeta existe y eliminarla
    if os.path.exists(rutaEjercicioEstudiante):
        shutil.rmtree(rutaEjercicioEstudiante)
    # Copiar la carpeta del ejercicio al estudiante
    shutil.copytree(ejercicio_path, rutaEjercicioEstudiante)

    return rutaEjercicioEstudiante

def agregarCarpetaSerieEstudiante(rutaArchivador, serie_id):
    try:
        rutaSerieEstudiante = os.path.join(rutaArchivador, f"Serie_{serie_id}")
        if os.path.exists(rutaSerieEstudiante):
            return rutaSerieEstudiante
        else:
            os.makedirs(rutaSerieEstudiante)
            return rutaSerieEstudiante
    except Exception as e:
        raise CarpetaCreacionError(f"Hubo un error al agregar la carpeta de la serie: {str(e)}")

def crearArchivadorEstudiante(matricula):
    # Función para crear la carpeta del estudiante con la matrícula para guardar sus archivos
    rutaPrincipal = 'ejerciciosEstudiantes'
    rutaEstudiante = os.path.join(rutaPrincipal, str(matricula))

    # Verificar si la carpeta del estudiante ya existe
    if not os.path.exists(rutaEstudiante):
        os.makedirs(rutaEstudiante)

    return rutaEstudiante

def crearCarpetaEjercicio(id_ejercicio, id_serie):
    rutaBase = "ejerciciosPropuestos/"
    rutaSerie = os.path.join(rutaBase, f"Serie_{id_serie}")
    nombreCarpetaEjercicio = os.path.join(rutaSerie, f"Ejercicio_{id_ejercicio}")
    rutaEnunciados = os.path.join("enunciadosEjercicios/", f"Serie_{id_serie}")
    rutaFinalEnunciado = os.path.join(rutaEnunciados, f"Ejercicio_{id_ejercicio}")

    # Verificar si las carpetas ya existen
    if os.path.exists(rutaFinalEnunciado) or os.path.exists(nombreCarpetaEjercicio):
        raise CarpetaYaExisteError("Las carpetas ya existen")

    try:
        # Crear las carpetas necesarias
        shutil.copytree("plantillaMaven/", nombreCarpetaEjercicio)
        os.makedirs(rutaFinalEnunciado)
        return nombreCarpetaEjercicio, rutaFinalEnunciado, "Carpetas creadas con éxito"
    except Exception as e:
        raise CarpetaCreacionError(f"Error al crear las carpetas: {str(e)}")

def crearCarpetaSerie(id_serie):
    rutaBase = "ejerciciosPropuestos/"
    rutaEnunciados = "enunciadosEjercicios/"
    nombreCarpetaEnunciados = f"Serie_{id_serie}"

    rutaSerie = os.path.join(rutaBase, nombreCarpetaEnunciados)
    rutaFinalEnunciado = os.path.join(rutaEnunciados, nombreCarpetaEnunciados)

    # Verificar si las carpetas ya existen
    if os.path.exists(rutaFinalEnunciado) or os.path.exists(rutaSerie):
        raise CarpetaYaExisteError("La carpeta ya existe")

    try:
        # Crear las carpetas necesarias
        os.makedirs(rutaSerie)
        os.makedirs(rutaFinalEnunciado)
        return rutaSerie
    except Exception as e:
        raise CarpetaCreacionError(f"Error al crear la carpeta de la serie: {str(e)}")