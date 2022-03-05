from flask import Blueprint, Response

from utils.access import *
from utils.questUtils import *
from utils.utils import *

import base64

app = Blueprint('images', __name__)

_DB = Database(read_config("config.json"))


@app.route("/<imageId>")
def imageGet(imageId):
    resp = _DB.execute(sql.selectImageById, [imageId])
    base64Data = resp['base64']
    imageBytes = base64.b64decode(base64Data)
    return Response(imageBytes, mimetype=f'image/{resp["type"]}')


_leftLen = len('data:image/')
_rightLen = len(';base64')
@app.route("", methods=["POST"])
@login_required_return_id
def imageUpload(userId):
    try:
        req = request.json
        dataUrl = req['dataUrl']
    except:
        return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    [dataUrl, base64Data] = dataUrl.split(',')
    imageType = dataUrl[_leftLen: -_rightLen]

    resp = _DB.execute(sql.insertImage, [userId, imageType, base64Data])
    return jsonResponse(resp)


@app.route("/<imageId>", methods=["DELETE"])
@login_required_return_id
def imageDelete(userId, imageId):
    _DB.execute(sql.deleteImageByIdAuthor, [imageId, userId])
    return jsonResponse("Изображение удалено")
