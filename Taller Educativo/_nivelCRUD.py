from datetime import date
from clsJson import JsonFile
from iCrud import ICrud
import time

# CLASE QUE REPRESENTA UN NIVEL EDUCATIVO (POR EJEMPLO, PRIMARIA, SECUNDARIA).
class Nivel:
    def __init__(self, id, nivel, active):
        self.id = id # Identificador único para el nivel.
        self.nivel = nivel # Nombre o descripción del nivel (por ejemplo, "Secundaria").
        self.fecha_creacion = date.today() # Fecha de creación del nivel, se asigna la fecha actual.
        self.active = active # El nivel se marca como activo de manera predeterminada.

    def getJson(self):
        return {
            "id": self.id,
            "nivel": self.nivel,
            "fecha_creacion": self.fecha_creacion.isoformat(),  # Convertir fecha a cadena
            "active": self.active
        }


# CRUD Nivel
class CrudNivel(ICrud):
    def __init__(self):
        self.json_file = JsonFile('archivos/niveles.json')

    def create(self):
        # Solicitar datos al usuario
        id = input("Ingrese el ID del nivel: ")
        nivel = input("Ingrese la descripción del nivel: ")
        active = input("¿Está activo el nivel? (s/n): ").lower() == 's'

        # Crear un objeto Nivel
        nivel_obj = Nivel(id, nivel, active)

        # Verificar si el ID ya existe
        existing = self.json_file.find("id", id)
        if existing:
            print(f"El ID '{id}' ya está en uso. No se puede crear el nivel.")
            time.sleep(2)
            return

        # Agregar el nuevo nivel
        self.json_file.add(nivel_obj.getJson())

        print("Nivel creado exitosamente")
        time.sleep(2)

    def update(self):
        id = input("Ingrese el ID del nivel a actualizar: ")

        # Verificar si el nivel existe
        nivel = self.json_file.find("id", id)
        if not nivel:
            print("Nivel no encontrado.")
            time.sleep(2)
            return

        # Solicitar los nuevos datos
        nueva_descripcion = input("Ingrese la nueva descripción (dejar en blanco para mantener): ")

        # Crear un diccionario con los nuevos datos
        new_data = {}
        if nueva_descripcion:
            new_data["nivel"] = nueva_descripcion

        if not new_data:
            print("No se realizaron cambios.")
            time.sleep(2)
            return

        try:
            self.json_file.update("id", id, new_data)
            print("Nivel actualizado exitosamente")
        except ValueError as e:
            print(e)
        time.sleep(2)

    def delete(self):
        id = input("Ingrese el ID del nivel a eliminar: ")
        try:
            self.json_file.delete("id", id)
            print("Nivel eliminado exitosamente")
        except ValueError as e:
            print(e)
        time.sleep(2)

    def consult(self):
        id = input("Ingrese el ID del nivel a consultar (deje en blanco para consultar todos): ")
        if id:
            nivel = self.json_file.find("id", id)
            if nivel:
                print(f"ID: {nivel['id']}, Descripción: {nivel['nivel']}, Fecha de Creación: {nivel['fecha_creacion']}, Activo: {'Sí' if nivel['active'] else 'No'}")
            else:
                print("Nivel no encontrado.")
        else:
            niveles = self.json_file.read()
            if niveles:
                print("Niveles registrados:")
                for nivel in niveles:
                    print(f"ID: {nivel['id']}, Descripción: {nivel['nivel']}, Fecha de Creación: {nivel['fecha_creacion']}, Activo: {'Sí' if nivel['active'] else 'No'}")
            else:
                print("No hay niveles registrados.")
        input("Presione una tecla para continuar...")