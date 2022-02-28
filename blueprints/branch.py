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
        questId = req['questId']
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    # Если юзер залогинен и юзер - автор квеста
    if userId is not None and checkQuestAuthor(questId, userId, _DB)[0]:
        resp = _DB.execute(sql.selectBranchesByQuestid, [questId], manyResults=True)  # можно смотреть все ветки квеста
    else:
        resp = _DB.execute(sql.selectPublishedBranchesByQuestid, [questId], manyResults=True)  # иначе - только опубликованные

    return jsonResponse(resp)


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

    res, questData = checkQuestAuthor(questId, userId, _DB)
    if not res: return questData

    resp = _DB.execute(sql.insertBranch, [questId, title, description])
    return jsonResponse(resp)


@app.route("", methods=["PUT"])
@login_required_return_id
def branchUpdate(userId):
    try:
        req = request.json
        branchId = req['id']
        title = req.get('username')
        description = req.get('description')
        isPublished = req.get('isPublished')
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    res, branchData = checkBranchAuthor(branchId, userId, _DB)
    if not res: return branchData

    title = title or branchData['title']
    description = description or branchData['description']
    isPublished = isPublished or branchData['ispublished']

    _DB.execute(sql.updateBranchById, [title, description, isPublished, branchId])
    return jsonResponse("Ветка обновлена")


@app.route("", methods=["DELETE"])
@login_required_return_id
def branchDelete(userId):
    try:
        req = request.json
        branchId = req['id']
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    res, branchData = checkBranchAuthor(branchId, userId, _DB)
    if not res: return branchData

    _DB.execute(sql.deleteBranchById, [branchId])
    return jsonResponse("Ветка удалена")
