from behave import given, when, then
import os
from io import BytesIO

@given('que existe un docente con correo "{correo}" y contraseña "{password}"')
def step_impl_existe_docente(context, correo, password):
    # La creación del docente ya se hizo en environment.py
    # Guardamos las credenciales para el login
    context.correo_docente = correo
    context.password_docente = password

@given('existe una "{nombre_serie}" en un curso activo')
def step_impl_existe_serie(context, nombre_serie):
    # Verificamos que el nombre coincida con lo que se creó en environment.py
    assert context.serie.nombre in nombre_serie

@given('el docente está autenticado en la plataforma')
def step_impl_docente_autenticado(context):
    # Simulamos el inicio de sesión del docente
    context.client.post('/login', data={
        'correo': context.correo_docente,
        'password': context.password_docente
    }, follow_redirects=True)

@given('el docente está en la página para agregar un ejercicio a la "{nombre_serie}"')
def step_impl_en_pagina_agregar_ejercicio(context, nombre_serie):
    # Navegamos a la página para agregar un ejercicio a la serie existente
    url = f'/dashDocente/{context.supervisor.id}/agregarEjercicio/{context.serie.id}'
    response = context.client.get(url, follow_redirects=True)
    assert response.status_code == 200
    assert b'Agregar Ejercicio' in response.data

@when('completa el formulario con el nombre "{nombre_ejercicio}", un archivo de enunciado "{enunciado_filename}" y un archivo de test "{test_filename}"')
def step_impl_completa_formulario(context, nombre_ejercicio, enunciado_filename, test_filename):
    # Preparamos los datos y archivos para la subida
    # Usaremos archivos de ejemplo existentes y les daremos el nombre esperado
    ruta_test_origen = 'ejercicio de ejemplo/AdderTest.java'
    ruta_enunciado_origen = 'ejercicio de ejemplo/sumar2.md'
    
    url = f'/dashDocente/{context.supervisor.id}/agregarEjercicio/{context.serie.id}'
    
    data = {
        'nombre_ejercicio': nombre_ejercicio,
        'archivo_test': (open(ruta_test_origen, 'rb'), test_filename),
        'enunciado': (open(ruta_enunciado_origen, 'rb'), enunciado_filename),
    }

    # Enviamos la petición POST con los datos del formulario
    context.response = context.client.post(url, data=data, content_type='multipart/form-data', follow_redirects=True)
    assert context.response.status_code == 200

@then('el sistema debe mostrar el mensaje "{mensaje}"')
def step_impl_verificar_mensaje_exito(context, mensaje):
    assert mensaje.encode() in context.response.data

@then('el "{nombre_ejercicio}" debe aparecer en la lista de ejercicios de la serie')
def step_impl_verificar_ejercicio_en_lista(context, nombre_ejercicio):
    # La página de respuesta (después de la redirección) debe ser la del detalle de la serie
    # y debe contener el nombre del ejercicio recién creado.
    assert nombre_ejercicio.encode() in context.response.data