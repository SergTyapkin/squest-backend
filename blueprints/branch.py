from flask import Blueprint

from utils.access import *
from utils.questUtils import *
from utils.utils import *

app = Blueprint('branches', __name__)

_DB = Database(read_config("config.json"))


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
        branchData = _DB.execute(sql.selectQuestByBranchId, [branchId])
        isAuthor = checkBranchAuthor(branchId, userId, _DB, allowHelpers=True)[0]
        # Если юзер залогинен и юзер - автор квеста ветки
        if branchData['ispublished'] or isAuthor:
            # Добавим прогресс пользователя
            resp = _DB.execute(sql.selectProgressByUseridBranchid, [userId, branchId])
            branchData['progress'] = resp.get('maxprogress') or 0
            # Добавим длину ветки
            resp = _DB.execute(sql.selectBranchLengthById, [branchId])
            branchData['length'] = max(resp['length'] - 1, 0)
            return jsonResponse(branchData)
        else:
            return jsonResponse("Ветка не опубликована, а вы не автор", HTTP_NO_PERMISSIONS)
    # Нужно выдать все ветки квеста
    elif questId is not None:
        if userId is not None and checkQuestAuthor(questId, userId, _DB, allowHelpers=True)[0]:  # Если юзер залогинен и юзер - автор квеста
            resp = _DB.execute(sql.selectBranchesByQuestid, [questId], manyResults=True)  # можно смотреть все ветки квеста
        else:
            resp = _DB.execute(sql.selectPublishedBranchesByQuestid, [questId], manyResults=True)  # иначе - только опубликованные
        return jsonResponse(resp)
    # Не пришло ни одного id
    return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)


@app.route("", methods=["POST"])
@login_required_return_id
def branchCreate(userId):
    try:
        req = request.json
        questId = req['questId']
        title = req['title']
        description = req['description']
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    res, questData = checkQuestAuthor(questId, userId, _DB, allowHelpers=True)
    if not res: return questData

    resp = _DB.execute(sql.selectBranchMaxOrderidByQuestid, [questId])
    maxOrderId = resp['maxorderid'] or 0

    resp = _DB.execute(sql.insertBranch, [questId, title, description, maxOrderId + 1])
    return jsonResponse(resp)


@app.route("/many", methods=["POST"])
@login_required_return_id
def branchCreateMany(userId):
    try:
        req = request.json
        questId = req['questId']
        branches = req['branches']
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    res, questData = checkQuestAuthor(questId, userId, _DB, allowHelpers=True)
    if not res: return questData

    resp = _DB.execute(sql.selectBranchMaxOrderidByQuestid, [questId])
    maxOrderId = resp['maxorderid'] or 0

    resp = []
    for branch in branches:
        maxOrderId += 1
        resp += [_DB.execute(sql.insertBranch, [questId, branch['title'], branch['description'], maxOrderId])]
    return jsonResponse(resp)


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

    res, branchData = checkBranchAuthor(branchId, userId, _DB, allowHelpers=True)
    if not res: return branchData

    title = title or branchData['title']
    description = description or branchData['description']
    if isPublished is None: isPublished = branchData['ispublished']
    orderId = orderId or branchData['orderid']

    resp = _DB.execute(sql.updateBranchById, [orderId, title, description, isPublished, branchId])
    return jsonResponse(resp)


@app.route("", methods=["DELETE"])
@login_required_return_id
def branchDelete(userId):
    try:
        req = request.json
        branchId = req['id']
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    res, branchData = checkBranchAuthor(branchId, userId, _DB, allowHelpers=True)
    if not res: return branchData

    _DB.execute(sql.deleteBranchById, [branchId])

    # Make orderids actual
    questId = branchData['questid']
    resp = _DB.execute(sql.selectBranchesByQuestid, [questId], manyResults=True)  # получаем все ветки
    idx = 1
    for branch in resp:
        if branch['orderid'] != idx:
            resp[idx-1] = _DB.execute(sql.updateBranchOrderidById, [idx, branch['id']])
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

    resp = _DB.execute(sql.updateProgressByUseridBranchid, [0, userId, branchId])
    return jsonResponse(resp)

