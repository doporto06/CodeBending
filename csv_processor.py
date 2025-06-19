import os
import csv
from flask import current_app
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError
from basedatos.modelos import Estudiante, inscripciones


class CSVProcessingError(Exception):
    """Excepción personalizada para errores de validación CSV"""
    pass

class CSVProcessor:
    def __init__(self, session, upload_folder):
        self.session = session
        self.upload_folder = upload_folder
        self._current_line = 0

    def process(self, filename, curso_id):
        try:
            filepath = os.path.join(self.upload_folder, filename)
            with open(filepath, 'r') as f:
                reader = csv.reader(f)
                next(reader)  # Saltar la primera fila
                self._process_body(reader, curso_id)
            return True
        except Exception as e:
            self._handle_error(f"Error inesperado: {str(e)}")
            return False

    def _process_body(self, reader, curso_id):
        self._current_line = 0
        for row in reader:
            self._current_line += 1
            try:
                self._validate_row(row)
                self._create_or_update_estudiante(row, curso_id)
            except CSVProcessingError as e:
                self._handle_error(f"Fila {self._current_line}: {str(e)}")
                continue

    def _validate_row(self, row):
        #Validar la estructura de las filas
        if len(row) != 5:
            raise CSVProcessingError("La fila no tiene el formato esperado")

    def _create_or_update_estudiante(self, row, curso_id):
        #Corroborar la existencia del estudiante y actuar de manera acorde
        matricula = row[0]
        estudiante = Estudiante.query.filter_by(matricula=matricula).first()
        if estudiante:
            # Si el estudiante ya existe, se actualiza
            self._update_estudiante(estudiante, curso_id)
            current_app.logger.info(f"Estudiante {estudiante.matricula} actualizado y registrado en el curso {curso_id}")
        else:
            # Si el estudiante no existe, se crea
            self._create_estudiante(row, curso_id)
            current_app.logger.info(f"Estudiante {matricula} creado y registrado en el curso {curso_id}")
    
    def _create_estudiante(self, row, curso_id):
        # Crear un nuevo estudiante
        try:
            with self.session.begin_nested():
                estudiante = self._create_estudiante_entity(row)
                estudiante_id = self._persist_estudiante(estudiante, curso_id)
                if estudiante_id:
                    self._create_inscripcion(estudiante_id, curso_id)
                else:
                    raise CSVProcessingError(f"Error al crear al estudiante {estudiante.matricula}")
        except IntegrityError as e:
            self.session.rollback()
            raise CSVProcessingError(f"Error al crear al estudiante {estudiante.matricula}")

    def _update_estudiante(self, estudiante, curso_id):
        # Actualizar el estudiante existente en caso de que no esté en el curso
        try:
            with self.session.begin_nested():
                if not self.session.query(inscripciones).filter_by(id_estudiante=estudiante.id, id_curso=curso_id).first():
                    self._create_inscripcion(estudiante.id, curso_id)  
                else:
                    raise CSVProcessingError(f"El estudiante {estudiante.matricula} ya está inscrito en el curso {curso_id}")
        except IntegrityError as e:
            self.session.rollback()
            raise CSVProcessingError(f"Error al registrar al estudiante {estudiante.matricula} en el curso {curso_id}")
        
    def _create_estudiante_entity(self, row):
        # Crear una instancia de Estudiante a partir de la fila
        return Estudiante(
            matricula = row[0],
            apellidos = row[1],
            nombres = row[2],
            correo = row[3],
            password = generate_password_hash(row[0]),
            carrera = row[4]
        )

    def _persist_estudiante(self, estudiante, curso_id):
        #Ingresar el estudiante a la base de datos
        try:
            self.session.add(estudiante)
            self.session.flush()  # Esto genera el id sin confirmar en la base de datos
            estudiante_id = estudiante.id  # Obtener el id del estudiante recién creado
            return estudiante_id
        except IntegrityError as e:
            self.session.rollback()
            raise CSVProcessingError(f"Error al crear al estudiante {estudiante.matricula}")
    
    def _create_inscripcion(self, estudiante_id, curso_id):
        # Crear una nueva inscripción del estudiante al curso
        self.session.execute(
            inscripciones.insert().values(
                id_estudiante = estudiante_id,
                id_curso = curso_id
            )
        )

    def _handle_error(self, message):
        current_app.logger.error(f"[CSVProcessor] {message}")