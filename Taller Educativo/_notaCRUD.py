from clsJson import JsonFile
from datetime import date
from iCrud import ICrud
import time


class Nota:
    def __init__(self, id, periodo, profesor, asignatura, active=True):
        self.id = id  # Identificador único para la nota.
        self.periodo = periodo  # Periodo en el que se otorga la nota.
        self.profesor = profesor  # Profesor que otorga la nota.
        self.asignatura = asignatura  # Asignatura a la que pertenece la nota.
        self.detalleNota = []  # Lista para almacenar los detalles de las notas para cada estudiante.
        self.fecha_creacion = date.today()  # Fecha de creación del registro de la nota.
        self.active = active  # Estado de actividad de la nota.

    def addNota(self, estudiante, calificacion):
        # Añadir detalle de la nota para un estudiante
        detalle = {
            "estudiante": estudiante,
            "calificacion": calificacion
        }
        self.detalleNota.append(detalle)
        print(f"Nota agregada para el estudiante {estudiante}: {calificacion}")

    def getJson(self):
        # Retornar los datos de la nota en formato JSON
        return {
            "id": self.id,
            "periodo": self.periodo,
            "profesor": self.profesor,
            "asignatura": self.asignatura,
            "detalleNota": self.detalleNota,
            "fecha_creacion": self.fecha_creacion.strftime("%d/%m/%Y"),
            "active": self.active
        }

class DetalleNota:
    def __init__(self, estudiante, nota1, nota2, recuperacion=None, observacion=None):
        self.estudiante = estudiante  # Estudiante al que se le asigna la nota.
        self.nota1 = nota1  # Primera calificación parcial.
        self.nota2 = nota2  # Segunda calificación parcial.
        self.recuperacion = recuperacion  # Nota de recuperación, opcional.
        self.observacion = observacion  # Observaciones sobre el rendimiento del estudiante, opcional.

    def getJson(self):
        # Retornar los datos del detalle de la nota en formato JSON
        return {
            "estudiante": self.estudiante,
            "nota1": self.nota1,
            "nota2": self.nota2,
            "recuperacion": self.recuperacion,
            "observacion": self.observacion
        }


