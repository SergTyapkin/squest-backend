from flask import Blueprint

from utils.access import *
from utils.questUtils import *
from utils.utils import *


app = Blueprint('tasks', __name__)

_DB = Database(read_config("config.json"))


@app.route("")
@login_required_return_id
def tasksGet(userId):
    try:
        req = request.args
        taskId = req.get('taskId')
        branchId = req.get('branchId')
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    # Нужно выдать таск по id
    if taskId is not None:
        isAuthor, taskData = checkTaskAuthor(taskId, userId, _DB)
        if not isAuthor: return taskData

        return jsonResponse(taskData)
    # Нужно выдать все таски ветки
    elif branchId is not None:
        # Можно смотреть только если юзер залогинен и юзер - автор ветки
        if userId is None or not checkBranchAuthor(branchId, userId, _DB)[0]:
            return jsonResponse("Вы не являетесь автором ветки", HTTP_NO_PERMISSIONS)
        resp = _DB.execute(sql.selectTasksByBranchid, [branchId], manyResults=True)  # можно смотреть все ветки квеста
        return jsonResponse(resp)
    # Не пришло ни одного id
    return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)


def getOrCreateUserProgress(userData):
    resp = _DB.execute(sql.selectProgressByUseridBranchid, [userData['id'], userData['chosenbranchid']])
    try:
        progress = resp['progress']
    except KeyError:  # прогресса нет - надо создать нулевой прогресс
        resp = _DB.execute(sql.insertProgress, [userData['id'], userData['chosenbranchid']])
        progress = resp['progress']
    return progress


@app.route("/play")
@login_required
def tasksGetLast(userData):
    if userData['chosenbranchid'] is None or userData['chosenquestid'] is None:
        return jsonResponse("Квест или ветка не выбраны", HTTP_INVALID_DATA)

    questResp = _DB.execute(sql.selectQuestById, [userData['chosenquestid']])
    branchResp = _DB.execute(sql.selectBranchLengthById, [userData['chosenbranchid']])
    # Можно получить только последний таск в выбранной ветке и квесте только если
    # ветка и квест опубликованы или юзер - автор
    if questResp['author'] != userData['id'] and (not questResp['ispublished'] or not branchResp['ispublished']):
        return jsonResponse("Выбранный квест или ветка не опубликованы, а вы не автор", HTTP_NO_PERMISSIONS)

    progress = getOrCreateUserProgress(userData)

    resp = _DB.execute(sql.selectTaskByBranchidNumber, [userData['chosenbranchid'], progress])
    # Добавим к ответу названия квеста и ветки
    resp['questtitle'] = questResp['title']
    resp['branchtitle'] = branchResp['title']
    # Добавим к ответу прогресс и общую длину ветки
    resp['progress'] = progress
    if branchResp['length'] == 0:
        return jsonResponse("В ветке нет заданий", 400)
    resp['length'] = max(branchResp['length'] - 1, 0)

    # Определим кол-во заданий, и уберем поле question, если задание - последнее
    maxOrderid = _DB.execute(sql.selectTaskMaxOrderidByBranchid, [userData['chosenbranchid']])
    if maxOrderid['maxorderid'] == resp['orderid']:
        del resp['question']

    return jsonResponse(resp)


@app.route("/play", methods=["POST"])
@login_required
def tasksCheckAnswer(userData):
    try:
        req = request.json
        userAnswer = req['answer'].lower()
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    progress = getOrCreateUserProgress(userData)

    task = _DB.execute(sql.selectTaskAnswersByBranchidNumber, [userData['chosenbranchid'], progress])
    for answer in task['answers']:
        if answer == userAnswer or answer == '*':  # если настроен ответ '*' - принимается любой ответ
            resp = _DB.execute(sql.increaseProgressByUseridBranchid, [userData['id'], userData['chosenbranchid']])
            return jsonResponse(resp)

    return jsonResponse("Ответ неверен", HTTP_ANSWER_MISS)


@app.route("", methods=["POST"])
@login_required_return_id
def taskCreate(userId):
    try:
        req = request.json
        branchId = req['branchId']
        title = req['title']
        description = req['description']
        question = req['question']
        answers = list(map(str.lower, req['answers']))
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    res, branchData = checkBranchAuthor(branchId, userId, _DB)
    if not res: return branchData

    resp = _DB.execute(sql.selectTaskMaxOrderidByBranchid, [branchId])
    maxOrderId = resp['maxorderid'] or 0

    resp = _DB.execute(sql.insertTask, [branchId, title, description, question, answers, maxOrderId + 1])
    return jsonResponse(resp)


@app.route("/many", methods=["POST"])
@login_required_return_id
def taskCreateMany(userId):
    try:
        req = request.json
        branchId = req['branchId']
        tasks = req['tasks']
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    res, branchData = checkBranchAuthor(branchId, userId, _DB)
    if not res: return branchData

    resp = _DB.execute(sql.selectTaskMaxOrderidByBranchid, [branchId])
    maxOrderId = resp['maxorderid'] or 0

    resp = []
    for task in tasks:
        maxOrderId += 1
        resp += [_DB.execute(sql.insertTask, [branchId, task['title'], task['description'], task['question'], task['answers'], maxOrderId])]
    return jsonResponse(resp)


@app.route("", methods=["PUT"])
@login_required_return_id
def taskUpdate(userId):
    try:
        req = request.json
        taskId = req['id']
        orderId = req.get('orderId')
        title = req.get('title')
        description = req.get('description')
        question = req.get('question')
        answers = req.get('answers')
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    res, taskData = checkTaskAuthor(taskId, userId, _DB)
    if not res: return taskData

    title = title or taskData['title']
    question = question or taskData['question']
    if answers is not None:
        answers = list(map(str.lower, answers))
    else:
        answers = taskData['answers']
    description = description or taskData['description']
    orderId = orderId or taskData['orderid']

    resp = _DB.execute(sql.updateTaskById, [orderId, title, description, question, answers, taskId])
    return jsonResponse(resp)


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

    # Make orderids actual
    branchId = taskData['branchid']
    resp = _DB.execute(sql.selectTasksByBranchid, [branchId], manyResults=True)  # получаем все ветки
    idx = 1
    for task in resp:
        if task['orderid'] != idx:
            resp[idx-1] = _DB.execute(sql.updateTaskOrderidById, [idx, task['id']])
        idx += 1
    return jsonResponse(resp)
