import os
from constans import UPLOAD_FOLDER

INPUT_FILES_FOLDER = UPLOAD_FOLDER+"/"


def upload_file(archivo_cargado, nombre_archivo):
    print(type(archivo_cargado.encode('utf8')))
    archivo_cargado = archivo_cargado.encode('utf8')
    from werkzeug.datastructures import FileStorage
    a = FileStorage(archivo_cargado)
    print(type(a))
    a.save(os.path.join(INPUT_FILES_FOLDER, nombre_archivo))
    print('subio')