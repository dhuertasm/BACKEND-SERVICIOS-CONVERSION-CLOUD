import os
from celery import Celery
from core.format_converte import ExportMusic

BROKER_URL = os.environ.get('BROKER_URL', 'redis://localhost:6379')

app = Celery('tasks',
             broker=BROKER_URL,
             include=['core.tasks']
             )

# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#
#     # Calls test('world') every 30 seconds
#     sender.add_periodic_task(10.0, add_test.s(1, 1), expires=10)
#

@app.task()
def add_test(a, b):
    ExportMusic().process()
    return a + b


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'core.tasks.add',
        'schedule': 10.0,
        'args': (16, 16)
    },
    'add-every-30': {
        'task': 'core.tasks.my_task',
        'schedule': 30.0,

    },
}
