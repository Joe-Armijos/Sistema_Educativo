from datetime import date
from clsJson import JsonFile
from iCrud import ICrud
import time

# CLASE QUE REPRESENTA UN PROFESOR.
class Profesor:
    def __init__(self, id, nombre, active):
        self.id = id # Identificador único para el profesor
        self.nombre = nombre # Nombre del profesor.
        self.fecha_creacion = date.today() # Fecha de creación del registro del profesor, se asigna la fecha actual.
        self.active = active # Estado de actividad del profesor (True o False)

    def getJson(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "fecha_creacion": self.fecha_creacion.isoformat(),  # Convertir fecha a cadena
            "active": self.active
        }


# CRUD Profesor
class CrudProfesor(ICrud):
    def __init__(self):
        self.json_file = JsonFile('archivos/profesores.json')

    def create(self):
        """Crear un nuevo profesor."""
        # Solicitar datos al usuario
        id = input("Ingrese el ID del profesor: ")
        nombre = input("Ingrese el nombre del profesor: ")
        active = input("¿Está activo el profesor? (s/n): ").lower() == 's'

        # Crear un objeto Profesor
        profesor = Profesor(id, nombre, active)

        # Verificar si el ID ya existe para evitar duplicados
        existing = self.json_file.find("id", id)
        if existing:
            print(f"El ID '{id}' ya está en uso. No se puede crear el profesor.")
            time.sleep(2)
            return

        # Agregar el nuevo profesor al archivo JSON
        self.json_file.add(profesor.getJson())

        # Confirmación
        print("Profesor creado exitosamente")
        time.sleep(2)

    def update(self):
        """Actualizar un profesor existente."""
        id = input("Ingrese el ID del profesor a actualizar: ")
        
        # Verificar si el profesor existe
        profesor = self.json_file.find("id", id)
        if not profesor:
            print("Profesor no encontrado.")
            time.sleep(2)
            return

        # Solicitar los nuevos datos
        nuevo_nombre = input("Ingrese el nuevo nombre (dejar en blanco para mantener): ")
        nueva_actividad = input("¿Está activo el profesor? (s/n, dejar en blanco para mantener): ").lower()

        # Crear un diccionario con los nuevos datos
        new_data = {}
        if nuevo_nombre:
            new_data["nombre"] = nuevo_nombre
        if nueva_actividad:
            new_data["active"] = nueva_actividad == 's'

        if not new_data:
            print("No se realizaron cambios.")
            time.sleep(2)
            return

        try:
            self.json_file.update("id", id, new_data)
            print("Profesor actualizado exitosamente")
        except ValueError as e:
            print(e)
        time.sleep(2)

    def delete(self):
        """Eliminar un profesor existente."""
        id = input("Ingrese el ID del profesor a eliminar: ")
        try:
            self.json_file.delete("id", id)
            print("Profesor eliminado exitosamente")
        except ValueError as e:
            print(e)
        time.sleep(2)

    def consult(self):
        """Consultar uno o todos los profesores."""
        id = input("Ingrese el ID del profesor a consultar (deje en blanco para consultar todos): ")
        if id:
            profesor = self.json_file.find("id", id)
            if profesor:
                print(f"ID: {profesor['id']}, Nombre: {profesor['nombre']}, Activo: {'Sí' if profesor['active'] else 'No'}")
            else:
                print("Profesor no encontrado.")
        else:
            profesores = self.json_file.read()
            if profesores:
                print("Profesores registrados:")
                for profesor in profesores:
                    print(f"ID: {profesor['id']}, Nombre: {profesor['nombre']}, Activo: {'Sí' if profesor['active'] else 'No'}")
            else:
                print("No hay profesores registrados.")
        input("Presione una tecla para continuar...")