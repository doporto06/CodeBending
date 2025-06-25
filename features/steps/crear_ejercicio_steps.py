from behave import given, when, then
import os
from io import BytesIO

@given('que existe un docente con correo "{correo}" y contraseña "{password}"')
def step_impl_existe_docente(context, correo, password):
    context.correo_docente = correo
    context.password_docente = password

@given('existe una "{nombre_serie}" en un curso activo')
def step_impl_existe_serie(context, nombre_serie):
    # Se usa '==' para una comparación exacta
    assert context.serie.nombre == nombre_serie

@given('el docente está autenticado en la plataforma')
def step_impl_docente_autenticado(context):
    context.client.post('/login', data={
        'correo': context.correo_docente,
        'password': context.password_docente
    }, follow_redirects=True)

@given('el docente está en la página para agregar un ejercicio')
def step_impl_en_pagina_agregar_ejercicio(context):
    url = f'/dashDocente/{context.supervisor.id}/agregarEjercicio'
    response = context.client.get(url, follow_redirects=True)
    assert response.status_code == 200, f"Error al acceder a la página. Status code: {response.status_code}"
    # Se comprueba que el título de la página sea el correcto según el HTML
    assert b'<h3>Agregar nuevo ejercicio</h3>' in response.data

@when('completa el formulario para agregar el ejercicio "{nombre_ejercicio}" a la "{nombre_serie}" con un archivo de enunciado "{enunciado_filename}" y un archivo de test "{test_filename}"')
def step_impl_completa_formulario(context, nombre_ejercicio, nombre_serie, enunciado_filename, test_filename):
    url = f'/dashDocente/{context.supervisor.id}/agregarEjercicio'
    
    ruta_test_origen = 'ejercicio de ejemplo/AdderTest.java'
    ruta_enunciado_origen = 'ejercicio de ejemplo/sumar2.md'
    
    data = {
        'nombreEjercicio': nombre_ejercicio,
        'id_serie': context.serie.id,
        'enunciadoFile': (open(ruta_enunciado_origen, 'rb'), enunciado_filename),
        # --- [CORRECCIÓN FINAL] ---
        # Para los campos de múltiples archivos, enviamos una lista de tuplas.
        'archivosJava': [(open(ruta_test_origen, 'rb'), test_filename)],
        # Para el campo opcional de imágenes, enviamos una lista con un archivo vacío
        # para evitar el error 'NoneType' en la aplicación.
        'imagenesFiles': [(BytesIO(b''), '')]
    }

    context.response = context.client.post(url, data=data, content_type='multipart/form-data', follow_redirects=True)
    assert context.response.status_code == 200, f"Error al enviar el formulario. Status code: {context.response.status_code}"

@then('el "{nombre_ejercicio}" debe aparecer en la lista de ejercicios de la serie')
def step_impl_verificar_ejercicio_en_lista(context, nombre_ejercicio):
    # Después de agregar un ejercicio, se verifica que aparezca en la página de detalles de la serie.
    url_detalle_serie = f'/dashDocente/{context.supervisor.id}/serie/{context.serie.id}'
    response = context.client.get(url_detalle_serie)
    assert nombre_ejercicio.encode() in response.data
