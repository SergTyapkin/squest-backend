from flask import Blueprint
from markdown import markdown

from utils.access import *
from utils.questUtils import *
from utils.utils import *


app = Blueprint('tasks', __name__)

_DB = Database(read_config("config.json"))


@app.route("")
@login_required_return_id
def tasksGet(userId):
    try:
        req = request.json
        branchId = req['branchId']
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    branchData = _DB.execute(sql.selectQuestByBranchId, [branchId])

    if branchData['author'] == userId:
        resp = _DB.execute(sql.selectTasksByBranchid, [branchId])
        return jsonResponse(resp)

    jsonResponse("Нет прав просмотра заданий в этой ветке", HTTP_NO_PERMISSIONS)  # нельзя


def getUserProgress(userData):
    resp = _DB.execute(sql.selectProgressByUserid, [userData['id']])
    try:
        progress = resp['progress']
    except KeyError:  # прогресса нет - надо создать нулевой прогресс
        resp = _DB.execute(sql.insertProgress, [userData['id'], userData['chosenbranchid']])
        progress = resp['progress']
    return progress + 1


@app.route("/play")
@login_required
def tasksGetLast(userData):
    if userData['chosenbranchid'] is None or userData['chosenquestid'] is None:
        return jsonResponse("Квест или ветка не выбраны", HTTP_INVALID_DATA)

    progress = getUserProgress(userData)

    # Можно получить только последний таск в выбранной ветке и квесте только если
    # ветка и квест опубликованы (проверки на это нет)
    resp = _DB.execute(sql.selectTaskByBranchidNumber, [userData['chosenbranchid'], progress])
    # Добавим к ответу названия квеста и ветки
    questResp = _DB.execute(sql.selectQuestById, [userData['chosenquestid']])
    branchResp = _DB.execute(sql.selectBranchLengthById, [userData['chosenbranchid']])
    resp['questtitle'] = questResp['title']
    resp['branchtitle'] = branchResp['title']
    # Добавим к ответу прогресс и общую длину ветки
    resp['progress'] = progress
    resp['length'] = branchResp['length']
    return jsonResponse(resp)


@app.route("/play", methods=["POST"])
@login_required
def tasksCheckAnswer(userData):
    try:
        req = request.json
        answer = req['answer'].lower()
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    progress = getUserProgress(userData)

    taskId = _DB.execute(sql.checkTaskAnswerByBranchidAnswerProgress, [userData['chosenbranchid'], answer, progress])
    if not taskId:
        return jsonResponse("Ответ неверен", HTTP_ANSWER_MISS)

    _DB.execute(sql.increaseProgressByUseridBranchid, [userData['id'], userData['chosenbranchid']])
    return jsonResponse("Правильно")


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

    description = markdown(description)

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
    question = question or taskData['question']
    answers = answers or taskData['answers']

    if description:
        description = markdown(description)
    else:
        description = taskData['description']

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
