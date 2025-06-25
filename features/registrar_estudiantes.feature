Feature: Registrar Estudiantes en un Curso

  Como docente, quiero registrar estudiantes en un curso cargando un archivo CSV,
  para que puedan acceder a la plataforma.

  Background:
    Given que existe un docente con correo "profesor@test.com" y contraseña "password123"
    And existe un curso "Curso de Prueba" activo
    And el docente está autenticado en la plataforma

  Scenario: El docente registra estudiantes exitosamente mediante un archivo CSV
    Given el docente está en la página para registrar estudiantes
    When selecciona el curso "Curso de Prueba" y carga el archivo "test_lista_de_clases.csv"
    Then la respuesta debe incluir el mensaje "Has creado exitosamente un nuevo Curso" o "Registrar Estudiantes"
    And los estudiantes del archivo "test_lista_de_clases.csv" deben estar registrados en el curso

  Scenario: El docente intenta registrar estudiantes con un archivo CSV vacío
    Given el docente está en la página para registrar estudiantes
    When selecciona el curso "Curso de Prueba" y carga el archivo "test_vacio.csv"
    Then el sistema me redirige al dash de docentes