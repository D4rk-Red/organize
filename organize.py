import os
import shutil
from datetime import datetime
from collections import defaultdict


class FileManager:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.files = self.get_files()

    def get_files(self):
        # Obtiene la lista de archivos de la carpeta 
        files = [archivo for archivo in os.listdir(self.folder_path) if os.path.isfile(os.path.join(self.folder_path, archivo))]
        return files

    def create_folder(self, folder_name):
        # Crea una carpeta 
        folder_path = os.path.join(self.folder_path, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        return folder_path

    def move_files_to_folder(self, folder_path, files):
        # Mueve los archivos a la carpeta especificada
        for file in files:
            src_path = os.path.join(self.folder_path, file)
            dest_path = os.path.join(folder_path, file)
            shutil.move(src_path, dest_path)

    def order_by_date(self):
        # Ordena los archivos por fecha
        date_mapping = defaultdict(list)

        for file in self.files:
            file_path = os.path.join(self.folder_path, file)
            file_creation_time = os.path.getctime(file_path)
            file_date = datetime.utcfromtimestamp(file_creation_time).strftime('%Y-%m-%d')
            date_mapping[file_date].append(file)

        for date, files in date_mapping.items():
            folder_name = f"Fecha_{date}"
            folder_path = self.create_folder(folder_name)
            self.move_files_to_folder(folder_path, files)

    def order_by_name(self):
        # Ordena archivos por nombre
        name_mapping = defaultdict(list)

        for file in self.files:
            file_name = os.path.splitext(file)[0]  # Elimina la extensión del archivo
            name_mapping[file_name].append(file)

        for name, files in name_mapping.items():
            # Se detectan las palabras clave (las palabras antes del primer espacio)
            keywords = name.split(" ")[:1]
            folder_name = "_".join(keywords)
            folder_path = self.create_folder(folder_name)
            self.move_files_to_folder(folder_path, files)



def main():
    # Obtiene la ruta del script actual
    script_path = os.path.abspath(__file__)
    # Obtiene el directorio del script (sin el nombre del archivo)
    script_directory = os.path.dirname(script_path)
    file_manager = FileManager(script_directory)

    while True:
        print("\nMenu:")
        print("1. Ordenar por Fecha (Date)")
        print("2. Ordenar por Nombre (Name)")
        print("0. Salir")
        try:
            option = int(input("Seleccione una opción (Select an option): "))

            if option == 1:
                file_manager.order_by_date()
                print("Archivos ordenados por Fecha.")
                break
            elif option == 2:
                file_manager.order_by_name()
                print("Archivos ordenados por Nombre.")
                break
            elif option == 0:
                break
            else:
                print("Opción no válida.")
        except ValueError:
            print("Ingresa un numero.")


if __name__ == "__main__":
    main()

