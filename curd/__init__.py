from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from config import Config
from celery import Celery
from flask_httpauth import HTTPBasicAuth
import os


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],  # 存储状态和运行结果
        broker=app.config['CELERY_BROKER_URL']  # 队列运行的url
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app = Flask(__name__)
api = Api(app)
CORS(app)
app.config.from_object(Config)
auth = HTTPBasicAuth()

from . import controller

api.add_resource(controller.all_machine, '/api/machine/')
api.add_resource(controller.admin_register, '/api/login/')
api.add_resource(controller.test_task_action, '/api/test_task/')
api.add_resource(controller.run_task, '/api/runTask/')


