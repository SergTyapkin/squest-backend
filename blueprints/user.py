import uuid
from datetime import datetime, timedelta

from flask import Blueprint

from utils.access import *
from constants import *
from utils.utils import *

app = Blueprint('user', __name__)

_DB = Database(read_config("config.json"))


def new_session(resp):
    tokenResp = _DB.execute(sql.selectSessionById, [resp['id']])
    if len(tokenResp) > 0:
        token = tokenResp['token']
        expires = tokenResp['expires']
    else:
        token = str(uuid.uuid4())
        expires = (datetime.now() + timedelta(seconds=24 * 60 * 60)).strftime("%Y-%m-%d %H:%M:%S")  # 24 * 60 * 60 = 1 day
        _DB.execute(sql.insertSession, [resp['id'], token, expires])

    res = jsonResponse(resp)
    res.set_cookie("session_token", token, expires=expires)
    return res


@app.route("/auth", methods=["POST"])
def userAuth():
    try:
        req = request.json
        username = req['username']
        password = req['password']
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    resp = _DB.execute(sql.selectUserByNamePassword, [username, password])
    if len(resp) == 0:
        return jsonResponse("Неверные логин или пароль", HTTP_INVALID_AUTH_DATA)

    return new_session(resp)


@app.route("/session", methods=["DELETE"])
def userSessionDelete():
    token = request.cookies.get('session_token')
    if not token:
        return jsonResponse("Вы не вошли в аккаунт", HTTP_NO_PERMISSIONS)

    try:
        _DB.execute(sql.deleteSessionByToken, [token])
    except:
        return jsonResponse("Сессия не удалена", HTTP_INTERNAL_ERROR)

    return jsonResponse("Вы вышли из аккаунта")


@app.route("")
@login_required
def userGet(userData):
    return jsonResponse(userData)


@app.route("", methods=["POST"])
def userCreate():
    try:
        req = request.json
        name = req['name']
        password = req['password']
        avatarUrl = req.get('avatarUrl')
        email = req.get('email')
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    try:
        resp = _DB.execute(sql.insertUser, [name, password, avatarUrl, email])
    except:
        return jsonResponse("Имя пользователя или email заняты", HTTP_INVALID_DATA)

    return new_session(resp)


@app.route("", methods=["PUT"])
@login_required
def userUpdate(userData):
    try:
        req = request.json
        name = req.get('name')
        email = req.get('email')
        avatarUrl = req.get('avatarUrl')
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    name = name or userData['name']
    email = email or userData['email']
    avatarUrl = avatarUrl or userData['avatarurl']

    try:
        resp = _DB.execute(sql.updateUserById, [name, email, avatarUrl, userData['id']])
    except:
        return jsonResponse("Имя пользователя или email заняты", HTTP_INVALID_DATA)

    return jsonResponse(resp)


@app.route("", methods=["DELETE"])
@login_required_return_id
def userDelete(userId):
    _DB.execute(sql.deleteUserById, [userId])
    return jsonResponse("Пользователь удален")


@app.route("/password", methods=["PUT"])
@login_required_return_id
def userUpdatePassword(userId):
    try:
        req = request.json
        oldPassword = req['oldPassword']
        newPassword = req['newPassword']
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    # if (userData['name'] != username) and (not userData['isadmin']):
    #     return jsonResponse("Нет прав", HTTP_NO_PERMISSIONS)

    _DB.execute(sql.updateUserPasswordByIdPassword, [newPassword, userId, oldPassword])
    return jsonResponse("Успешно обновлено")
