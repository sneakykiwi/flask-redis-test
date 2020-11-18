from flask import Flask
from celery import Celery
from datetime import timedelta

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['result_backend'],
        broker=app.config['broker_url']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


application = app = Flask(__name__)
app.config['result_backend'] = 'redis://lredistest.3mesk0.ng.0001.use2.cache.amazonaws.com:6379'
app.config['broker_url'] = 'redis://redistest.3mesk0.ng.0001.use2.cache.amazonaws.com:6379'
celery = make_celery(app)

celery.conf.beat_schedule = {
    'add-every-monday-morning': {
        'task': 'app.print_hello',
        'schedule': timedelta(seconds=10),
    },
}


@app.route('/')
def home():
    result = add_together.delay(10, 5)
    print(result.wait())
    return 'Works'


@app.route('/test', methods=['GET'])
def test():
    return {'success': True}


@celery.task()
def add_together(a, b):
    return a + b


@celery.task()
def print_hello():
    print("THIS SHIT WORKS WELL")
