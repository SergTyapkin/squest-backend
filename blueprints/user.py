import random
import uuid
from datetime import datetime, timedelta

from flask import Blueprint
from flask_mail import Mail, Message
from flask import current_app

from connctions import DB
from utils.access import *
from constants import *
from utils.utils import *

app = Blueprint('user', __name__)


def new_session(resp):
    tokenResp = DB.execute(sql.selectSessionByUserId, [resp['id']])
    if tokenResp:
        token = tokenResp['token']
        expires = tokenResp['expires']
    else:
        token = str(uuid.uuid4())
        expires = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
        DB.execute(sql.insertSession, [resp['id'], token, expires])

    DB.execute(sql.deleteExpiredSessions)

    res = jsonResponse(resp)
    res.set_cookie("session_token", token, expires=expires, httponly=True, samesite="lax")
    return res


def new_secret_code(userId, type):
    DB.execute(sql.deleteExpiredSecretCodes)

    secretCode = DB.execute(sql.selectSecretCodeByUserIdType, [userId, type])
    if secretCode:
        code = secretCode['code']
        return code

    # create new
    code = ''
    if type == "login":
        random.seed()
        code = str(random.randint(1, 999999)).zfill(6)
    elif type == "password":
        code = str(uuid.uuid4())

    expires = (datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
    DB.execute(sql.insertSecretCode, [userId, code, type, expires])

    return code


@app.route("/auth", methods=["POST"])
def userAuth():
    try:
        req = request.json
        username = req['username']
        password = req['password']
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    password = hash_sha256(password)

    resp = DB.execute(sql.selectUserByUsernamePassword, [username, password])
    if len(resp) == 0:
        return jsonResponse("Неверные логин или пароль", HTTP_INVALID_AUTH_DATA)

    return new_session(resp)


@app.route("/session", methods=["DELETE"])
def userSessionDelete():
    token = request.cookies.get('session_token')
    if not token:
        return jsonResponse("Вы не вошли в аккаунт", HTTP_NO_PERMISSIONS)

    try:
        DB.execute(sql.deleteSessionByToken, [token])
    except:
        return jsonResponse("Сессия не удалена", HTTP_INTERNAL_ERROR)

    res = jsonResponse("Вы вышли из аккаунта")
    res.set_cookie("session_token", "", max_age=-1, httponly=True, samesite="none", secure=True)
    return res


@app.route("")
@login_or_none
def userGet(userData):
    try:
        req = request.args
        userId = req.get('id')
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    def addRating(obj, id):
        res = DB.execute(sql.selectRatings, [], manyResults=True)
        positionDecrease = 0
        for idx, rating in enumerate(res):
            if rating['rating'] is None:
                positionDecrease += 1

            if str(rating['id']) == str(id):
                obj['rating'] = rating['rating'] or 0
                obj['position'] = idx + 1 - positionDecrease
                return
        obj['rating'] = 0
        obj['position'] = len(res)

    def addQuestsInfo(obj, id):
        createdQuests = DB.execute(sql.selectCreatedQuestsByUserid, [id])
        completedBranches = DB.execute(sql.selectCompletedBranchesByUserid, [id])
        obj['createdquests'] = createdQuests.get('questscreated') or 0
        obj['completedbranches'] = completedBranches.get('completedbranches') or 0


    if userId is None:  # return self user data
        if userData is None:
            return jsonResponse("Не авторизован", HTTP_INVALID_AUTH_DATA)
        addRating(userData, userData['id'])
        addQuestsInfo(userData, userData['id'])
        return jsonResponse(userData)

    # get another user data
    res = DB.execute(sql.selectAnotherUserById, [userId])
    if not res:
        return jsonResponse("Пользователь не найден", HTTP_NOT_FOUND)
    addRating(res, userId)
    addQuestsInfo(res, userId)
    return jsonResponse(res)


@app.route("", methods=["POST"])
def userCreate():
    try:
        req = request.json
        username = req['username']
        name = req['name']
        password = req['password']
        avatarUrl = req.get('avatarUrl')
        email = req.get('email')
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    password = hash_sha256(password)

    try:
        resp = DB.execute(sql.insertUser, [username, password, avatarUrl, email, name])
    except:
        return jsonResponse("Имя пользователя или email заняты", HTTP_DATA_CONFLICT)

    return new_session(resp)


@app.route("", methods=["PUT"])
@login_required
def userUpdate(userData):
    try:
        req = request.json
        username = req.get('username')
        name = req.get('name')
        email = req.get('email')
        avatarUrl = req.get('avatarUrl')
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    if name is None: name = userData['name']
    if username is None: username = userData['username']
    if email is None: email = userData['email']
    if avatarUrl is None: avatarUrl = userData['avatarurl']

    try:
        resp = DB.execute(sql.updateUserById, [username, name, email, avatarUrl, userData['id']])
    except:
        return jsonResponse("Имя пользователя или email заняты", HTTP_DATA_CONFLICT)

    return jsonResponse(resp)


@app.route("", methods=["DELETE"])
@login_required_return_id
def userDelete(userId):
    DB.execute(sql.deleteUserById, [userId])
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

    oldPassword = hash_sha256(oldPassword)
    newPassword = hash_sha256(newPassword)

    # if (userData['name'] != username) and (not userData['isadmin']):
    #     return jsonResponse("Нет прав", HTTP_NO_PERMISSIONS)

    resp = DB.execute(sql.updateUserPasswordByIdPassword, [newPassword, userId, oldPassword])
    if len(resp) == 0:
        return jsonResponse("Старый пароль не такой", HTTP_INVALID_AUTH_DATA)

    return jsonResponse("Успешно обновлено")


@app.route("/password/restore", methods=["POST"])
def userRestorePasswordSendEmail():
    try:
        req = request.json
        email = req['email']
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    userData = DB.execute(sql.selectUserByEmail, [email])
    if not userData:
        return jsonResponse("На этот email не зарегистрирован ни один аккаунт", HTTP_NOT_FOUND)

    secretCode = new_secret_code(userData['id'], "password")

    with current_app.app_context():
        mail = Mail()
        msg = Message("Восстановление пароля на SQuest", recipients=[email])
        msg.html = f"""<p>Для восстановления пароля, пожалуйста, перейдите по ссылке ниже: <br>
                   <a href="https://sergtyapkin.herokuapp.com/squest/password/restore?code={secretCode}">Восстановить пароль</a> <br>
                   <br>
                   <hr>
                   <small>Если вы не хотели восстанавливать пароль от своего аккаунта, проигнорируйте это письмо</small></p>"""
        mail.send(msg)

    return jsonResponse("Код выслан на почту " + email)


@app.route("/password/restore", methods=["PUT"])
def userRestorePasswordChangePassword():
    try:
        req = request.json
        newPassword = req['newPassword']
        code = req['code']
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    newPassword = hash_sha256(newPassword)

    userData = DB.execute(sql.updateUserPasswordBySecretcode, [newPassword, code])
    if not userData:
        return jsonResponse("Код восстановления не найден", HTTP_NOT_FOUND)

    DB.execute(sql.deleteSecretCodeByUseridCode, [userData['id'], code])
    return jsonResponse("Пароль изменен")
