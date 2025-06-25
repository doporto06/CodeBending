# CodeBending
Para la realización de las pruebas de aceptación, se utilizó el framework Behave para Python.

Las pruebas cubren las siguientes historias de usuario:
- **Estudiante:** Envío de una solución a un ejercicio.
- **Estudiante:** Re-envío de una solución a un ejercicio.
- **Docente:** Creación de un nuevo ejercicio en una serie.
- **Docente:** Registro de estudiantes en un curso

## Instrucciones para instalar y ejecutar pruebas
### Prerrequisitos
Además de los prerrequisitos del proyecto Codebending, se utilizaron los siguientes para realizar las pruebas de aceptación:
- Python 3.12
- behave

Para instalar `behave`, ejecutar el siguiente comando en la terminal:
```bash
pip install behave
```

Luego, para ejecutar las pruebas, basta con clonar el repositorio y ejecutar el siguiente comando dentro de la carpeta raiz:
```bash
behave
```

***

You need Java JRE > 21 installed and Apache Maven in your computer.

In your favorite virtual env :
`pip install -r requirements.txt`

Then to create the database :
`python .\crear_db.py`

Then to start the project :
`python .\main.py` 

Then you need to connect to http://127.0.0.1:3000/registerSupervisor to create the first supervsor account.

You can encounter an example of exercise for the platform here : https://github.com/GeoffreyHecht/FizzBuzzPasoAPaso

Important: There seems to be a problem with path management under Windows, so I recommend using Linux (or correcting the problem).
