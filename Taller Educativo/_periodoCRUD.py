from clsJson import JsonFile
from datetime import date
from iCrud import ICrud
import time

# CLASE QUE REPRESENTA UN PERIODO ACADÉMICO.
class Periodo:
    def __init__(self, id, periodo, active): 
        self.id = id # Identificador único para el periodo.
        self.periodo = periodo # Nombre o descripción del periodo (por ejemplo, "Semestre 1").
        self.fecha_creacion = date.today() # Fecha de creación del periodo, se asigna la fecha actual.
        self.active = active # Estado de actividad del periodo (True o False).

    def getJson(self):
        return {
            "id": self.id,
            "periodo": self.periodo,
            "fecha_creacion": self.fecha_creacion.isoformat(),  # Convertir fecha a cadena
            "active": self.active
        }


# CRUD Periodo
class CrudPeriodo(ICrud):
    def __init__(self):
        self.json_file = JsonFile('archivos/periodos.json')

    def create(self):
        # Solicitar datos al usuario
        id = input("Ingrese el ID del periodo: ")
        periodo = input("Ingrese la descripción del periodo: ")
        active = input("¿Está activo el periodo? (s/n): ").lower() == 's'

        # Crear un objeto Periodo
        periodo_obj = Periodo(id, periodo, active)

        # Verificar si el ID ya existe
        existing = self.json_file.find("id", id)
        if existing:
            print(f"El ID '{id}' ya está en uso. No se puede crear el periodo.")
            time.sleep(2)
            return

        # Agregar el nuevo periodo
        self.json_file.add(periodo_obj.getJson())

        print("Periodo creado exitosamente")
        time.sleep(2)

    def update(self):
        id = input("Ingrese el ID del periodo a actualizar: ")

        # Verificar si el periodo existe
        periodo = self.json_file.find("id", id)
        if not periodo:
            print("Periodo no encontrado.")
            time.sleep(2)
            return

        # Solicitar los nuevos datos
        nueva_descripcion = input("Ingrese la nueva descripción (dejar en blanco para mantener): ")
        nueva_actividad = input("¿Está activo el periodo? (s/n, dejar en blanco para mantener): ").lower()

        # Crear un diccionario con los nuevos datos
        new_data = {}
        if nueva_descripcion:
            new_data["periodo"] = nueva_descripcion
        if nueva_actividad:
            new_data["active"] = nueva_actividad == 's'

        if not new_data:
            print("No se realizaron cambios.")
            time.sleep(2)
            return

        try:
            self.json_file.update("id", id, new_data)
            print("Periodo actualizado exitosamente")
        except ValueError as e:
            print(e)
        time.sleep(2)

    def delete(self):
        id = input("Ingrese el ID del periodo a eliminar: ")
        try:
            self.json_file.delete("id", id)
            print("Periodo eliminado exitosamente")
        except ValueError as e:
            print(e)
        time.sleep(2)   

    def consult(self):
        id = input("Ingrese el ID del periodo a consultar (deje en blanco para consultar todos): ")
        if id:
            periodo = self.json_file.find("id", id)
            if periodo:
                print(f"ID: {periodo['id']}, Descripción: {periodo['periodo']}, Fecha de Creación: {periodo['fecha_creacion']}, Activo: {'Sí' if periodo['active'] else 'No'}")
            else:
                print("Periodo no encontrado.")
        else:
            periodos = self.json_file.read()
            if periodos:
                print("Periodos registrados:")
                for periodo in periodos:
                    print(f"ID: {periodo['id']}, Descripción: {periodo['periodo']}, Fecha de Creación: {periodo['fecha_creacion']}, Activo: {'Sí' if periodo['active'] else 'No'}")
            else:
                print("No hay periodos registrados.")
        input("Presione una tecla para continuar...")