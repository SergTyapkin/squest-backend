from constants import *
import database.SQL_requests as sql
from database.database import Database
from utils.utils import jsonResponse


def _checkAuthor(sqlRequest: str, args: list, fieldName: str, toCompare: any, DB: Database) -> (bool, dict or str):
    questData = DB.execute(sqlRequest, args)
    if not questData:
        return False, jsonResponse("Квеста не существует", HTTP_NOT_FOUND)
    if questData[fieldName] != toCompare:
        return False, jsonResponse("Вы не являетесь автором квеста", HTTP_NO_PERMISSIONS)
    return True, questData


def _checkHelper(sqlRequest: str, args: list, DB: Database) -> (bool, dict or str):
    questData = DB.execute(sqlRequest, args)
    if len(questData) == 0:
        return False, jsonResponse("Вы не являетесь автором или соавтором квеста", HTTP_NO_PERMISSIONS)
    questData['helper'] = True
    return True, questData


# ------------
def checkQuestAuthor(questId, userId, DB, allowHelpers=False) -> (bool, dict or str):
    result = _checkAuthor(sql.selectQuestById, [questId], 'author', userId, DB)
    if not result[0] and allowHelpers:
        return _checkHelper(sql.selectQuestByIdHelperid, [questId, userId], DB)
    return result


def checkBranchAuthor(branchId, userId, DB, allowHelpers=False) -> (bool, dict or str):
    result = _checkAuthor(sql.selectQuestByBranchId, [branchId], 'author', userId, DB)
    if not result[0] and allowHelpers:
        return _checkHelper(sql.selectQuestByBranchidHelperId, [branchId, userId], DB)
    return result


def checkTaskAuthor(taskId, userId, DB, allowHelpers=False) -> (bool, dict or str):
    result = _checkAuthor(sql.selectQuestByTaskId, [taskId], 'author', userId, DB)
    if not result[0] and allowHelpers:
        return _checkHelper(sql.selectQuestByTaskidHelperId, [taskId, userId], DB)
    return result
