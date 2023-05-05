from tinydb import TinyDB, Query
from datetime import datetime
from typing import List
import os


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


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
        
    def actualizar_ids_tareas(self):
        tareas = self.tareas.all()
        tareas_ordenadas = sorted(tareas, key=lambda tarea: int(tarea['id']) if 'id' in tarea else 0)
        ids_existente = set(map(lambda tarea: tarea['id'], tareas))
        
        for i, tarea in enumerate(tareas_ordenadas):
            tarea_id_anterior = tarea['id']
            nueva_tarea = tarea.copy()
            nueva_tarea['id'] = i + 1

            while nueva_tarea['id'] in ids_existente:
                nueva_tarea['id'] += 1

            self.tareas.update(nueva_tarea, Query().id == tarea_id_anterior)
            ids_existente.add(nueva_tarea['id'])

    def get_last_id(self) -> int:
        last_tarea = self.tareas.get(doc_id=len(self.tareas))
        if last_tarea is not None:
            return last_tarea['id']
        else:
            return 0

    def agregar_tarea(self, tarea: Tarea) -> int:
        last_id = self.get_last_id()
        if last_id == 0:
            estado = 'en proceso'
        else:
            estado = 'en espera'
        tarea_dict = {
            'id': last_id + 1,
            'titulo': tarea.titulo,
            'descripcion': tarea.descripcion,
            'estado': estado,
            'creada': tarea.creada,
            'actualizada': tarea.actualizada
        }
        tarea_id = self.tareas.insert(tarea_dict)
        return tarea_id

    def traer_tarea(self, tarea_id: int) -> Tarea:
        TareaQuery = Query()
        tarea_dict = self.tareas.get(TareaQuery.id == tarea_id)
        if tarea_dict:
            tarea = Tarea(
                tarea_dict['id'],
                tarea_dict['titulo'],
                tarea_dict['descripcion'],
                tarea_dict['estado'],
                tarea_dict['creada'],
                tarea_dict['actualizada']
            )
            tarea.estado = tarea_dict['estado']
            return tarea
        else:
            return None

    def actualizar_estado_tarea(self, tarea_id: int, estado: str):
        self.tareas.update({'estado': estado, 'actualizada': str(datetime.now())}, Query().id == tarea_id)

    def eliminar_tarea(self, tarea_id: int):
        tarea = self.tareas.get(Query().id == tarea_id)
        if tarea is not None:
            self.tareas.remove(doc_ids=[tarea.doc_id])
            for tareaPosterior in self.tareas.search(Query().id > tarea_id):
                self.tareas.update({'id': tareaPosterior['id'] - 1},
                                   doc_ids=[tareaPosterior.doc_id])
        else:
            print("No se encontró la tarea con ID", tarea_id)

    def eliminar_todas_las_tareas(self):
        self.tareas.truncate()
        print("Se han eliminado todas las tareas")

    
    def traer_todas_tareas(self) -> List[Tarea]:
        tareas_dicts = self.tareas.all()
        return [Tarea(
            tarea_dict['id'],
            tarea_dict['titulo'],
            tarea_dict['descripcion'],
            tarea_dict['estado'],
            tarea_dict['creada'],
            tarea_dict['actualizada']
        ) for tarea_dict in tareas_dicts]
    

if __name__ == '__main__':
    admin_tareas = AdminTarea('db.json')


    while True:
        print('Ingrese una opción:')
        print('1. Agregar tarea')
        print('2. Ver tarea')
        print('3. Eliminar tarea')
        print('4. Ver todas las tareas')
        print('5. Salir')
        print("\n")

        opcion = input('Opción: ')

        if opcion == "1":
            titulo = input("Ingrese el título de la tarea: ")
            descripcion = input("Ingrese la descripción de la tarea: ")
            estado = "creando"
            creada = str(datetime.now())
            actualizada = creada
            
            tarea = Tarea(None, titulo, descripcion, estado, creada, actualizada)
            
            tarea_id = admin_tareas.agregar_tarea(tarea)
            clear_console()
            print("Se ha agregado la tarea con ID\n", tarea_id)
        
        elif opcion == "2":
            clear_console()
            while True:
                try:
                    tarea_id = int(input("Ingrese el ID de la tarea: "))
                    break
                except ValueError:
                    print("Código no válido")
                    
            tarea = admin_tareas.traer_tarea(tarea_id)

            if tarea:
                print("ID:", tarea.id)
                print("Título:", tarea.titulo)
                print("Descripción:", tarea.descripcion)
                print("Estado:", tarea.estado)
                print("Creada:", tarea.creada)
                print("Actualizada:", tarea.actualizada)
                print("\n")
            else:
                print("No se encontró la tarea con ID", tarea_id)
                
        
        elif opcion == "3":
            clear_console()
            opcion = input("Ingrese '1' para eliminar una tarea o '2' para eliminar todas las tareas: ")
            if opcion == '1':
                tarea_id = int(input("Ingrese el ID de la tarea: "))
                admin_tareas.eliminar_tarea(tarea_id)
                print("Se ha eliminado la tarea con ID", tarea_id)
                
            elif opcion == '2':
                admin_tareas.eliminar_todas_las_tareas()
            else:
                print("Opción inválida.")
               
        elif opcion == "4":
            clear_console()

            tareas = admin_tareas.traer_todas_tareas()
            
            if tareas:
                for tarea in tareas:
                    print("ID:", tarea.id)
                    print("Título:", tarea.titulo)
                    print("Descripción:", tarea.descripcion)
                    print("Estado:", tarea.estado)
                    print("Creada:", tarea.creada)
                    print("Actualizada:", tarea.actualizada)
                    print("\n")
            else:
                print("No hay tareas registradas.")

        elif opcion == "5":
                break

        else:
            print("Opción inválida. Por favor, intenta de nuevo.")
