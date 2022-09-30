from flask import Blueprint

from connections import DB
from utils.access import *
from constants import *
from utils.utils import *

app = Blueprint('admin', __name__)


@app.route("/sql", methods=["POST"])
@login_required_admin
def executeSQL():
    try:
        req = request.json
        sqlText = req['sql']
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    try:
        resp = DB.execute(sqlText, manyResults=True)
        return jsonResponse({"response": resp})
    except Exception as err:
        return jsonResponse(str(err), HTTP_INTERNAL_ERROR)
