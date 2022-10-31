from celery.schedules import crontab


CELERY_IMPORTS = ('core.tasks')


CELERYBEAT_SCHEDULE = {
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