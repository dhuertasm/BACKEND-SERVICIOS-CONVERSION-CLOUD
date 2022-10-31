import subprocess
from pydub import AudioSegment
import glob

from email.message import EmailMessage
import smtplib

from modelos import db
from modelos import Tarea
from modelos import Archivo
from modelos import Usuario
import os
import time
from flask import current_app

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
                                id_tarea=data["id_tarea"],
                                tiempo_proceso=data["tiempo_proceso"]
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
                  'nombre_archivo': i.nombre_archivo,
                  'id_usuario':i.user_id}
            for i in all_uploaded
        ]

    def read_file(self, data):
        pass

    def export_file(self, data):
        print('export')
        name = '{}.{}'.format(data['nombre_archivo'], data['formato_salida'])
        file_export = f"{UPLOAD_FOLDER}/{name}"
        file_path = '{}/{}.{}'.format(UPLOAD_FOLDER, data['nombre_archivo'], data['formato_entrada'])
        try:
            #
            init = time.time()
            converter = subprocess.call(['ffmpeg', '-i', file_path,
                             file_export])
            end_n = time.time()
            time_operation = end_n - init
            print("time", end_n - init)
            #
            if converter == 0:
                save_file = {
                    "nombre_archivo": name,
                    'ruta_archivo': file_export,
                    'id_tarea': data['id_tarea'],
                    'tiempo_proceso': str(time_operation)

                }
                self.update_database_archivotranformado(save_file)
                #
                enviar_mail(data)
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



def enviar_mail(data):

    destinatario = db.session.query(Usuario).get(data['id_usuario'])
    print(destinatario.email, data)
    remitente = "flask.nube@outlook.com"
    destinatario = destinatario.email
    mensaje = f"¡El Archivo {data['nombre_archivo']} fue tranformado!"
    email = EmailMessage()
    email["From"] = remitente
    email["To"] = destinatario
    email["Subject"] = f"Archvio {data['nombre_archivo']} tranformado"
    email.set_content(mensaje)
    smtp = smtplib.SMTP("smtp-mail.outlook.com", port=587)
    smtp.starttls()
    smtp.login(remitente, "flask.123")
    smtp.sendmail(remitente, destinatario, email.as_string())
    smtp.quit()