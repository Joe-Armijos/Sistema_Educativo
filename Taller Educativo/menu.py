from _notaCRUD import CrudNota
from _nivelCRUD import CrudNivel
from _periodoCRUD import CrudPeriodo
from _estudianteCRUD import CrudEstudiante
from _asignaturaCRUD import CrudAsignatura
from _profesorCRUD import CrudProfesor
from utilities import borrarPantalla, gotoxy
from components import Menu
import time
import shutil

# Color definitions
reset_color = "\033[0m"
red_color = "\033[91m"
green_color = "\033[92m"
yellow_color = "\033[93m"
blue_color = "\033[94m"
purple_color = "\033[95m"
cyan_color = "\033[96m"

def get_terminal_size():
    try:
        size = shutil.get_terminal_size((80, 20))
        return size.columns, size.lines
    except Exception as e:
        return 80, 20  # Default size

# Get terminal size
terminal_width, terminal_height = get_terminal_size()

# Center text function
def center_text(text, width):
    return text.center(width)

# Define menu options
main_menu_options = [
    f"{red_color}1) Gestión de Asignatura{reset_color}",
    f"{red_color}2) Gestión de Nivel{reset_color}",
    f"{red_color}3) Gestión de Periodo{reset_color}",
    f"{red_color}4) Gestión de Estudiante{reset_color}",
    f"{red_color}5) Gestión de Profesor{reset_color}",
    f"{red_color}6) Gestión de Notas{reset_color}",
    f"{red_color}7) Salir{reset_color}"
]

def print_centered_menu(title, options):
    borrarPantalla()
    title_line = center_text(title, terminal_width)
    print(title_line)
    print()  # Blank line for spacing
    for option in options:
        print(center_text(option, terminal_width))

