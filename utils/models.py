from flask import request, make_response, jsonify

from constants import HTTP_INVALID_DATA
from utils.access import get_logined_user


class Model:
    fieldNames = {
        # json_name: [DB_name, options, default],
        # options:
        #   +  : required
        #   a  : admin permissions
        #   a+ : admin + required
    }
    fields = {}

    _fieldDBNames = {}

    def __init__(self):
        for json_name, val in self.fieldNames.items():
            self._fieldDBNames[val[0]] = json_name

    def __str__(self):
        return self.fields

    def byRequest(self, needResponseOnError: bool = True, perm: dict = {}):
        try:
            self._byRequest(perm)
        except:
            if needResponseOnError:
                return jsonResponse("Не удалось сериализовать json", HTTP_INVALID_DATA)

    def _byRequest(self, customPermissions):
        data = request.json

        userData = get_logined_user()
        isAdmin = False
        if userData is not None and userData['isadmin']:
            isAdmin = True

        for json_name, val in self.fieldNames.items():
            if json_name in customPermissions:
                option = customPermissions[json_name]
            else:
                try:               option = val[1]
                except IndexError: option = ''
            try:               default = val[2]
            except IndexError: default = None

            if option == '+':
                self.fields[json_name] = data[json_name]
            elif option == 'a':
                if not isAdmin:
                    self.fields[json_name] = default
                else:
                    self.fields[json_name] = data.get(json_name, default)
            elif option == 'a+':
                if not isAdmin:
                    raise PermissionError(f'For field {json_name} need admin permissions')
                self.fields[json_name] = data[json_name]
            else:
                self.fields[json_name] = data.get(json_name, default)

    def toResponse(self, needCleanup: bool = True):
        if not needCleanup:
            return jsonResponse(self.fields))

        cleaned = {}
        for key, val in self.fields.items():
            if val is not None:
                cleaned[key] = val

        return jsonResponse(cleaned))

    def toDB(self, *args: list[str]):
        dbList = []
        for name in args:
            dbList += self.fields[name]
        return dbList

    def byDB(self, data: dict):
        for dbName, val in data.items():
            self.fields[self._fieldDBNames[dbName]] = val


class User(Model):
    fieldNames = {
        'username': ['name', '+'],
        'password': ['password'],
        'email': ['email'],
        'isAdmin': ['isadmin', 'a'],
        'isConfirmed': ['isconfirmed', 'a'],
        'avatarUrl': ['avatarurl'],
        'questId': ['chosenQuestId']
    }
