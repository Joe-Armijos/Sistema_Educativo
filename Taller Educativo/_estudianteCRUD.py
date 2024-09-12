from clsJson import JsonFile
from datetime import date
from iCrud import ICrud
import time

# CLASE QUE REPRESENTA UN ESTUDIANTE.
class Estudiante:
    def __init__(self, id, nombre, asignatura=None, active=True):
        self.id = id # Identificador único para el estudiante.
        self.nombre = nombre # Nombre del estudiante.
        self.fecha_creacion = date.today() # Fecha de creación del registro del estudiante, se asigna la fecha actual.
        self.asignatura = asignatura
        self.active = active # Estado de actividad del estudiante (True o False)


    def getJson(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "fecha_creacion": self.fecha_creacion.isoformat(),  # Convertir fecha a cadena
            "asignatura": self.asignatura,
            "active": self.active
        }


# CRUD Estudiante
class CrudEstudiante(ICrud):
    def __init__(self):
        self.json_file = JsonFile('archivos/estudiantes.json')

    def create(self):
        id = input("Ingrese el ID del estudiante: ")
        nombre = input("Ingrese el nombre del estudiante: ")
        asignatura = input("Ingrese la asignatura del estudiante (deje vacío si no aplica): ")
        active = input("¿Está activo el estudiante? (s/n): ").lower() == 's'

        estudiante = Estudiante(id, nombre, asignatura if asignatura else None, active)

        # Verifica si el ID ya está en uso
        existing = self.json_file.find("id", id)
        if existing:
            print(f"😊 El ID '{id}' ya está en uso. No se puede crear el estudiante.")
            time.sleep(2)
            return

        # Agrega el nuevo estudiante al archivo JSON
        self.json_file.add(estudiante.getJson())
        print("😊 Estudiante creado exitosamente 😊")
        time.sleep(2)

    def assign_subject(self):
        id = input("Ingrese el ID del estudiante a asignar a una asignatura: ")
        asignatura = input("Ingrese la nueva asignatura: ")

        estudiantes = self.json_file.read()
        for estudiante in estudiantes:
            if estudiante['id'] == id:
                estudiante['asignatura'] = asignatura
                self.json_file.update("id", id, estudiante)
                print(f"Estudiante {id} asignado a la asignatura {asignatura}.")
                return

        print("Estudiante no encontrado.")
        time.sleep(2)

    def update(self):
        id = input("Ingrese el ID del estudiante a actualizar: ")
        estudiante = self.json_file.find("id", id)
        if not estudiante:
            print("Estudiante no encontrado.")
            time.sleep(2)
            return

        nuevo_nombre = input("Ingrese el nuevo nombre (dejar en blanco para mantener): ")
        nueva_asignatura = input("Ingrese la nueva asignatura (dejar en blanco para mantener): ")
        nuevo_active = input("¿Está activo el estudiante? (s/n, dejar en blanco para mantener): ").lower()

        new_data = {}
        if nuevo_nombre:
            new_data["nombre"] = nuevo_nombre
        if nueva_asignatura:
            new_data["asignatura"] = nueva_asignatura
        if nuevo_active:
            new_data["active"] = nuevo_active == 's'

        if not new_data:
            print("No se realizaron cambios.")
            time.sleep(2)
            return

        try:
            self.json_file.update("id", id, new_data)
            print("😊 Estudiante actualizado exitosamente 😊")
        except ValueError as e:
            print(e)
        time.sleep(2)

    def delete(self):
        id = input("Ingrese el ID del estudiante a eliminar: ")
        try:
            self.json_file.delete("id", id)
            print("😊 Estudiante eliminado exitosamente 😊")
        except ValueError as e:
            print(e)
        time.sleep(2)

    def consult(self):
        id = input("Ingrese el ID del estudiante a consultar (deje en blanco para consultar todos): ")
        if id:
            estudiante = self.json_file.find("id", id)
            if estudiante:
                print(f"ID: {estudiante['id']}, Nombre: {estudiante['nombre']}, Asignatura: {estudiante['asignatura']}, Activo: {'Sí' if estudiante['active'] else 'No'}")
            else:
                print("Estudiante no encontrado.")
        else:
            estudiantes = self.json_file.read()
            if estudiantes:
                print("Estudiantes registrados:")
                for estudiante in estudiantes:
                    print(f"ID: {estudiante['id']}, Nombre: {estudiante['nombre']}, Asignatura: {estudiante['asignatura']}, Activo: {'Sí' if estudiante['active'] else 'No'}")
            else:
                print("No hay estudiantes registrados.")
        input("Presione una tecla para continuar...")