opc = ''
while opc != '7':
    print_centered_menu(f"{red_color}Gestión Académica{reset_color}", main_menu_options)
    opc = input("Seleccione una opción: ").strip()

    if opc == "1":
        while opc != '6':
            borrarPantalla()
            crud_asignatura = CrudAsignatura()
            print_centered_menu(f"{blue_color}CRUD Asignaturas{reset_color}", [
                f"{blue_color}1) Crear Asignatura{reset_color}",
                f"{blue_color}2) Actualizar Asignatura{reset_color}",
                f"{blue_color}3) Eliminar Asignatura{reset_color}",
                f"{blue_color}4) Consultar Asignatura{reset_color}",
                f"{blue_color}5) Asignar Profesor a Asignatura{reset_color}",
                f"{blue_color}6) Salir{reset_color}"
            ])
            opc = input("Seleccione una opción: ").strip()

            if opc == "1":
                crud_asignatura.create()
            elif opc == "2":
                crud_asignatura.update()
            elif opc == "3":
                crud_asignatura.delete()
            elif opc == "4":
                crud_asignatura.consult()
            elif opc == "5":
                crud_asignatura.assign_profesor()
            print("Regresando al menú CRUD Asignaturas...")
            time.sleep(2)

    elif opc == "2":
        while opc != '5':
            borrarPantalla()
            crud_nivel = CrudNivel()
            print_centered_menu(f"{blue_color}CRUD Niveles{reset_color}", [
                f"{blue_color}1) Crear Nivel{reset_color}",
                f"{blue_color}2) Actualizar Nivel{reset_color}",
                f"{blue_color}3) Eliminar Nivel{reset_color}",
                f"{blue_color}4) Consultar Nivel{reset_color}",
                f"{blue_color}5) Salir{reset_color}"
            ])
            opc = input("Seleccione una opción: ").strip()

            if opc == "1":
                crud_nivel.create()
            elif opc == "2":
                crud_nivel.update()
            elif opc == "3":
                crud_nivel.delete()
            elif opc == "4":
                crud_nivel.consult()
            print("Regresando al menú CRUD Niveles...")
            time.sleep(2)

    elif opc == "3":
        while opc != '5':
            borrarPantalla()
            crud_periodo = CrudPeriodo()
            print_centered_menu(f"{yellow_color}CRUD Periodos{reset_color}", [
                f"{yellow_color}1) Crear Periodo{reset_color}",
                f"{yellow_color}2) Actualizar Periodo{reset_color}",
                f"{yellow_color}3) Eliminar Periodo{reset_color}",
                f"{yellow_color}4) Consultar Periodo{reset_color}",
                f"{yellow_color}5) Salir{reset_color}"
            ])
            opc = input("Seleccione una opción: ").strip()

            if opc == "1":
                crud_periodo.create()
            elif opc == "2":
                crud_periodo.update()
            elif opc == "3":
                crud_periodo.delete()
            elif opc == "4":
                crud_periodo.consult()
            print("Regresando al menú CRUD Periodos...")
            time.sleep(2)

    elif opc == "4":
        while opc != '6':
            borrarPantalla()
            crud_estudiante = CrudEstudiante()
            print_centered_menu(f"{yellow_color}CRUD Estudiantes{reset_color}", [
                f"{yellow_color}1) Crear Estudiante{reset_color}",
                f"{yellow_color}2) Actualizar Estudiante{reset_color}",
                f"{yellow_color}3) Eliminar Estudiante{reset_color}",
                f"{yellow_color}4) Consultar Estudiante{reset_color}",
                f"{yellow_color}5) Asignar Estudiante a Asignatura{reset_color}",
                f"{yellow_color}6) Salir{reset_color}"
            ])
            opc = input("Seleccione una opción: ").strip()

            if opc == "1":
                crud_estudiante.create()
            elif opc == "2":
                crud_estudiante.update()
            elif opc == "3":
                crud_estudiante.delete()
            elif opc == "4":
                crud_estudiante.consult()
            elif opc == "5":
                crud_estudiante.assign_subject()
            print("Regresando al menú CRUD Estudiantes...")
            time.sleep(2)

    elif opc == "5":
        while opc != '5':
            borrarPantalla()
            crud_profesor = CrudProfesor()
            print_centered_menu(f"{yellow_color}CRUD Profesores{reset_color}", [
                f"{yellow_color}1) Crear Profesor{reset_color}",
                f"{yellow_color}2) Actualizar Profesor{reset_color}",
                f"{yellow_color}3) Eliminar Profesor{reset_color}",
                f"{yellow_color}4) Consultar Profesor{reset_color}",
                f"{yellow_color}5) Salir{reset_color}"
            ])
            opc = input("Seleccione una opción: ").strip()

            if opc == "1":
                crud_profesor.create()
            elif opc == "2":
                crud_profesor.update()
            elif opc == "3":
                crud_profesor.delete()
            elif opc == "4":
                crud_profesor.consult()
            print("Regresando al menú CRUD Profesores...")
            time.sleep(2)

    elif opc == "6":
        while opc != '5':
            borrarPantalla()
            crud_nota = CrudNota()
            print_centered_menu(f"{yellow_color}CRUD Notas{reset_color}", [
                f"{yellow_color}1) Crear Nota{reset_color}",
                f"{yellow_color}2) Actualizar Nota{reset_color}",
                f"{yellow_color}3) Eliminar Nota{reset_color}",
                f"{yellow_color}4) Consultar Nota{reset_color}",
                f"{yellow_color}5) Salir{reset_color}"
            ])
            opc = input("Seleccione una opción: ").strip()

            if opc == "1":
                crud_nota.create()
            elif opc == "2":
                crud_nota.update()
            elif opc == "3":
                crud_nota.delete()
            elif opc == "4":
                crud_nota.consult()
            print("Regresando al menú CRUD Notas...")
            time.sleep(2)

    print("Regresando al menú Principal...")
    time.sleep(2)

borrarPantalla()
input("Presione una tecla para salir...")
borrarPantalla()
