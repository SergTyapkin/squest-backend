from flask import Blueprint

from utils.access import *
from utils.questUtils import *
from utils.utils import *

app = Blueprint('tasks', __name__)

_DB = Database(read_config("config.json"))


@app.route("")
@login_or_none_return_id
def tasksGet(userId):
    try:
        req = request.json
        branchId = req['branchId']
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    branchData = _DB.execute(sql.selectQuestByBranchId, [branchId])

    # Можно смотреть таски только есть:
    # 1. Юзер залогинен и юзер - автор квеста ветки
    # 2. Таски только если ветка и квест опубликованы
    if (userId is not None and branchData['author'] == userId) or \
            (branchData['ispublished'] and branchData['qispublished']):
        resp = _DB.execute(sql.selectTasksByBranchid, [branchId])  # можно смотреть таски
        return jsonResponse(resp)

    jsonResponse("Нет прав просмотра заданий в этой ветке", HTTP_NO_PERMISSIONS)  # нельзя


@app.route("", methods=["POST"])
@login_required_return_id
def taskCreate(userId):
    try:
        req = request.json
        branchId = req['branchId']
        title = req['title']
        description = req['description']
        question = req['question']
        answers = req['answers']
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    res, branchData = checkBranchAuthor(branchId, userId, _DB)
    if not res: return branchData

    resp = _DB.execute(sql.insertTask, [branchId, title, description, question, answers])
    return jsonResponse(resp)


@app.route("", methods=["PUT"])
@login_required_return_id
def taskUpdate(userId):
    try:
        req = request.json
        taskId = req['id']
        title = req.get('title')
        description = req.get('description')
        question = req.get('question')
        answers = req.get('answers')
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    res, taskData = checkTaskAuthor(taskId, userId, _DB)
    if not res: return taskData

    title = title or taskData['title']
    description = description or taskData['description']
    question = question or taskData['question']
    answers = answers or taskData['answers']

    _DB.execute(sql.updateTaskById, [title, description, question, answers, taskId])
    return jsonResponse("Задание обновлено")


@app.route("", methods=["DELETE"])
@login_required_return_id
def taskDelete(userId):
    try:
        req = request.json
        taskId = req['id']
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    res, taskData = checkTaskAuthor(taskId, userId, _DB)
    if not res: return taskData

    _DB.execute(sql.deleteTaskById, [taskId])
    return jsonResponse("Задание удалено")
