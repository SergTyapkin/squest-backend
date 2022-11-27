from flask import Blueprint

from connections import DB
from utils.access import *
from utils.questUtils import *
from utils.utils import *

app = Blueprint('branches', __name__)


@app.route("")
@login_or_none_return_id
def branchesGet(userId):
    try:
        req = request.args
        questId = req.get('questId')
        branchId = req.get('branchId')
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    # Нужно выдать ветку по id
    if branchId is not None:
        branchData = DB.execute(sql.selectQuestByBranchId, [branchId])
        isAuthor = checkBranchAuthor(branchId, userId, DB, allowHelpers=True)[0]
        # Если юзер залогинен и юзер - автор квеста ветки
        if branchData and (branchData['ispublished'] or isAuthor):
            # Добавим прогресс пользователя
            resp = DB.execute(sql.selectProgressByUseridBranchid, [userId, branchId])
            branchData['progress'] = resp.get('maxprogress') or 0
            # Добавим длину ветки
            resp = DB.execute(sql.selectBranchLengthById, [branchId])
            branchData['length'] = max(resp['length'] - 1, 0)
            return jsonResponse(branchData)
        else:
            return jsonResponse("Ветка не опубликована, а вы не автор", HTTP_NO_PERMISSIONS)
    # Нужно выдать все ветки квеста
    elif questId is not None:
        if userId is not None and checkQuestAuthor(questId, userId, DB, allowHelpers=True)[0]:  # Если юзер залогинен и юзер - автор квеста
            resp = DB.execute(sql.selectBranchesByQuestid, [questId], manyResults=True)  # можно смотреть все ветки квеста
        else:
            resp = DB.execute(sql.selectPublishedBranchesByQuestid, [questId], manyResults=True)  # иначе - только опубликованные
        return jsonResponse({'branches': resp})
    # Не пришло ни одного id
    return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)


@app.route("", methods=["POST"])
@login_and_email_confirmation_required
def branchCreate(userData):
    try:
        req = request.json
        questId = req['questId']
        title = req['title']
        description = req['description']
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    res, questData = checkQuestAuthor(questId, userData['id'], DB, allowHelpers=True)
    if not res: return questData

    resp = DB.execute(sql.selectBranchMaxOrderidByQuestid, [questId])
    maxOrderId = resp['maxorderid'] or 0

    resp = DB.execute(sql.insertBranch, [questId, title, description, maxOrderId + 1])
    return jsonResponse(resp)


@app.route("/many", methods=["POST"])
@login_and_email_confirmation_required
def branchCreateMany(userData):
    try:
        req = request.json
        questId = req['questId']
        branches = req['branches']
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    res, questData = checkQuestAuthor(questId, userData['id'], DB, allowHelpers=True)
    if not res: return questData

    resp = DB.execute(sql.selectBranchMaxOrderidByQuestid, [questId])
    maxOrderId = resp['maxorderid'] or 0

    resp = []
    for branch in branches:
        maxOrderId += 1
        resp += [DB.execute(sql.insertBranch, [questId, branch['title'], branch['description'], maxOrderId])]
    return jsonResponse({'branches': resp})


@app.route("", methods=["PUT"])
@login_required_return_id
def branchUpdate(userId):
    try:
        req = request.json
        branchId = req['id']
        orderId = req.get('orderId')
        title = req.get('title')
        description = req.get('description')
        isPublished = req.get('isPublished')
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    res, branchData = checkBranchAuthor(branchId, userId, DB, allowHelpers=True)
    if not res: return branchData

    if title is None: title = branchData['title']
    if description is None: description = branchData['description']
    if isPublished is None: isPublished = branchData['ispublished']
    if orderId is None: orderId = branchData['orderid']

    resp = DB.execute(sql.updateBranchById, [orderId, title, description, isPublished, branchId])
    return jsonResponse(resp)


@app.route("", methods=["DELETE"])
@login_required_return_id
def branchDelete(userId):
    try:
        req = request.json
        branchId = req['id']
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    res, branchData = checkBranchAuthor(branchId, userId, DB, allowHelpers=True)
    if not res: return branchData

    DB.execute(sql.deleteBranchById, [branchId])

    # Make orderids actual
    questId = branchData['questid']
    resp = DB.execute(sql.selectBranchesByQuestid, [questId], manyResults=True)  # получаем все ветки
    idx = 1
    for branch in resp:
        if branch['orderid'] != idx:
            resp[idx-1] = DB.execute(sql.updateBranchOrderidById, [idx, branch['id']])
        idx += 1

    return jsonResponse(resp)


@app.route("/progress/reset", methods=["PUT"])
@login_required_return_id
def progressReset(userId):
    try:
        req = request.json
        branchId = req['branchId']
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    resp = DB.execute(sql.updateProgressByUseridBranchid, [0, userId, branchId])
    return jsonResponse(resp)


# Можно переключиться на следующее или предыдущее задание квеста,
# только если ты автор или соавтор квеста
@app.route("/progress/set", methods=["PUT"])
@login_required
def setProgress(userData):
    try:
        req = request.json
        branchId = req['branchId']
        targetProgress = req['progress']
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    # проверяем права доступа
    res, branchData = checkBranchAuthor(branchId, userData['id'], DB, allowHelpers=True)
    if not res: return branchData

    # получаем длину ветки
    branchInfo = DB.execute(sql.selectBranchLengthById, [branchId])

    if (targetProgress < 0) or (targetProgress >= branchInfo['length']):
        return jsonResponse("Указанное смещение выходит за пределы количества заданий ветки", HTTP_INVALID_DATA)

    DB.execute(sql.updateProgressByUseridBranchid, [targetProgress, userData['id'], branchId])
    return jsonResponse(f"Прогресс в ветке изменён на {targetProgress}")
