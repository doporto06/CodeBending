from behave import given, when, then
from features.steps.validacion_usuario_steps import *

@when('el estudiante intenta reenviar una solución "{filename}" que {status} las pruebas')
def step_impl_reenvio_solucion(context, filename, status):
    filepath = 'ejercicio de ejemplo/SolucionCorrecta/Adder.java' if status == 'pasa' else 'ejercicio de ejemplo/SolucionIncorrecta/Adder.java'
    url = f'/dashEstudiante/{context.estudiante.id}/serie/{context.serie.id}/ejercicio/{context.ejercicio.id}'
    with open(filepath, 'rb') as f:
        data = {'archivo_java': (f, filename)}
        context.response = context.client.post(url, data=data, content_type='multipart/form-data', follow_redirects=True)
    assert context.response.status_code == 200

@then('el sistema debe mostrar el mensaje de reenvío "{mensaje}"')
def step_impl_verificar_mensaje_reenvio(context, mensaje):
    assert mensaje.encode() in context.response.data

@then('el estado del ejercicio tras el reenvío debe mostrarse como "{estado}"')
def step_impl_verificar_estado_reenvio(context, estado):
    if estado == 'aprobado':
        assert b'bg-success-custom' in context.response.data
    elif estado == 'reprobado':
        assert b'bg-danger-custom' in context.response.data
    else:
        raise Exception(f"Estado desconocido: {estado}")
