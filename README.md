# CodeBending

CodeBending es una plataforma educativa para ejercicios de programación en Java. Los estudiantes envían soluciones a ejercicios y el sistema proporciona retroalimentación automatizada usando Maven.

## Funcionalidades

Las pruebas de aceptación cubren las siguientes historias de usuario:
- **Estudiante:** Envío de una solución a un ejercicio.
- **Estudiante:** Re-envío de una solución a un ejercicio.
- **Docente:** Creación de un nuevo ejercicio en una serie.
- **Docente:** Registro de estudiantes en un curso

## Opciones de Instalación

### Opción 1: Usando Docker (Recomendado)

#### Prerrequisitos
- Docker instalado en tu sistema

#### Instrucciones
1. Clona el repositorio:
```bash
git clone <repository-url>
cd CodeBending
```

2. Construye la imagen Docker:
```bash
docker build -t codebending .
```

3. Ejecuta el contenedor:
```bash
docker run -p 3000:3000 codebending
```

4. Accede a la aplicación en http://localhost:3000

5. Para crear la primera cuenta de supervisor, visita: http://localhost:3000/registerSupervisor

#### Ejecutar con volúmenes persistentes
Para mantener los datos entre reinicios del contenedor:
```bash
docker run -p 3000:3000 -v codebending_data:/app/instance codebending
```

### Opción 2: Instalación Local

#### Prerrequisitos
- Python 3.10+
- Java JRE 17+
- Apache Maven

#### Instrucciones
1. Crea un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Linux/Mac
# o
venv\Scripts\activate     # En Windows
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Crea la base de datos:
```bash
python crear_db.py
```

4. Inicia el proyecto:
```bash
python main.py
```

5. Accede a http://127.0.0.1:3000/registerSupervisor para crear la primera cuenta de supervisor.

## Ejecutar Pruebas

### Pruebas de aceptación con Behave
```bash
# Instalar behave si no está instalado
pip install behave

# Ejecutar pruebas
behave
```

## Recursos Adicionales

Ejemplo de ejercicio para la plataforma: https://github.com/GeoffreyHecht/FizzBuzzPasoAPaso

**Nota:** Existe un problema conocido con la gestión de rutas en Windows, se recomienda usar Linux o Docker.
