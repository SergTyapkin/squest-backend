from flask import Blueprint

from utils.access import *
from utils.utils import *

app = Blueprint('ratings', __name__)

_DB = Database(read_config("config.json"))


@app.route("")
def userAuth():
    resp = _DB.execute(sql.selectRatings, manyResults=True)
    notNoneRatings = []
    noneRatings = []
    for rating in resp:
        if rating['rating'] is None:
            rating['rating'] = 0
            noneRatings.append(rating)
        else:
            notNoneRatings.append(rating)

    return jsonResponse({'ratings': notNoneRatings + noneRatings})
