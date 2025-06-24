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
