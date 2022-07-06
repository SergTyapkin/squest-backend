from flask import Blueprint

from utils.access import *
from constants import *
from utils.questUtils import checkQuestAuthor
from utils.utils import *

app = Blueprint('quests', __name__)

_DB = Database(read_config("config.json"))


@app.route("")
@login_or_none_return_id
def questsGet(userId_logined):
    try:
        req = request.args
        userId = req.get('userId')
        questId = req.get('questId')
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    # Нужно выдать квест по id
    if questId is not None:
        res, questData = checkQuestAuthor(questId, userId_logined, _DB, allowHelpers=True)
        return questData
    # Нужно выдать все квесты юзера
    elif userId is not None:
        if str(userId_logined) == userId:
            resp = _DB.execute(sql.selectQuestsByAuthorx2, [userId_logined] * 2, manyResults=True)  # просмотр всех своих квестов
        else:
            resp = _DB.execute(sql.selectPublishedQuestsByAuthor, [userId], manyResults=True)  # просмотр квестов определенного автора
    # Нужно выдать вообще все квесты
    else:
        resp = _DB.execute(sql.selectAvailableQuestsByUseridx5, [userId_logined] * 5, manyResults=True)  # просмотр всех опубликованных квестов

    return jsonResponse(resp)


@app.route("", methods=["POST"])
@login_required_return_id
def questCreate(userId):
    try:
        req = request.json
        title = req['title']
        description = req['description']
        isPublished = req['isPublished']
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    resp = _DB.execute(sql.insertQuest, [title, description, userId, isPublished])

    return jsonResponse(resp)


@app.route("", methods=["PUT"])
@login_required_return_id
def questUpdate(userId):
    try:
        req = request.json
        questId = req['id']
        title = req.get('title')
        description = req.get('description')
        isPublished = req.get('isPublished')
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    res, questData = checkQuestAuthor(questId, userId, _DB, allowHelpers=True)
    if not res: return questData

    title = title or questData['title']
    description = description or questData['description']
    if isPublished is None: isPublished = questData['ispublished']

    resp = _DB.execute(sql.updateQuestById, [title, description, isPublished, questId])
    return jsonResponse(resp)


@app.route("", methods=["DELETE"])
@login_required_return_id
def questDelete(userId):
    try:
        req = request.json
        questId = req['id']
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    res, questData = checkQuestAuthor(questId, userId, _DB)
    if not res: return questData

    _DB.execute(sql.deleteQuestById, [questId])
    return jsonResponse("Квест удален")


@app.route("/choose", methods=["POST"])
@login_required_return_id
def questChoose(userId):
    try:
        req = request.json
        questId = req['questId']
        branchId = req['branchId']
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    resp = _DB.execute(sql.updateUserChooseBranchByUserId, [questId, branchId, userId])
    return jsonResponse(resp)


@app.route("/privacy")
@login_required_return_id
def privacyGet(userId):
    try:
        req = request.args
        questId = req['questId']
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    res, questData = checkQuestAuthor(questId, userId, _DB, allowHelpers=True)
    if not res: return questData

    resp = _DB.execute(sql.selectPrivacyUserNamesByQuestId, [questId], manyResults=True)
    return jsonResponse(resp)


@app.route("/privacy", methods=["POST"])
@login_required_return_id
def privacyCreate(userId_logined):
    try:
        req = request.json
        questId = req['questId']
        userId = req.get('userId')
        userName = req.get('name')
        isInBlackList = req['isInBlackList']
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    if userId is None:
        if userName is None:
            return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)
        resp = _DB.execute(sql.selectUserByName, [userName])
        if not resp:
            return jsonResponse("Пользователя не существует", HTTP_NOT_FOUND)
        userId = resp['id']

    res, questData = checkQuestAuthor(questId, userId_logined, _DB, allowHelpers=True)
    if not res: return questData

    try:
        resp = _DB.execute(sql.insertPrivacy, [userId, questId, isInBlackList])
    except:
        return jsonResponse("Пользователя не существует или уже настроен", HTTP_DATA_CONFLICT)
    return jsonResponse(resp)


