from tinydb import TinyDB, Query
from datetime import datetime
from typing import List
import os
import json

from rich.console import Console
from rich.table import Table

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_tarea(tarea):
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID")
    table.add_column("Título")
    table.add_column("Descripción")
    table.add_column("Estado")
    table.add_column("Creada")
    table.add_column("Actualizada")

    table.add_row(
        str(tarea.id),
        tarea.titulo,
        tarea.descripcion,
        tarea.estado,
        str(tarea.creada),
        str(tarea.actualizada),
        )

    console.print(table)

def mostrar_tareas(tareas):
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID")
    table.add_column("Título")
    table.add_column("Descripción")
    table.add_column("Estado")
    table.add_column("Creada")
    table.add_column("Actualizada")

    for tarea in tareas:
        table.add_row(
            str(tarea.id),
            tarea.titulo,
            tarea.descripcion,
            tarea.estado,
            str(tarea.creada),
            str(tarea.actualizada),
        )

    console.print(table)

class Tarea:
    def __init__(self, id, titulo, descripcion, estado, creada, actualizada):
        self.id = id
        self.titulo = titulo
        self.descripcion = descripcion
        self.estado = estado
        self.creada = creada
        self.actualizada = actualizada


class AdminTarea:
    def __init__(self, db):
        self.db = TinyDB(db)
        self.tareas = self.db.table('tareas')

    def get_last_id(self) -> int:
        tareas = self.tareas.all()
        if tareas:
            last_tarea = tareas[-1]
            return last_tarea['id']
        else:
            return 0

    def agregar_tarea(self, tarea: Tarea) -> int:
        last_id = self.get_last_id()
        tarea_dict = {
            'id': last_id + 1,
            'titulo': tarea.titulo,
            'descripcion': tarea.descripcion,
            'estado': "creada",
            'creada': tarea.creada,
            'actualizada': tarea.actualizada
        }
        tarea_id = self.tareas.insert(tarea_dict)
        return tarea_id

    def traer_tarea(self, tarea_id: int) -> Tarea:
        TareaQuery = Query()
        tarea_dict = self.tareas.get((TareaQuery.id == tarea_id) & (TareaQuery.estado != "eliminada"))
        if tarea_dict:
            tarea = Tarea(
                tarea_dict['id'],
                tarea_dict['titulo'],
                tarea_dict['descripcion'],
                tarea_dict['estado'],
                tarea_dict['creada'],
                tarea_dict['actualizada']
            )
            return tarea
        else:
            return None

    def traer_todas_tareas(self) -> List[Tarea]:
        TareaQuery = Query()
        tareas_dicts = self.tareas.search(TareaQuery.estado != "eliminada")
        return [Tarea(
            tarea_dict['id'],
            tarea_dict['titulo'],
            tarea_dict['descripcion'],
            tarea_dict['estado'],
            tarea_dict['creada'],
            tarea_dict['actualizada']
        ) for tarea_dict in tareas_dicts]
    
    def actualizar_estado_tarea(self, tarea_id: int, titulo: str = None, descripcion: str = None, estado: str = None):
        tarea = self.traer_tarea(tarea_id)
        if tarea:
            tarea_dict = {'actualizada': str(datetime.now())}
            if titulo is not None:
                tarea_dict['titulo'] = titulo
            if descripcion is not None:
                tarea_dict['descripcion'] = descripcion
            if estado is not None:
                tarea_dict['estado'] = estado
            self.tareas.update(tarea_dict, Query().id == tarea_id)

    def eliminar_tarea(self, tarea_id: int):
        tarea = self.traer_tarea(tarea_id)
        if tarea is not None:
            if tarea.estado != "eliminada":
                tarea.estado = "eliminada"
                tarea.actualizada = str(datetime.now())
                self.actualizar_estado_tarea(tarea_id, estado="eliminada")
                return True
            else:
                return False


    def eliminar_todas_las_tareas(self):
        tareas = self.traer_todas_tareas()
        if len(tareas) > 0:
            for tarea in tareas:
                tarea.estado = "eliminada"
                self.actualizar_estado_tarea(tarea.id, estado=tarea.estado)
            return True
        else:
            return False
        

