from flask import Blueprint

from utils.access import *
from constants import *
from utils.utils import *

app = Blueprint('ratings', __name__)

_DB = Database(read_config("config.json"))


@app.route("")
def userAuth():
    resp = _DB.execute(sql.selectRatings, manyResults=True)
    for r in resp:
        if r['rating'] is None:
            r['rating'] = 0
    return jsonResponse(resp)
