from behave import given, when, then
import os

@given('existe un curso "{nombre_curso}" activo')
def step_impl_existe_curso(context, nombre_curso):
    assert context.curso.nombre == nombre_curso

@given('el docente está en la página para registrar estudiantes')
def step_impl_en_pagina_registrar_estudiantes(context):
    url = f'/dashDocente/{context.supervisor.id}/registrarEstudiante'
    response = context.client.get(url, follow_redirects=True)
    assert response.status_code == 200
    assert b'Registro de Estudiantes' in response.data or b'Registrar Estudiantes' in response.data

@when('selecciona el curso "{nombre_curso}" y carga el archivo "{csv_filename}"')
def step_impl_carga_csv(context, nombre_curso, csv_filename):
    # Busca el curso por nombre
    from basedatos.modelos import Curso
    curso = Curso.query.filter_by(nombre=nombre_curso).first()
    assert curso is not None

    url = f'/dashDocente/{context.supervisor.id}/registrarEstudiante'
    ruta_csv = os.path.join('uploads', csv_filename)
    data = {
        'accion': 'registrarEstudiantes',
        'curso': curso.id,
        'listaClases': (open(ruta_csv, 'rb'), csv_filename)
    }
    context.response = context.client.post(url, data=data, content_type='multipart/form-data', follow_redirects=True)
    assert context.response.status_code == 200

@then('la respuesta debe incluir el mensaje "{mensaje1}" o "{mensaje2}"')
def step_impl_verifica_mensaje_alternativo(context, mensaje1, mensaje2):
    """
    Verifica que al menos uno de los dos mensajes esté presente en la respuesta.
    """
    data = context.response.data
    assert mensaje1.encode() in data or mensaje2.encode() in data, \
        f"Error: No se encontró ni '{mensaje1}' ni '{mensaje2}' en la respuesta."
    
@then('el sistema me redirige al dash de docentes')
def step_impl_redireccion_dash_docente(context):
    """
    Verifica que la respuesta redirija al dashboard del docente.
    """
    assert '/dashDocente' in context.response.request.path, \
        f"Se esperaba ser redirigido a '/dashDocente', pero se fue a '{context.response.request.path}'"

@then('los estudiantes del archivo "{csv_filename}" deben estar registrados en el curso')
def step_impl_estudiantes_registrados(context, csv_filename):
    from basedatos.modelos import Curso, Estudiante
    curso = Curso.query.filter_by(nombre="Curso de Prueba").first()
    assert curso is not None
    ruta_csv = os.path.join('uploads', csv_filename)
    with open(ruta_csv, 'r') as f:
        next(f)  # Saltar cabecera si existe
        for linea in f:
            matricula = linea.split(',')[0]
            estudiante = Estudiante.query.filter_by(matricula=matricula).first()
            assert estudiante is not None
            assert curso in estudiante.cursos