if __name__ == '__main__':
    admin_tareas = AdminTarea('db.json')


    while True:
        print("\n")
        print('Ingrese una opción:')
        print('1. Agregar tarea')
        print('2. Ver tarea')
        print('3. Eliminar tarea')
        print('4. Editar Tarea')
        print('5. Salir')
        print("\n")

        opcion = input('Opción: ')

        if opcion == "1":
            titulo = input("Ingrese el título de la tarea: ")
            if titulo == "":
                last_id = admin_tareas.get_last_id()
                titulo = "Tarea " + str(last_id + 1)
            descripcion = input("Ingrese la descripción de la tarea: ")
            estado = "Creado"
            creada = str(datetime.now())
            actualizada = creada
            
            tarea = Tarea(None, titulo, descripcion, estado, creada, actualizada)
            
            tarea_id = admin_tareas.agregar_tarea(tarea)
            clear_console()
            print("Se ha agregado la tarea con ID\n", tarea_id)
        
        elif opcion == "2":
            clear_console()
            print("\n")
            opcion = input("Ingrese 1 para ver una tarea particular o 2 para ver todas las tareas: ")
            print("\n")
            if opcion == '1':
                try:
                    tarea_id = int(input("Ingrese el ID de la tarea: "))
                    print("\n")
                    tarea = admin_tareas.traer_tarea(tarea_id)
                    if tarea:
                        mostrar_tarea(tarea)
                    else:
                        print("No se encontró la tarea con ID", tarea_id)
                        print("\n")
                except ValueError:
                    clear_console()
                    print("Opción inválida")

            elif opcion == '2':
                tareas = admin_tareas.traer_todas_tareas()
                if tareas:
                        mostrar_tareas(tareas)
                else:
                    print("No hay tareas registradas.")
                    print("\n")
            else:
                print("Opción inválida.")
                print("\n")
        
        elif opcion == "3":
            clear_console()
            opcion = input("Ingrese 1 para eliminar una tarea o 2 para eliminar todas las tareas: ")
            if opcion == '1':
                try:
                    tarea_id = int(input("Ingrese el ID de la tarea: "))
                    eliminada = admin_tareas.eliminar_tarea(tarea_id)
                    if eliminada:
                        print("Se ha eliminado la tarea con ID", tarea_id)
                    else:
                        print("No se encontro tarea para eliminar")
                except ValueError:
                    clear_console()
                    print("Opción inválida")

            elif opcion == '2':

                eliminada = admin_tareas.eliminar_todas_las_tareas()
                if eliminada:
                    print("Se han eliminado todas las tareas")
                else:
                    print("No hay tareas que eliminar")
            else:
                print("Opción inválida.")
               
        elif opcion == "4":
            try:
                tarea_id = int(input("Ingrese el ID de la tarea: "))
                tarea = admin_tareas.traer_tarea(tarea_id)
                if tarea is not None:
                    opcion = input("Ingrese 1 para actualizar título, 2 para actualizar descripción o 3 para editar todo: ")
                    if opcion == '1':
                        titulo = input("Ingrese el nuevo título: ")
                        admin_tareas.actualizar_estado_tarea(tarea_id, titulo=titulo)
                        clear_console()
                        print("Se ha actualizado el título de la tarea con ID", tarea.id)
                    elif opcion == '2':
                        descripcion = input("Ingrese la nueva descripción: ")
                        admin_tareas.actualizar_estado_tarea(tarea_id, descripcion=descripcion)
                        clear_console()
                        print("Se ha actualizado la descripción de la tarea con ID", tarea.id)
                    elif opcion == '3':
                        titulo = input("Ingrese el nuevo título: ")
                        descripcion = input("Ingrese la nueva descripción: ")
                        admin_tareas.actualizar_estado_tarea(tarea_id, titulo=titulo, descripcion=descripcion)
                        clear_console()
                        print("Se ha actualizado la tarea con ID", tarea.id)
                    else:
                        print("Opción inválida")
                else:
                    print("No se encontró la tarea con ID", tarea_id)
            except ValueError:
                clear_console()
                print("Opción inválida")

        
        elif opcion == "5":
                break
        
        elif opcion == "66":
            archivo_tareas = 'db.json'
            with open(archivo_tareas, 'w') as archivo:
                json.dump({},archivo)
            print("Orden 66 ejecutada")

        else:
            print("Opción inválida. Por favor, intenta de nuevo.")
