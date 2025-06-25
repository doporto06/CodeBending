import os
import shutil
from main import app, db
from basedatos.modelos import Supervisor, Estudiante, Curso, Grupo, Serie, Ejercicio, serie_asignada, inscripciones, estudiantes_grupos, supervisores_grupos
from werkzeug.security import generate_password_hash

def before_all(context):
    """
    Se ejecuta una vez antes de todas las pruebas.
    Configura la aplicación Flask para el entorno de pruebas.
    """
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    # Usar una base de datos SQLite en memoria para las pruebas
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False  # Deshabilitar CSRF para pruebas de formularios

    # Crea un cliente de pruebas para simular peticiones
    context.client = app.test_client()

    # Empuja un contexto de aplicación para que db.create_all() funcione
    context.app_context = app.app_context()
    context.app_context.push()
    db.create_all()

def before_scenario(context, scenario):
    """
    Se ejecuta antes de cada escenario.
    Limpia la base de datos y crea los datos necesarios para el escenario.
    """
    # Limpiar todas las tablas antes de cada escenario para asegurar aislamiento
    db.session.rollback()
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()

    # --- Crear datos base para las pruebas ---
    # Supervisor
    supervisor = Supervisor(nombres="Profesor", apellidos="Test", correo="profesor@test.com", password=generate_password_hash("password123"))
    db.session.add(supervisor)
    context.supervisor = supervisor # Guardar el supervisor en el contexto para usarlo en los steps

    # Curso
    curso = Curso(nombre="Curso de Prueba", activa=True)
    db.session.add(curso)
    context.curso = curso
    
    # Grupo
    grupo = Grupo(nombre="Sección 1", id_curso=1)
    db.session.add(grupo)

    # Serie
    serie = Serie(nombre="Serie 1", activa=True)
    db.session.add(serie)
    db.session.flush() # Para obtener los IDs generados

    # --- Crear estructura de carpetas y archivos para el ejercicio ---
    path_ejercicio = "ejerciciosPropuestos/Serie_1/Ejercicio_1"
    path_enunciado_file = "enunciadosEjercicios/Serie_1/Ejercicio_1/1_Sumar2.md"
    
    # Crear directorios necesarios
    os.makedirs(os.path.dirname(path_enunciado_file), exist_ok=True)
    
    # Copiar la plantilla del ejercicio
    if os.path.exists(path_ejercicio):
        shutil.rmtree(path_ejercicio)
    shutil.copytree("plantillaMaven", path_ejercicio)

    # Añadir el archivo de test a la ruta del ejercicio
    ruta_origen_test = "ejercicio de ejemplo/AdderTest.java"
    ruta_destino_test = os.path.join(path_ejercicio, "src/test/java/org/example/AdderTest.java")
    shutil.copy(ruta_origen_test, ruta_destino_test)

    # Crear un archivo de enunciado de prueba
    with open(path_enunciado_file, "w") as f:
        f.write("# Enunciado de Suma Simple\nEscribe un programa que sume dos números enteros. \n\n## Ejemplo de Entrada/Salida\n- Entrada: 2, 3\n- Salida: 5\n")

    # Ejercicio
    ejercicio = Ejercicio(nombre="Suma Simple", id_serie=serie.id, path_ejercicio=path_ejercicio, enunciado=path_enunciado_file)
    db.session.add(ejercicio)

    # Estudiante
    estudiante = Estudiante(nombres="Juan", apellidos="Perez", matricula="202012345", correo="alumno@test.com", password=generate_password_hash("password123"), carrera = "Ingeniería Civil Informática")
    db.session.add(estudiante)
    db.session.flush()

    # --- Realizar las asignaciones en tablas intermedias ---
    db.session.execute(inscripciones.insert().values(id_estudiante=estudiante.id, id_curso=curso.id))
    db.session.execute(estudiantes_grupos.insert().values(id_estudiante=estudiante.id, id_grupo=grupo.id))
    db.session.execute(supervisores_grupos.insert().values(id_supervisor=supervisor.id, id_grupo=grupo.id))
    db.session.execute(serie_asignada.insert().values(id_serie=serie.id, id_grupo=grupo.id))
    db.session.commit()

    # Guardar objetos en el contexto para usarlos en los steps
    context.estudiante = estudiante
    context.serie = serie
    context.ejercicio = ejercicio

def after_scenario(context, scenario):
    """
    Se ejecuta después de cada escenario.
    """
    # Limpiar carpetas creadas durante la prueba
    if os.path.exists("ejerciciosPropuestos"):
        shutil.rmtree("ejerciciosPropuestos")
    if os.path.exists("enunciadosEjercicios"):
        shutil.rmtree("enunciadosEjercicios")
    if os.path.exists("ejerciciosEstudiantes"):
        shutil.rmtree("ejerciciosEstudiantes")

def after_all(context):
    """
    Se ejecuta una vez después de todas las pruebas.
    Limpia el contexto de la aplicación.
    """
    context.app_context.pop()