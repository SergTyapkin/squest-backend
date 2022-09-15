from flask import Blueprint

from utils.access import *
from utils.utils import *

app = Blueprint('ratings', __name__)

_DB = Database(read_config("config.json"))


@app.route("")
def userAuth():
    resp = _DB.execute(sql.selectRatings, manyResults=True)
    for rating in resp:
        if rating['rating'] is None:
            rating['rating'] = 0
    return jsonResponse({'ratings': resp})
