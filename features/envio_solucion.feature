Feature: Envío de Solución a un ejercicio por parte de un Estudiante

  Como estudiante, quiero subir un archivo de solución para un ejercicio
  y recibir retroalimentación inmediata para saber si mi código es correcto.

  Background:
    Given que existe un estudiante con correo "alumno@test.com" y contraseña "password123"
    And existe un ejercicio "Suma Simple" en la "Serie 1" de un curso activo
    And el estudiante está autenticado en la plataforma

  Scenario: El estudiante envía una solución correcta que pasa las pruebas
    Given el estudiante está en la página del ejercicio "Suma Simple"
    When sube un archivo de solución "Adder.java" que pasa las pruebas
    Then el sistema debe mostrar el mensaje "Todos los test aprobados"
    And el estado del ejercicio debe mostrarse como "aprobado"

  Scenario: El estudiante envía una solución incorrecta que falla las pruebas
    Given el estudiante está en la página del ejercicio "Suma Simple"
    When sube un archivo de solución "Adder.java" que falla las pruebas
    Then el sistema debe mostrar el mensaje "Errores en la ejecución de pruebas unitarias"
    And el estado del ejercicio debe mostrarse como "reprobado"

Feature: Reenvío de Solución tras Fallo Inicial

  Como estudiante, quiero poder volver a enviar una solución corregida
  después de fallar inicialmente, para poder aprobar el ejercicio.

  Background:
    Given que existe un estudiante con correo "alumno@test.com" y contraseña "password123"
    And existe un ejercicio "Suma Simple" en la "Serie 1" de un curso activo
    And el estudiante está autenticado en la plataforma
    And el estudiante está en la página del ejercicio "Suma Simple"

  Scenario: El estudiante falla y luego aprueba el ejercicio tras reenviar la solución
    When sube un archivo de solución "Adder.java" que falla las pruebas
    Then el sistema debe mostrar el mensaje "Errores en la ejecución de pruebas unitarias"
    And el estado del ejercicio debe mostrarse como "reprobado"
    When sube un archivo de solución "Adder.java" que pasa las pruebas
    Then el sistema debe mostrar el mensaje "Todos los test aprobados"
    And el estado del ejercicio debe mostrarse como "aprobado"
