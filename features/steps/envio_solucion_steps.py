from behave import given, when, then

@given('que existe un estudiante con correo "{correo}" y contraseña "{password}"')
def step_impl_existe_estudiante(context, correo, password):
    # La creación del estudiante ya se hizo en environment.py
    # Guardamos las credenciales para el login
    context.correo_estudiante = correo
    context.password_estudiante = password

@given('existe un ejercicio "{nombre_ejercicio}" en la "{nombre_serie}" de un curso activo')
def step_impl_existe_ejercicio(context, nombre_ejercicio, nombre_serie):
    # Esto también se maneja en environment.py
    # Verificamos que los nombres coincidan con lo que se espera en el contexto.
    assert context.ejercicio.nombre == nombre_ejercicio
    assert context.serie.nombre == nombre_serie

@given('el estudiante está autenticado en la plataforma')
def step_impl_estudiante_autenticado(context):
    # Simulamos el inicio de sesión usando la ruta directa
    context.client.post('/login', data={
        'correo': context.correo_estudiante,
        'password': context.password_estudiante
    }, follow_redirects=True)

@given('el estudiante está en la página del ejercicio "{nombre_ejercicio}"')
def step_impl_en_pagina_ejercicio(context, nombre_ejercicio):
    # Construimos la URL manualmente para el cliente de pruebas
    url = f'/dashEstudiante/{context.estudiante.id}/serie/{context.serie.id}/ejercicio/{context.ejercicio.id}'
    response = context.client.get(url)
    assert response.status_code == 200
    assert nombre_ejercicio.encode() in response.data # Confirmar que estamos en la pág correcta

@when('sube un archivo de solución "{filename}" que {status} las pruebas')
def step_impl_sube_solucion(context, filename, status):
    # Se determina qué archivo subir basado en el estado esperado
    if status == 'pasa':
        filepath = 'ejercicio de ejemplo/SolucionCorrecta/Adder.java'
    else:
        filepath = 'ejercicio de ejemplo/SolucionIncorrecta/Adder.java'

    # Usamos la misma URL construida manualmente para la petición POST
    url = f'/dashEstudiante/{context.estudiante.id}/serie/{context.serie.id}/ejercicio/{context.ejercicio.id}'
    
    # Abrimos el archivo real y lo preparamos para la subida
    with open(filepath, 'rb') as f:
        data = {
            'archivo_java': (f, filename)
        }

        # Enviamos la petición POST con el archivo
        context.response = context.client.post(url, data=data, content_type='multipart/form-data', follow_redirects=True)
    
    assert context.response.status_code == 200

@then('el sistema debe mostrar el mensaje "{mensaje}"')
def step_impl_verificar_mensaje_feedback(context, mensaje):
    # Verificamos que el mensaje de feedback esté en la página de respuesta
    assert mensaje.encode() in context.response.data

@then('el estado del ejercicio debe mostrarse como "{estado}"')
def step_impl_verificar_estado_visual(context, estado):
    # Verificamos el feedback visual (basado en las clases CSS que usa la plataforma)
    if estado == 'aprobado':
        # Buscamos la clase CSS para el éxito
        assert b'bg-success-custom' in context.response.data, "No se encontró el indicador de 'aprobado'"
    elif estado == 'reprobado':
        # Buscamos la clase CSS para el error
        assert b'bg-danger-custom' in context.response.data, "No se encontró el indicador de 'reprobado'"
    else:
        raise Exception(f"Estado desconocido: {estado}")