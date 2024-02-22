import datetime
import uuid

from flask import Blueprint

from connections import DB
from utils.access import *
from constants import *
from utils.questUtils import checkQuestAuthor
from utils.utils import *

app = Blueprint('quests', __name__)


@app.route("")
@login_or_none_return_id
def questsGet(userId_logined):
    try:
        req = request.args
        userId = req.get('userId')
        questId = req.get('questId')
        questUid = req.get('questUid')
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    # Нужно выдать квест по id
    if questId is not None:
        res, questData = checkQuestAuthor(questId, userId_logined, DB, allowHelpers=True)
        if res:
            return questData

        questData = DB.execute(sql.selectPublishedQuestById, [questId])
        if not questData:
            return jsonResponse('Квеста не существует или нет прав доступа', HTTP_NOT_FOUND)

        return jsonResponse(questData)
    # Нужно выдать квест по uid
    elif questUid is not None:
        questData = DB.execute(sql.selectQuestByUid, [questUid])
        if not questData:
            return jsonResponse('Квеста не существует или нет прав доступа', HTTP_NO_PERMISSIONS)

        return jsonResponse(questData)
    # Нужно выдать все квесты юзера
    elif userId is not None:
        if str(userId_logined) == userId:
            resp = DB.execute(sql.selectEditableQuestsByUseridx2, [userId_logined] * 2, manyResults=True)  # просмотр всех своих квестов
        else:
            resp = DB.execute(sql.selectPublishedQuestsByAuthorUserid, [userId, userId_logined], manyResults=True)  # просмотр квестов определенного автора
    # Нужно выдать вообще все квесты
    elif userId_logined is not None:
        allQuests = DB.execute(sql.selectPublishedQuests, manyResults=True)  # берем все опубликованные
        myQuests = DB.execute(sql.selectEditableQuestsByUseridx2, [userId_logined] * 2, manyResults=True)  # берем все, доступные для редактирования
        myQuestsIds = list(map(lambda quest: quest['id'], myQuests))
        for quest in allQuests:  # т.к. они могут пересекаться, добавляем к доступым для редактирования, остальные неопубликованные
            if quest['id'] not in myQuestsIds:
                quest['canedit'] = False  # следим за полями canedit. Всё что мы делаем ради них и нужно
                myQuests.append(quest)
        resp = myQuests
    else:
        resp = DB.execute(sql.selectPublishedQuests, manyResults=True)  # просмотр всех опубликованных квестов для незалогиненного пользователя

    return jsonResponse({'quests': resp})


@app.route("/uid")
@login_required_return_id
def questsUidGet(userId):
    try:
        req = request.args
        questId = req.get('id')
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    res, questData = checkQuestAuthor(questId, userId, DB, allowHelpers=True)
    if not res:
        return questData
    resp = DB.execute(sql.selectQuestUidById, [questData['id']])
    if not resp:
        return jsonResponse("Квеста не существует или нет прав доступа", HTTP_NO_PERMISSIONS)
    return jsonResponse(resp)


@app.route("", methods=["POST"])
@login_and_email_confirmation_required
def questCreate(userData):
    try:
        req = request.json
        title = req['title']
        description = req['description']
        isPublished = req['isPublished']
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    uid = str(uuid.uuid4())
    resp = DB.execute(sql.insertQuest, [uid, title, description, userData['id'], isPublished])
    defaultBranch = DB.execute(sql.insertBranch, [resp['id'], DEFAULT_BRANCH_NAME, None, 1, True])
    if not defaultBranch:
        print("Не удалось создать дефолтную ветку квеста!")
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
        isLinkActive = req.get('isLinkActive')
        previewUrl = req.get('previewUrl')
        backgroundImageUrl = req.get('backgroundImageUrl')
        customCSS = req.get('customCSS')
        bottomLink = req.get('bottomLink')
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    res, questData = checkQuestAuthor(questId, userId, DB, allowHelpers=True)
    if not res: return questData

    if title is None: title = questData['title']
    if isPublished is None: description = questData['description']
    if isPublished is None: isPublished = questData['ispublished']
    if isLinkActive is None: isLinkActive = questData['islinkactive']
    if previewUrl is None: previewUrl = questData['previewurl']
    if backgroundImageUrl is None: backgroundImageUrl = questData['backgroundimageurl']
    if customCSS is None: customCSS = questData['customcss']
    if 'bottomLink' not in req: bottomLink = questData['bottomlink']

    resp = DB.execute(sql.updateQuestById, [title, description, isPublished, isLinkActive, previewUrl, backgroundImageUrl, customCSS, bottomLink, questId])
    return jsonResponse(resp)


