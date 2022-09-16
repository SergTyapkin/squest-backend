import os
from flask import Flask

from blueprints.user import app as user_app
from blueprints.admin import app as admin_app
from blueprints.quest import app as quest_app
from blueprints.branch import app as branch_app
from blueprints.task import app as task_app
from blueprints.image import app as image_app
from blueprints.rating import app as rating_app
from middleware import Middleware
from utils.utils import read_config

_config = read_config('config.json')

app = Flask(__name__)
app.wsgi_app = Middleware(app.wsgi_app, url_prefix='/api', cors_origins=_config['cors-origins'])

app.register_blueprint(user_app,   url_prefix='/user')
app.register_blueprint(admin_app,  url_prefix='/admin')
app.register_blueprint(quest_app,  url_prefix='/quest')
app.register_blueprint(branch_app, url_prefix='/branch')
app.register_blueprint(task_app,   url_prefix='/task')
app.register_blueprint(image_app,   url_prefix='/image')
app.register_blueprint(rating_app,   url_prefix='/ratings')


@app.route('/')
def home():
    return "Это начальная страница API для сайта с онлайн-квестами, а не сайт. Вiйди отсюда!"


@app.errorhandler(404)
def error404(err):
    print(err)
    return "404 страница не найдена"


@app.errorhandler(500)
def error500(err):
    print(err)
    return "500 внутренняя ошибка сервера"


if __name__ == '__main__':
    port = int(os.environ.get('PORT', _config['api_port']))
    app.run(port=port, debug=bool(_config['debug']))
