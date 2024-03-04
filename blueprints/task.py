from flask import Blueprint

from connections import DB
from utils.access import *
from utils.questUtils import *
from utils.utils import *


app = Blueprint('tasks', __name__)


@app.route("")
@login_required_return_id
def tasksGet(userId):
    try:
        req = request.args
        taskId = req.get('taskId')
        branchId = req.get('branchId')
        authorPlayMode = (req.get('authorPlayMode') == 'true')
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    # Нужно выдать таску по id
    if taskId is not None:
        isAuthor, taskData = checkTaskAuthor(taskId, userId, DB, allowHelpers=True)
        if not isAuthor: return taskData
        return jsonResponse(taskData)
    # Нужно выдать все таски ветки
    elif branchId is not None:
        # Можно смотреть только если юзер - автор ветки и он не играет в ветку
        if not authorPlayMode and checkBranchAuthor(branchId, userId, DB, allowHelpers=True)[0]:
            resp = DB.execute(sql.selectTasksByBranchid, [branchId], manyResults=True)  # можно смотреть все ветки квеста
            return jsonResponse({'tasks': resp})
        # Иначе можно смотреть только если юзер играет в эту ветку и в ней несортированые задания. Тогда надо выдать все ещё не пройденные задания
        resp = DB.execute(sql.selectBranchById, [branchId])
        if resp['istasksnotsorted'] is True:
            print(branchId, userId)
            resp = DB.execute(sql.selectUnfinishedTasksByBranchidUserid, [branchId, userId], manyResults=True)  # можно смотреть не пройденные таски ветки
            resp.pop()  # Удаляем последеднюю таску с поздравлением
            return jsonResponse({'tasks': resp})
        return jsonResponse("В выбранной ветке нельзя смотреть список всех заданий, и вы не автор квеста", HTTP_NO_PERMISSIONS)
    # Не пришло ни одного id
    return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)


def getOrCreateUserProgress(userData):
    resp = DB.execute(sql.selectProgressByUseridBranchid, [userData['id'], userData['chosenbranchid']])
    try:
        progress = resp['progress']
        completedTasks = resp['completedtasks']
    except KeyError:  # прогресса нет - надо создать нулевой прогресс
        resp = DB.execute(sql.insertProgress, [userData['id'], userData['chosenbranchid']])
        progress = resp['progress']
        completedTasks = resp['completedtasks']
    return [progress, completedTasks]


def getPlayTaskFormatted(questId, branchId, userData=None, selectFirstTask=False, noAuthorCheck=False):
    questResp = DB.execute(sql.selectQuestById, [questId])
    branchResp = DB.execute(sql.selectBranchLengthById, [branchId])
    isAuthor = True
    if not noAuthorCheck:
        isAuthor = checkQuestAuthor(questResp['id'], userData['id'], DB, allowHelpers=True)[0]
    # Можно получить только последний таск в выбранной ветке и квесте только если
    # ветка и квест опубликованы или доступны по ссылке или юзер - автор
    if (not isAuthor and selectFirstTask) or (not isAuthor and ((not questResp['ispublished'] and not questResp['islinkactive']) or not branchResp['ispublished'])):
        return jsonResponse("Выбранный квест или ветка не опубликованы, а вы не автор", HTTP_NO_PERMISSIONS)


    if selectFirstTask:
        resp = DB.execute(sql.selectFirstTaskByBranchid, [branchId])
        resp['orderid'] = 1
        resp['progress'] = 0.5
    else:
        [progress, _] = getOrCreateUserProgress(userData)
        resp = DB.execute(sql.selectTaskByBranchidNumber, [branchId, progress])
        resp['progress'] = progress
    # Добавим к ответу названия квеста и ветки, а так же настройки ветки
    resp['questtitle'] = questResp['title']
    resp['customcss'] = questResp['customcss']
    resp['bottomlink'] = questResp['bottomlink']
    resp['backgroundimageurl'] = questResp['backgroundimageurl']
    resp['branchtitle'] = branchResp['title']
    resp['istasksnotsorted'] = branchResp['istasksnotsorted']
    # Добавим к ответу прогресс и общую длину ветки
    if branchResp['length'] == 0:
        return jsonResponse("В ветке нет заданий", 400)
    resp['length'] = max(branchResp['length'] - 1, 0)
    # Добавим к ответу, является ли пользователь автором или соавтором квеста с этим заданием
    resp['canedit'] = isAuthor

    # Определим кол-во заданий, и уберем поле question, если задание - последнее
    maxOrderid = DB.execute(sql.selectTaskMaxOrderidByBranchid, [branchId])
    if maxOrderid['maxorderid'] == resp['orderid']:
        del resp['question']

    return jsonResponse(resp)


