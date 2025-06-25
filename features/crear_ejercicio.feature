Feature: Creación de un nuevo ejercicio por parte de un Docente

  Como docente, quiero agregar un nuevo ejercicio a una serie existente
  para que mis estudiantes puedan resolverlo.

  Background:
    Given que existe un docente con correo "profesor@test.com" y contraseña "password123"
    And existe una "Serie 1" en un curso activo
    And el docente está autenticado en la plataforma

  Scenario: El docente crea un nuevo ejercicio exitosamente
    Given el docente está en la página para agregar un ejercicio
    When completa el formulario para agregar el ejercicio "Ejercicio de Resta" a la "Serie 1" con un archivo de enunciado "resta.md" y un archivo de test "RestaTest.java"
    Then el sistema debe mostrar el mensaje "Ejercicio agregado con éxito"
    And el "Ejercicio de Resta" debe aparecer en la lista de ejercicios de la serie
