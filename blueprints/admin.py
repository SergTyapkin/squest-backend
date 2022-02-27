from flask import Blueprint

from utils.access import *
from constants import *
from utils.utils import *

app = Blueprint('admin', __name__)

_DB = Database(read_config("config.json"))


@app.route("/user/confirmation", methods=["PUT"])
@login_required_admin
def userUpdateConfirmation():
    try:
        req = request.json
        username = req['username']
        isConfirmed = req['isConfirmed']
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    resp = _DB.execute(sql.updateUserConfirmationByName, [isConfirmed, username])
    if len(resp) == 0:
        return jsonResponse("Имя пользователя не найдено", HTTP_NOT_FOUND)

    return jsonResponse("Успешно обновлено")
