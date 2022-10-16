from celery import Celery


import logging

BROKER_URL = 'redis://localhost:6379'

app = Celery('tasks', broker=BROKER_URL)

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):

    # Calls test('world') every 30 seconds
    sender.add_periodic_task(10.0, add.s(1, 1), expires=10)


@app.task()
def add(a, b):
    return a + b


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