class CrudNota(ICrud):
    def __init__(self):
        self.json_file = JsonFile('archivos/notas.json')

    def create(self):
        # Solicitar datos para la creación de la nota
        id = input("Ingrese el ID de la nota: ")
        periodo = input("Ingrese el periodo: ")
        profesor = input("Ingrese el nombre del profesor: ")
        asignatura = input("Ingrese la asignatura: ")
        active = input("¿Está activa la nota? (s/n): ").lower() == 's'

        # Crear un objeto Nota
        nota = Nota(id, periodo, profesor, asignatura, active)

        # Verificar si el ID ya existe
        existing = self.json_file.find("id", id)
        if existing:
            print(f"El ID '{id}' ya está en uso. No se puede crear la nota.")
            time.sleep(2)
            return

        # Listar estudiantes de la asignatura y asignar notas
        estudiantes = self.obtener_estudiantes(asignatura)
        if not estudiantes:
            print(f"No se encontraron estudiantes para la asignatura '{asignatura}'.")
            return

        for estudiante in estudiantes:
            calificacion = input(f"Ingrese la calificación para {estudiante['nombre']}: ")
            nota.addNota(estudiante['nombre'], calificacion)

        # Agregar la nueva nota al archivo JSON
        self.json_file.add(nota.getJson())

        print("Nota creada exitosamente.")
        time.sleep(2)

    def obtener_estudiantes(self, asignatura):
        # Método simulado para obtener estudiantes registrados en la asignatura
        estudiantes_json = JsonFile('archivos/estudiantes.json')
        estudiantes = estudiantes_json.read()
        return [est for est in estudiantes if est['asignatura'] == asignatura]

    def consult(self):
        id = input("Ingrese el ID de la nota a consultar (deje en blanco para consultar todas): ")
        if id:
            nota = self.json_file.find("id", id)
            if nota:
                print(f"ID: {nota['id']}, Periodo: {nota['periodo']}, Profesor: {nota['profesor']}, Asignatura: {nota['asignatura']}")
                print("Detalles de la nota:")
                for detalle in nota["detalleNota"]:
                    print(f"Estudiante: {detalle['estudiante']}, Calificación: {detalle['calificacion']}")
            else:
                print("Nota no encontrada.")
        else:
            notas = self.json_file.read()
            if notas:
                for nota in notas:
                    print(f"ID: {nota['id']}, Periodo: {nota['periodo']}, Profesor: {nota['profesor']}, Asignatura: {nota['asignatura']}")
                    print("Detalles de la nota:")
                    for detalle in nota["detalleNota"]:
                        print(f"Estudiante: {detalle['estudiante']}, Calificación: {detalle['calificacion']}")
            else:
                print("No hay notas registradas.")
        input("Presione una tecla para continuar...")

    def delete(self):
        id = input("Ingrese el ID de la nota a eliminar: ")
        try:
            self.json_file.delete("id", id)
            print("Nota eliminada exitosamente.")
        except ValueError as e:
            print(e)
        time.sleep(2)

    def update(self):
        id = input("Ingrese el ID de la nota a actualizar: ")

        # Buscar si la nota existe
        nota = self.json_file.find("id", id)
        if not nota:
            print(f"La nota con ID '{id}' no fue encontrada.")
            return

        # Mostrar la nota actual antes de actualizar
        print(f"Nota actual: ID: {nota['id']}, Periodo: {nota['periodo']}, Profesor: {nota['profesor']}, Asignatura: {nota['asignatura']}")
        print("Detalles de la nota:")
        for detalle in nota["detalleNota"]:
            print(f"Estudiante: {detalle['estudiante']}, Calificación: {detalle['calificacion']}")

        # Solicitar nuevos valores para los campos de la nota
        nuevo_periodo = input(f"Ingrese el nuevo periodo (actual: {nota['periodo']}): ") or nota['periodo']
        nuevo_profesor = input(f"Ingrese el nuevo nombre del profesor (actual: {nota['profesor']}): ") or nota['profesor']
        nueva_asignatura = input(f"Ingrese la nueva asignatura (actual: {nota['asignatura']}): ") or nota['asignatura']
        active = input(f"¿Está activa la nota? (s/n) (actual: {'s' if nota['active'] else 'n'}): ").lower() == 's'

        # Actualizar los estudiantes y sus calificaciones
        actualizar_estudiantes = input("¿Desea actualizar las calificaciones de los estudiantes? (s/n): ").lower() == 's'
        if actualizar_estudiantes:
            estudiantes = self.obtener_estudiantes(nueva_asignatura)
            if not estudiantes:
                print(f"No se encontraron estudiantes para la asignatura '{nueva_asignatura}'.")
                return

            detalles_nuevos = []
            for estudiante in estudiantes:
                calificacion = input(f"Ingrese la nueva calificación para {estudiante['nombre']} (actual: {self.obtener_calificacion_estudiante(nota, estudiante['nombre'])}): ")
                detalles_nuevos.append({"estudiante": estudiante['nombre'], "calificacion": calificacion})

            # Reemplazar las calificaciones antiguas por las nuevas
            nota["detalleNota"] = detalles_nuevos

        # Actualizar los datos de la nota
        nota["periodo"] = nuevo_periodo
        nota["profesor"] = nuevo_profesor
        nota["asignatura"] = nueva_asignatura
        nota["active"] = active

        # Guardar los cambios en el archivo JSON
        self.json_file.update("id", id, nota)

        print("Nota actualizada exitosamente.")
        time.sleep(2)

    def obtener_calificacion_estudiante(self, nota, nombre_estudiante):
        """Método auxiliar para obtener la calificación de un estudiante en una nota."""
        for detalle in nota["detalleNota"]:
            if detalle["estudiante"] == nombre_estudiante:
                return detalle["calificacion"]
        return "N/A"  # Si no se encuentra calificación