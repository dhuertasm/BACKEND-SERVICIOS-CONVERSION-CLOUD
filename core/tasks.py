import glob
from core.celery import app
from core.format_converte import ExportMusic

from app import app as flask
from constans import UPLOAD_FOLDER

@app.task()
def add(a, b):
    print(UPLOAD_FOLDER)
    print(glob.glob(UPLOAD_FOLDER+"/*", recursive=True))
    return a + b

@app.task()
def my_task():
    flask.app_context().push()
    export = ExportMusic()
    export.process()



