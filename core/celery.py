from celery import Celery
from pydub import AudioSegment
BROKER_URL = 'redis://localhost:6379'

app = Celery('tasks', broker=BROKER_URL)

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):

    # Calls test('world') every 30 seconds
    sender.add_periodic_task(10.0, add_test.s(1, 1), expires=10)


@app.task()
def add_test(a, b):

    sound = AudioSegment.from_mp3("/path/to/file.mp3")
    sound.export("/output/path/file.wav", format="wav")
    return a + b


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


