from flask import Blueprint

from utils.access import *
from constants import *
from utils.utils import *

app = Blueprint('ratings', __name__)

_DB = Database(read_config("config.json"))


@app.route("")
def userAuth():
    resp = _DB.execute(sql.selectRatings, manyResults=True)
    addi = 0
    for i in range(len(resp)):
        i -= addi
        r = resp[i]
        if r['rating'] is None:
            r['rating'] = 0
            resp += [r]
            resp.pop(i)
            addi += 1
    return jsonResponse(resp)
