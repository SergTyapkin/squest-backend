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

    resp = _DB.execute(sql.updateUserConfirmationByUsername, [isConfirmed, username])
    if len(resp) == 0:
        return jsonResponse("Имя пользователя не найдено", HTTP_NOT_FOUND)

    return jsonResponse("Успешно обновлено")


@app.route("/sql", methods=["POST"])
@login_required_admin
def executeSQL():
    try:
        req = request.json
        sqlText = req['sql']
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    try:
        resp = _DB.execute(sqlText, manyResults=True)
        return jsonResponse({"response": resp})
    except Exception as err:
        return jsonResponse(str(err), HTTP_INTERNAL_ERROR)