@app.route("", methods=["DELETE"])
@login_required_return_id
def questDelete(userId):
    try:
        req = request.json
        questId = req['id']
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    res, questData = checkQuestAuthor(questId, userId, DB)
    if not res: return questData

    DB.execute(sql.deleteQuestById, [questId])
    return jsonResponse("Квест удален")


@app.route("/choose", methods=["POST"])
@login_required_return_id
def questChoose(userId):
    try:
        req = request.json
        questId = req['questId']
        branchId = req['branchId']
        mode = req.get('mode') or 0
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    resp = DB.execute(sql.updateUserChooseBranchByUserId, [questId, branchId, mode, userId])
    return jsonResponse(resp)


@app.route("/helpers")
@login_required_return_id
def helperGet(userId):
    try:
        req = request.args
        questId = req['questId']
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    res, questData = checkQuestAuthor(questId, userId, DB)
    if not res: return questData

    resp = DB.execute(sql.selectHelpersUserNamesByQuestId, [questId], manyResults=True)
    return jsonResponse({'helpers': resp})


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
        resp = DB.execute(sql.selectUserByUsername, [userName])
        if not resp:
            return jsonResponse("Пользователя не существует", HTTP_NOT_FOUND)
        userId = resp['id']

    res, questData = checkQuestAuthor(questId, userId_logined, DB)
    if not res: return questData

    try:
        resp = DB.execute(sql.insertHelper, [userId, questId])
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
        resp = DB.execute(sql.selectUserByUsername, [userName])
        if not resp:
            return jsonResponse("Пользователя не существует", HTTP_NOT_FOUND)
        userId = resp['id']

    res, questData = checkQuestAuthor(questId, userId_logined, DB)
    if not res: return questData

    try:
        resp = DB.execute(sql.updateHelperByIdQuestid, [userId, id, questId])
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

    resp = DB.execute(sql.selectHelperById, [id])
    questId = resp['questid']

    res, questData = checkQuestAuthor(questId, userId_logined, DB)
    if not res: return questData

    DB.execute(sql.deleteHelperById, [id])
    return jsonResponse("Запись доступа удалена")


# ---- statistics ---
@app.route("/users/finished")
def getFinishedUsers():
    try:
        req = request.args
        questId = req['questId']
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    resp = DB.execute(sql.selectFinishedQuestPLayersByQuestid, [questId], manyResults=True)
    for user in resp:
        user['time'] = user['time'].total_seconds()
    return jsonResponse({"players": resp})


@app.route("/users/progresses")
def getUsersProgresses():
    try:
        req = request.args
        questId = req['questId']
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    resp = DB.execute(sql.selectPLayersProgressesByQuestid, [questId], manyResults=True)
    for user in resp:
        user['time'] = user['time'].total_seconds()
    return jsonResponse({"players": resp})


@app.route("/progress/stats")
@login_required_return_id
def getUserProgressStats(userId):
    try:
        req = request.args
        branchId = req['branchId']
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    resp = DB.execute(sql.selectProgressStatsByUseridBranchid, [userId, branchId])
    resp['time'] = resp['time'].total_seconds()
    return jsonResponse(resp)


@app.route("/rating", methods=['POST'])
@login_and_email_confirmation_required
def branchRatingVote(userData):
    try:
        req = request.json
        branchId = req['branchId']
        rating = int(req['rating'])
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    if rating < 1 or rating > 5:
        return jsonResponse("rating может быть только от 0 до 5", HTTP_INVALID_DATA)

    resp = DB.execute(sql.updateProgressRatingByBranchidUserid, [rating, branchId, userData['id']], manyResults=True)
    if not resp:
        return jsonResponse("Нет прав на голосование за рейтинг квеста", HTTP_NO_PERMISSIONS)
    return jsonResponse(resp)


@app.route("/stats")
def getQuestStatistics():
    try:
        req = request.args
        questId = req['questId']
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    resp = DB.execute(sql.selectQuestStatisticsByQuestid, [questId])
    if not resp:
        return jsonResponse("Квест не найден или в него пока никто не играл", HTTP_NOT_FOUND)

    if resp['time']:
        resp['time'] = resp['time'].total_seconds()
    return jsonResponse(resp)
