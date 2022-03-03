from flask import make_response

from constants import *
import database.SQL_requests as sql
from database.database import Database
from utils.utils import jsonResponse


def _checkAuthor(sqlRequest: str, args: list, fieldName: str, toCompare: any, DB: Database) -> (bool, dict or str):
    questData = DB.execute(sqlRequest, args)
    if questData[fieldName] != toCompare:
        return False, jsonResponse("Вы не являетесь автором квеста", HTTP_NO_PERMISSIONS)
    return True, questData


def checkQuestAuthor(questId, userId, DB) -> (bool, dict or str):
    return _checkAuthor(sql.selectQuestById, [questId], 'author', userId, DB)


def checkBranchAuthor(branchId, userId, DB) -> (bool, dict or str):
    return _checkAuthor(sql.selectQuestByBranchId, [branchId], 'author', userId, DB)


def checkTaskAuthor(taskId, userId, DB) -> (bool, dict or str):
    return _checkAuthor(sql.selectQuestByTaskId, [taskId], 'author', userId, DB)
