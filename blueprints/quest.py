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
        req = request.json
        userId = req.get('userId')
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    if userId is not None:
        resp = _DB.execute(sql.selectPublishedQuestsByAuthor, [userId])  # просмотр квестов определенного автора
    else:
        if userId_logined is not None:
            resp = _DB.execute(sql.selectQuestsByAuthor, [userId_logined])  # просмотр всех своих квестов
        else:
            resp = _DB.execute(sql.selectPublishedQuests, [])  # просмотр всех опубликованных квестов

    return jsonResponse(resp)


@app.route("", methods=["POST"])
@login_required_return_id
def questCreate(userId):
    try:
        req = request.json
        title = req['title']
        description = req['description']
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    resp = _DB.execute(sql.insertQuest, [title, description, userId])
    return jsonResponse(resp)


@app.route("", methods=["PUT"])
@login_required_return_id
def questUpdate(userId):
    try:
        req = request.json
        questId = req['id']
        title = req.get('username')
        description = req.get('description')
        isPublished = req.get('isPublished')
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    res, questData = checkQuestAuthor(questId, userId, _DB)
    if not res: return questData

    title = title or questData['title']
    description = description or questData['description']
    isPublished = isPublished or questData['ispublished']

    _DB.execute(sql.updateQuestById, [title, description, isPublished, questId])
    return jsonResponse("Квест обновлен")


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


@app.route("/privacy")
@login_required_return_id
def privacyGet(userId):
    try:
        req = request.json
        questId = req['questId']
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    res, questData = checkQuestAuthor(questId, userId, _DB)
    if not res: return questData

    resp = _DB.execute(sql.selectPrivacyUsersIdByQuestId, [questId])
    return jsonResponse(resp)


@app.route("/privacy", methods=["POST"])
@login_required_return_id
def privacyCreate(userId_logined):
    try:
        req = request.json
        questId = req['questId']
        userId = req['userId']
        listType = req['listType']
        isBlackList = False
        if listType == "black":
            isBlackList = True
        elif listType != "white":
            raise(ValueError("Непредвиденное значение"))
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    res, questData = checkQuestAuthor(questId, userId_logined, _DB)
    if not res: return questData

    resp = _DB.execute(sql.insertQuestPrivacy, [userId, questId, isBlackList])
    return jsonResponse(resp)


@app.route("/privacy", methods=["PUT"])
@login_required_return_id
def privacyUpdate(userId_logined):
    try:
        req = request.json
        questId = req['questId']
        userId = req['userId']
        listType = req['listType']
        isBlackList = False
        if listType == "black":
            isBlackList = True
        elif listType != "white":
            raise(ValueError("Непредвиденное значение"))
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    res, questData = checkQuestAuthor(questId, userId_logined, _DB)
    if not res: return questData

    _DB.execute(sql.updatePrivacyIsInBlackListByQuestidUserid, [questId, userId, isBlackList])
    return jsonResponse("Записи доступа обновлены")


@app.route("/privacy", methods=["DELETE"])
@login_required_return_id
def privacyDelete(userId_logined):
    try:
        req = request.json
        questId = req['questId']
        userId = req['userId']
        isAll = req.get('all')
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    res, questData = checkQuestAuthor(questId, userId_logined, _DB)
    if not res: return questData

    if isAll == 'true':
        _DB.execute(sql.deletePrivacyByQuestid, [questId])
    else:
        _DB.execute(sql.deletePrivacyByQuestidUserid, [questId, userId])

    return jsonResponse("Записи доступа удалены")

