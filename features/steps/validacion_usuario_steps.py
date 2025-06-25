from behave import given

@given('que existe un estudiante con correo "{correo}" y contraseña "{password}"')
def step_impl_existe_estudiante(context, correo, password):
    context.correo_estudiante = correo
    context.password_estudiante = password

@given('existe un ejercicio "{nombre_ejercicio}" en la "{nombre_serie}" de un curso activo')
def step_impl_existe_ejercicio(context, nombre_ejercicio, nombre_serie):
    assert context.ejercicio.nombre == nombre_ejercicio
    assert context.serie.nombre == nombre_serie