@app.route("/privacy", methods=["PUT"])
@login_required_return_id
def privacyUpdate(userId_logined):
    try:
        req = request.json
        id = req['id']
        questId = req['questId']
        userId = req.get('userId')
        userName = req.get('name')
        isInBlackList = req.get('isInBlackList')
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    if userId is None:
        if userName is None:
            return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)
        resp = _DB.execute(sql.selectUserByName, [userName])
        if not resp:
            return jsonResponse("Пользователя не существует", HTTP_NOT_FOUND)
        userId = resp['id']

    res, questData = checkQuestAuthor(questId, userId_logined, _DB, allowHelpers=True)
    if not res: return questData

    try:
        resp = _DB.execute(sql.updatePrivacyByIdQuestid, [userId, isInBlackList, id, questId])
    except:
        return jsonResponse("Пользователя не существует или уже настроен", HTTP_DATA_CONFLICT)
    return jsonResponse(resp)


@app.route("/privacy", methods=["DELETE"])
@login_required_return_id
def privacyDelete(userId_logined):
    try:
        req = request.json
        id = req['id']

        # isAll = req.get('all')
        # questId = req.get('questId')
        # userId = req.get('userId')
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    resp = _DB.execute(sql.selectPrivacyById, [id])
    questId = resp['questid']

    res, questData = checkQuestAuthor(questId, userId_logined, _DB, allowHelpers=True)
    if not res: return questData

    # if isAll == 'true':
    #     _DB.execute(sql.deletePrivacyByQuestid, [questId])
    # else:
    _DB.execute(sql.deletePrivacyById, [id])

    return jsonResponse("Запись доступа удалена")


@app.route("/helpers")
@login_required_return_id
def helperGet(userId):
    try:
        req = request.args
        questId = req['questId']
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    res, questData = checkQuestAuthor(questId, userId, _DB)
    if not res: return questData

    resp = _DB.execute(sql.selectHelpersUserNamesByQuestId, [questId], manyResults=True)
    return jsonResponse(resp)


@app.route("/helpers", methods=["POST"])
@login_required_return_id
def helperCreate(userId_logined):
    try:
        req = request.json
        questId = req['questId']
        userId = req.get('userId')
        userName = req.get('name')
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    if userId is None:
        if userName is None:
            return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)
        resp = _DB.execute(sql.selectUserByName, [userName])
        if not resp:
            return jsonResponse("Пользователя не существует", HTTP_NOT_FOUND)
        userId = resp['id']

    res, questData = checkQuestAuthor(questId, userId_logined, _DB)
    if not res: return questData

    try:
        resp = _DB.execute(sql.insertHelper, [userId, questId])
    except:
        return jsonResponse("Пользователя не существует или уже настроен", HTTP_DATA_CONFLICT)
    return jsonResponse(resp)


@app.route("/helpers", methods=["PUT"])
@login_required_return_id
def helperUpdate(userId_logined):
    try:
        req = request.json
        id = req['id']
        questId = req['questId']
        userId = req.get('userId')
        userName = req.get('name')
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    if userId is None:
        if userName is None:
            return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)
        resp = _DB.execute(sql.selectUserByName, [userName])
        if not resp:
            return jsonResponse("Пользователя не существует", HTTP_NOT_FOUND)
        userId = resp['id']

    res, questData = checkQuestAuthor(questId, userId_logined, _DB)
    if not res: return questData

    try:
        resp = _DB.execute(sql.updateHelperByIdQuestid, [userId, id, questId])
    except:
        return jsonResponse("Пользователя не существует или уже настроен", HTTP_DATA_CONFLICT)
    return jsonResponse(resp)


@app.route("/helpers", methods=["DELETE"])
@login_required_return_id
def helperDelete(userId_logined):
    try:
        req = request.json
        id = req['id']
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    resp = _DB.execute(sql.selectHelperById, [id])
    questId = resp['questid']

    res, questData = checkQuestAuthor(questId, userId_logined, _DB)
    if not res: return questData

    _DB.execute(sql.deleteHelperById, [id])
    return jsonResponse("Запись доступа удалена")
