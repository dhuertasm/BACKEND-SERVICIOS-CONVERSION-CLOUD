import subprocess
from pydub import AudioSegment
import glob

from modelos import db
from modelos import Tarea
from modelos import Archivo
import os

from constans import UPLOAD_FOLDER


class ExportMusic:

    def __init__(self):
        pass


    def update_state_archivosubido(self, state_i, state_f) -> None:
        db.session.query(Tarea).filter(Tarea.estado == state_i).\
            update({Tarea.estado: state_f}, synchronize_session=False)
        db.session.commit()

    def update_database_archivotranformado(self, data) -> None:
        nueva_archivotranformado = Archivo(
                                nombre_archivo=data["nombre_archivo"],
                                ruta_archivo=data["ruta_archivo"],
                                id_tarea=data["id_tarea"]
        )
        db.session.add(nueva_archivotranformado)
        db.session.query(Tarea).filter(Tarea.id == data["id_tarea"]). \
            update({Tarea.estado: 'processed'}, synchronize_session=False)
        db.session.commit()

    def query_database_archivosubido(self) -> list:
        all_uploaded = db.session.query(Tarea).filter(Tarea.estado == 'pending').all()
        return [
                 {"formato_entrada": i.formato_entrada,
                  'id_tarea': i.id,
                  'formato_salida': i.formato_salida,
                  'nombre_archivo': i.nombre_archivo}
            for i in all_uploaded
        ]

    def read_file(self, data):
        pass

    def export_file(self, data):
        name = '{}.{}'.format(data['nombre_archivo'], data['formato_salida'])
        file_export = f"{UPLOAD_FOLDER}/{name}"
        file_path = '{}/{}.{}'.format(UPLOAD_FOLDER, data['nombre_archivo'], data['formato_entrada'])
        dir_actual = os.path.dirname(os.path.abspath(__file__))
        print('file_export', file_export)
        print('file_path', file_path)
        print(glob.glob(UPLOAD_FOLDER+"/*", recursive=True))
        print(glob.glob(UPLOAD_FOLDER+ "/*", recursive=True))
        try:
            converter = subprocess.call(['ffmpeg', '-i', file_path,
                             file_export])

            if converter == 0:
                save_file = {
                    "nombre_archivo": name,
                    'ruta_archivo': file_export,
                    'id_tarea': data['id_tarea'],

                }
                self.update_database_archivotranformado(save_file)
                return True

            db.session.query(Tarea).filter(Tarea.id == data["id_tarea"]). \
                update({Tarea.estado: 'uploaded'}, synchronize_session=False)
            db.session.commit()
        except Exception as e:
            print(e)
            return False

    def process(self):
        self.update_state_archivosubido("uploaded", "pending")
        files_to_export = self.query_database_archivosubido()
        for data in files_to_export:
            self.export_file(data)




