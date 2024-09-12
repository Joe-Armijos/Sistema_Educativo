from datetime import date
from clsJson import JsonFile
from iCrud import ICrud
import time

# CLASE QUE REPRESENTA UNA ASIGNATURA
class Asignatura:
    def __init__(self, id, descripcion, nivel, active):
        self.id = id
        self.descripcion = descripcion
        self.nivel = nivel
        self.fecha_creacion = date.today()
        self.active = active
        self.profesor = None

    def getJson(self):
        return {
            "id": self.id,
            "descripcion": self.descripcion,
            "nivel": self.nivel,
            "fecha_creacion": self.fecha_creacion.isoformat(),  # Convertir fecha a cadena
            "active": self.active,
            "profesor": self.profesor
        }


# CRUD Asignatura
class CrudAsignatura(ICrud):
    def __init__(self):
        self.json_file = JsonFile('archivos/asignaturas.json')
        self.profesores_json = JsonFile('archivos/profesores.json')

    def create(self):
        # Solicitar datos al usuario
        id = input("Ingrese el ID de la asignatura: ")
        descripcion = input("Ingrese la descripción de la asignatura: ")
        nivel = input("Ingrese el ID del nivel al que pertenece la asignatura: ")
        active = input("¿Está activa la asignatura? (s/n): ").lower() == 's'

        # Crear un objeto Asignatura
        asignatura = {
            "id": id,
            "descripcion": descripcion,
            "nivel": nivel,
            "profesor": None,  # Inicialmente no asignado a ningún profesor
            "active": active
        }

        # Verificar si el ID ya existe
        existing = self.json_file.find("id", id)
        if existing:
            print(f"El ID '{id}' ya está en uso. No se puede crear la asignatura.")
            time.sleep(2)
            return

        # Agregar la nueva asignatura
        self.json_file.add(asignatura)

        print("Asignatura creada exitosamente.")
        time.sleep(2)

    def update(self):
        # Solicitar el ID de la asignatura a actualizar
        id = input("Ingrese el ID de la asignatura a actualizar: ")

        # Buscar la asignatura
        asignatura = self.json_file.find("id", id)
        if not asignatura:
            print(f"La asignatura con ID '{id}' no existe.")
            time.sleep(2)
            return

        # Solicitar nuevos datos
        nueva_descripcion = input(f"Ingrese la nueva descripción (actual: {asignatura['descripcion']}): ")
        nuevo_nivel = input(f"Ingrese el nuevo nivel (actual: {asignatura['nivel']}): ")
        nueva_actividad = input(f"¿Está activa la asignatura? (actual: {'s' if asignatura['active'] else 'n'}): ").lower()

        # Actualizar los campos
        updates = {}
        if nueva_descripcion:
            updates["descripcion"] = nueva_descripcion
        if nuevo_nivel:
            updates["nivel"] = nuevo_nivel
        if nueva_actividad:
            updates["active"] = nueva_actividad == 's'

        if updates:
            # Actualizar la asignatura en el archivo
            self.json_file.update("id", id, updates)
            print(f"Asignatura con ID '{id}' actualizada exitosamente.")
        else:
            print("No se realizaron cambios.")

        time.sleep(2)

    def delete(self):
        # Solicitar el ID de la asignatura a eliminar
        id = input("Ingrese el ID de la asignatura a eliminar: ")

        # Verificar si la asignatura existe
        asignatura = self.json_file.find("id", id)
        if not asignatura:
            print(f"La asignatura con ID '{id}' no existe.")
            time.sleep(2)
            return

        # Confirmar eliminación
        confirm = input(f"¿Está seguro que desea eliminar la asignatura '{asignatura['descripcion']}'? (s/n): ").lower()
        if confirm != 's':
            print("Operación cancelada.")
            return

        # Eliminar la asignatura
        try:
            self.json_file.delete("id", id)
            print(f"Asignatura con ID '{id}' eliminada exitosamente.")
        except ValueError as e:
            print(f"Error al eliminar la asignatura: {e}")
        time.sleep(2)

    def assign_profesor(self):
    # Obtener asignaturas
        asignaturas = self.json_file.read()
    
        if not asignaturas:
            print("No hay asignaturas registradas.")
            return

        # Mostrar asignaturas
        print("Asignaturas disponibles:")
        for asignatura in asignaturas:
            # Verificar si el campo profesor existe antes de acceder
            profesor = asignatura.get('profesor', 'No asignado')
            print(f"ID: {asignatura['id']}, Descripción: {asignatura['descripcion']}, Profesor: {profesor}")

        # Solicitar el ID de la asignatura
        id_asignatura = input("Ingrese el ID de la asignatura a la que desea asignar un profesor: ")
        asignatura = self.json_file.find("id", id_asignatura)
    
        if not asignatura:
            print("Asignatura no encontrada.")
            return

        # Solicitar el ID del profesor
        id_profesor = input("Ingrese el ID del profesor: ")

        # Asignar el profesor a la asignatura
        asignatura['profesor'] = id_profesor

    # Actualizar el archivo con la asignatura modificada
        self.json_file.update("id", id_asignatura, asignatura)
        print(f"Profesor con ID {id_profesor} asignado a la asignatura {asignatura['descripcion']}.")
        time.sleep(2)


    def consult(self):
        id = input("Ingrese el ID de la asignatura a consultar (deje en blanco para consultar todas): ")
        if id:
            asignatura = self.json_file.find("id", id)
            if asignatura:
                print(f"ID: {asignatura['id']}, Descripción: {asignatura['descripcion']}, Nivel: {asignatura['nivel']}, "
                      f"Profesor: {asignatura['profesor']}, Activa: {'Sí' if asignatura['active'] else 'No'}")
            else:
                print("Asignatura no encontrada.")
        else:
            asignaturas = self.json_file.read()
            if asignaturas:
                print("Asignaturas registradas:")
                for asignatura in asignaturas:
                    print(f"ID: {asignatura['id']}, Descripción: {asignatura['descripcion']}, Nivel: {asignatura['nivel']}, "
                          f"Profesor: {asignatura['profesor']}, Activa: {'Sí' if asignatura['active'] else 'No'}")
            else:
                print("No hay asignaturas registradas.")
        input("Presione una tecla para continuar...")
