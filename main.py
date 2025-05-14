import os
from flask import Flask
from flask_mail import Mail

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
app.wsgi_app = Middleware(app.wsgi_app, cors_origins=_config['cors-origins'])

app.register_blueprint(user_app,   url_prefix='/user')
app.register_blueprint(admin_app,  url_prefix='/admin')
app.register_blueprint(quest_app,  url_prefix='/quest')
app.register_blueprint(branch_app, url_prefix='/branch')
app.register_blueprint(task_app,   url_prefix='/task')
app.register_blueprint(image_app,   url_prefix='/image')
app.register_blueprint(rating_app,   url_prefix='/ratings')

app.config['MAIL_SERVER'] = _config['SMTP_mail_server_host']
app.config['MAIL_PORT'] = _config['SMTP_mail_server_port']
app.config['MAIL_USE_TLS'] = _config['SMTP_mail_server_use_tls']
app.config['MAIL_USERNAME'] = _config['mail_address']
app.config['MAIL_DEFAULT_SENDER'] = _config['mail_sender_name']
app.config['MAIL_PASSWORD'] = _config['mail_password']

mail = Mail(app)


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
    app.run(port=9000, debug=bool(_config['debug']))