@app.route("/play")
@login_required
def tasksGetLast(userData):
    if userData['chosenbranchid'] is None or userData['chosenquestid'] is None:
        return jsonResponse("Квест или ветка не выбраны", HTTP_INVALID_DATA)
    return getPlayTaskFormatted(userData['chosenquestid'], userData['chosenbranchid'], userData)


@app.route("/play", methods=["POST"])
@login_required
def tasksCheckAnswer(userData):
    try:
        req = request.json
        userAnswer = req['answer'].lower()
        taskId = req.get('taskId')
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    [progress, completedTasks] = getOrCreateUserProgress(userData)
    if taskId is None:
        task = DB.execute(sql.selectTaskByBranchidCount, [userData['chosenbranchid'], progress])
    else:
        task = DB.execute(sql.selectTaskByBranchidTaskid, [userData['chosenbranchid'], taskId])

    for answer in task['answers']:
        if answer == userAnswer or answer == '*':  # если настроен ответ '*' - принимается любой ответ
            if task['id'] not in completedTasks:
                completedTasks.append(task['id'])
            resp = DB.execute(sql.increaseProgressByUseridBranchid, [completedTasks, userData['id'], userData['chosenbranchid']])
            return jsonResponse(resp)

    return jsonResponse("Ответ неверен", HTTP_ANSWER_MISS)


@app.route("/example", methods=["GET"])
@login_and_email_confirmation_required
def taskGetExample(userData):
    try:
        req = request.args
        questId = req['questId']
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    res, questData = checkQuestAuthor(questId, userData['id'], DB, allowHelpers=True)
    if not res: return questData

    branchData = DB.execute(sql.selectFirstBranchByQuestid, [questId])
    if branchData is None:
        return jsonResponse('У квеста нет ни одной ветки с заданиями', HTTP_NOT_FOUND)

    return getPlayTaskFormatted(questId, branchData['id'], userData, True, True)


@app.route("", methods=["POST"])
@login_and_email_confirmation_required
def taskCreate(userData):
    try:
        req = request.json
        branchId = req['branchId']
        title = req['title']
        description = req['description']
        question = req['question']
        answers = list(map(str.lower, req['answers']))
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    res, branchData = checkBranchAuthor(branchId, userData['id'], DB, allowHelpers=True)
    if not res: return branchData

    resp = DB.execute(sql.selectTaskMaxOrderidByBranchid, [branchId])
    maxOrderId = resp['maxorderid'] or 0

    resp = DB.execute(sql.insertTask, [branchId, title, description, question, answers, maxOrderId + 1])
    return jsonResponse(resp)


@app.route("/many", methods=["POST"])
@login_and_email_confirmation_required
def taskCreateMany(userData):
    try:
        req = request.json
        branchId = req['branchId']
        tasks = req['tasks']
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    print(branchId, userData['id'], tasks)
    res, branchData = checkBranchAuthor(branchId, userData['id'], DB, allowHelpers=True)
    if not res: return branchData

    resp = DB.execute(sql.selectTaskMaxOrderidByBranchid, [branchId])
    maxOrderId = resp['maxorderid'] or 0

    resp = []
    for task in tasks:
        maxOrderId += 1
        resp += [DB.execute(sql.insertTask, [branchId, task['title'], task['description'], task['question'], task['answers'], maxOrderId])]
    return jsonResponse({'tasks': resp})


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
        isQrAnswer = req.get('isQrAnswer')
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    res, taskData = checkTaskAuthor(taskId, userId, DB, allowHelpers=True)
    if not res: return taskData

    if title is None: title = taskData['title']
    if question is None: question = taskData['question']
    if answers is not None:
        answers = list(map(str.lower, answers))
    else:
        answers = taskData['answers']
    if description is None: description = taskData['description']
    if orderId is None: orderId = taskData['orderid']
    if isQrAnswer is None:
        isQrAnswer = taskData['isqranswer']

    resp = DB.execute(sql.updateTaskById, [orderId, title, description, question, answers, isQrAnswer, taskId])
    return jsonResponse(resp)


@app.route("", methods=["DELETE"])
@login_required_return_id
def taskDelete(userId):
    try:
        req = request.json
        taskId = req['id']
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    res, taskData = checkTaskAuthor(taskId, userId, DB, allowHelpers=True)
    if not res: return taskData

    DB.execute(sql.deleteTaskById, [taskId])

    # Make orderids actual
    branchId = taskData['branchid']
    resp = DB.execute(sql.selectTasksByBranchid, [branchId], manyResults=True)  # получаем все ветки
    idx = 1
    for task in resp:
        if task['orderid'] != idx:
            resp[idx-1] = DB.execute(sql.updateTaskOrderidById, [idx, task['id']])
        idx += 1
    return jsonResponse(resp)
