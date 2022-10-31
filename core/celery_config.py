import os
from celery import Celery
# from core.format_converte import ExportMusic
#
BROKER_URL = os.environ.get('BROKER_URL', 'redis://localhost:6379')
#
# app = Celery('tasks',
#              broker=BROKER_URL,
#              include=['core.tasks']
#              )
#
# # @app.task()
# # def add_test(a, b):
# #     ExportMusic().process()
# #     return a + b
#
#
# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))
#
#
# app.conf.beat_schedule = {
#     'add-every-30-seconds': {
#         'task': 'core.tasks.add',
#         'schedule': 10.0,
#         'args': (16, 16)
#     },
#     'add-every-30': {
#         'task': 'core.tasks.my_task',
#         'schedule': 30.0,
#
#     },
# }
from core import celeryconfig
def make_celery(app):
    # create context tasks in celery
    celery = Celery(
        'tasks',
        broker=BROKER_URL,
        include=['core.tasks']
    )
    TaskBase = celery.Task
    celery.config_from_object(celeryconfig)
    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery
