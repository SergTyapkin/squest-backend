import requests

base_path = "http://127.0.0.1:9000/api"
session = requests.Session()

requests_total = 0


def respInfo(resp):
    global requests_total
    requests_total += 1
    print("#", requests_total, ": ", sep="")
    print(resp.status_code, resp.headers)
    print(resp.content.decode())
    print("---")


def post(path, data):
    respInfo(session.post(base_path + path, json=data))


def put(path, data):
    respInfo(session.put(base_path + path, json=data))


def get(path):
    respInfo(session.get(base_path + path))


def delete(path):
    respInfo(session.delete(base_path + path))


if __name__ == '__main__':
    # Create user
    # post("/user", {
    #     "name": "Serg",
    #     "password": "root",
    #     "university": "МГТУ",
    #     "educationGroup": "РК6-62Б",
    #     "groupRole": "student",
    #     # "avatarUrl": "",
    #     "email": "Tyapki2002@mail.ru",
    # })
    #
    # get("/user")
    #
    # delete("/user/session")

    # Auth user
    post("/user/auth", {
        "username": "Serg",
        "password": "root",
    })

    get("/user")

    # Update user
    put("/user", {
        "email": "ty@mail.ru"
    })

    put("/user/password", {"oldPassword": "root",
                            "newPassword": "rootable"})

    put("/user/password", {"oldPassword": "rootable",
                            "newPassword": "root"})

    # Log out
    delete("/user/session")
