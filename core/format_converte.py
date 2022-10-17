from pydub import AudioSegment
from modelos import db
from modelos import ArchivoSubido
from modelos import ArchivoTranformado

class ExportMusic:

    def __init__(self):
        pass

    @staticmethod
    def update_state_archivosubido(state_i, state_f) -> None:
        db.session.query(ArchivoSubido).filter(ArchivoSubido.estado_proceso == state_i).\
            update({ArchivoSubido.estado_proceso: state_f}, synchronize_session=False)

    def update_database_archivotranformado(state_i, data) -> None:
        nueva_archivotranformado = ArchivoTranformado(
                                nombre_archivo=data["nombre_archivo"],
                                ruta_archivo=data["ruta_archivo"],
                                formato_salida=data["formato_salida"],
                                id_archivosubido=data["id_archivosubido"],
                                id_usuario=data["id_usuario"]
        )
        db.session.add(nueva_archivotranformado)
        db.session.commit()

    def query_database_archivosubido(self) -> dict:
        all_uploaded = db.session.query(ArchivoSubido).filter(ArchivoSubido.estado_proceso == 'uploaded').all()
        return {i.formato_entrada: [i.ruta_archivo, i.formato_salida] for i in all_uploaded}

    def read_file(self, type_file, file_path):
        if "mp3" == type_file:
            return AudioSegment.from_mp3(file_path)
        elif "aac" == type_file:
            return AudioSegment.from_file(file_path, "aac")
        elif "ogg" == type_file:
            return AudioSegment.from_ogg(file_path)
        elif "wav" == type_file:
            return AudioSegment.from_wav(file_path)
        elif "wma" == type_file:
            return AudioSegment.from_file(file_path, "wma")
        return False

    def export_file(self, file, format, name):
        if file:
            name = '.'.join(name.split('.')[0:-1] + [format])
            file_export = f"./media/transformados/{name}"
            file.export(file_export, format=format)
            data = {

            }
            self.update_database_archivotranformado()


    def process(self):
        self.update_state_archivosubido("uploaded", "pending")
        files_to_export = self.query_database_archivosubido()
        for type_file, export in files_to_export.items():
            read_file = self.read_file(type_file, export[0])
            self.export_file(read_file, export[1], export[0])
        self.update_state("pending", "processed")




