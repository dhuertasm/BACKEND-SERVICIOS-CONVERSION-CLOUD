import glob
import celery

from core.format_converte import ExportMusic

from constans import UPLOAD_FOLDER

@celery.shared_task()
def add(a, b):
    print(UPLOAD_FOLDER)
    print(glob.glob(UPLOAD_FOLDER+"/*", recursive=True))
    return a + b

@celery.shared_task()
def my_task():
    # create_app().app_context().push()
    export = ExportMusic()
    export.process()
