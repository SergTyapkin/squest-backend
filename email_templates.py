from utils.utils import read_config

config = read_config('config.json')

def _default_template(avatarUrl, fullName, htmlContent):
    avatarDiv = '<br>'
    if avatarUrl:
        avatarDiv = f'''<img src="{config['api_url']}{avatarUrl}" height="80px" width="80px" alt="avatar" title="avatar" style="margin: 20px auto;border-radius: 40px"/>
            <br>
        '''

    fullNameDiv = ''
    if fullName:
        fullNameDiv = f'''<span style="font-weight: bold;font-size: 22px;color: #f3f3f3;">{fullName},</span>
            <br>
            <br>
        '''

    return f"""
    <div style="background: linear-gradient(-20deg,#b8860b 0%,#5b3509 20%,#1c051c 70%,#0e0909 100%);">
        <div style="margin-left: auto;margin-right: auto;width: 100%;max-width: 600px;padding:40px 0;font-family: Arial, sans-serif">
            <div style="margin: 40px 0;padding: 0 35px 25px;text-align: center;color: #d5d5d5;background: linear-gradient(20deg,#1c051c 0%,#5b3509 50%,#29190c 100%) 50% 50% no-repeat;box-shadow: 3px 3px 10px #000;border-radius: 7px;line-height: 1.3;font-size: 16px;">
                {avatarDiv}
    
                {fullNameDiv}
                
                <div class="content">
                    {htmlContent}
                </div>
                
                <br>
                <div style="padding: 0 15px;color: #aaa;font-size: 11px;text-align: center;">
                    <span>Ты получаешь это письмо, потому что этот адрес почты указапри регистрации на SQuest.</span>
                    <br>
                    <span>С этого электронного адреса приходят только важные письма для восстановления пароля, входа в аккаунт и.т.п.</span>
                </div>
            </div>
    
            <div style="padding: 20px 30px;color: #666;overflow: auto;background-color: #00000055;border-radius: 7px">
                <span style="float: left">
                    <a href="{config['frontend_url']}" target="_blank" style="font-size: 13px;font-weight: bold;color: #e7e7e7 !important;" rel=" noopener noreferrer">SQuest.ml</a>
                    <br>
                    <span style="color: #b9b9b9;font-size: 12px;">SQuest Ltd., ул. Пушкина, д. Колотушкина.</span>
                </span>
    
                <div style="float: right;padding: 8px 0 8px 20px;">
                    <span style="vertical-align: middle;padding-right: 10px;font-size: 13px;color: #b9b9b9;">Соцсети:</span>
                    <a style="margin-left: 5px;height: 22px;vertical-align: middle" href="https://vk.com/squest_studio" target="_blank" rel=" noopener noreferrer">
                        <img width="22px" height="22px" alt="vk" title="vk" src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNTEycHgiIGhlaWdodD0iNTEycHgiIHZpZXdCb3g9IjAgMCA1MTIgNTEyIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIGZpbGw9IiM5MzYzMjgiPg0KICAgIDxwYXRoIGQ9Ik00ODQuNywxMzJjMy41Ni0xMS4yOCwwLTE5LjQ4LTE1Ljc1LTE5LjQ4SDQxNi41OGMtMTMuMjEsMC0xOS4zMSw3LjE4LTIyLjg3LDE0Ljg2LDAsMC0yNi45NCw2NS42LTY0LjU2LDEwOC4xMy0xMi4yLDEyLjMtMTcuNzksMTYuNC0yNC40LDE2LjQtMy41NiwwLTguMTQtNC4xLTguMTQtMTUuMzdWMTMxLjQ3YzAtMTMuMzItNC4wNi0xOS40Ny0xNS4yNS0xOS40N0gxOTljLTguMTQsMC0xMy4yMiw2LjE1LTEzLjIyLDEyLjMsMCwxMi44MSwxOC44MSwxNS44OSwyMC44NCw1MS43NlYyNTRjMCwxNi45MS0zLDIwLTkuNjYsMjAtMTcuNzksMC02MS02Ni4xMS04Ni45Mi0xNDEuNDRDMTA1LDExNy42NCw5OS44OCwxMTIsODYuNjYsMTEySDMzLjc5QzE4LjU0LDExMiwxNiwxMTkuMTcsMTYsMTI2Ljg2YzAsMTMuODQsMTcuNzksODMuNTMsODIuODYsMTc1Ljc3LDQzLjIxLDYzLDEwNC43Miw5Ni44NiwxNjAuMTMsOTYuODYsMzMuNTYsMCwzNy42Mi03LjY5LDM3LjYyLTIwLjVWMzMxLjMzYzAtMTUuMzcsMy4wNS0xNy45MywxMy43My0xNy45Myw3LjYyLDAsMjEuMzUsNC4wOSw1Mi4zNiwzNC4zM0MzOTguMjgsMzgzLjYsNDA0LjM4LDQwMCw0MjQuMjEsNDAwaDUyLjM2YzE1LjI1LDAsMjIuMzctNy42OSwxOC4zLTIyLjU1LTQuNTctMTQuODYtMjEuODYtMzYuMzgtNDQuMjMtNjItMTIuMi0xNC4zNC0zMC41LTMwLjIzLTM2LjA5LTM3LjkyLTcuNjItMTAuMjUtNS41OS0xNC4zNSwwLTIzLjU3LS41MSwwLDYzLjU1LTkxLjIyLDcwLjE1LTEyMiIgc3R5bGU9ImZpbGwtcnVsZTpldmVub2RkIi8+DQo8L3N2Zz4NCg=="/>
                    </a>
                    <a style="margin-left: 5px;height: 22px;vertical-align: middle" href="https://t.me/tyapkin_s" target="_blank" rel=" noopener noreferrer">
                        <img width="22px" height="22px" alt="tg" title="tg" src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjRweCIgaGVpZ2h0PSIyNHB4IiB2aWV3Qm94PSIwIDAgMjQgMjQiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgZmlsbD0iIzkzNjMyOCI+DQogICAgPHBhdGggZD0ibTIwLjY2NSAzLjcxNy0xNy43MyA2LjgzN2MtMS4yMS40ODYtMS4yMDMgMS4xNjEtLjIyMiAxLjQ2Mmw0LjU1MiAxLjQyIDEwLjUzMi02LjY0NWMuNDk4LS4zMDMuOTUzLS4xNC41NzkuMTkybC04LjUzMyA3LjcwMWgtLjAwMmwuMDAyLjAwMS0uMzE0IDQuNjkyYy40NiAwIC42NjMtLjIxMS45MjEtLjQ2bDIuMjExLTIuMTUgNC41OTkgMy4zOTdjLjg0OC40NjcgMS40NTcuMjI3IDEuNjY4LS43ODVsMy4wMTktMTQuMjI4Yy4zMDktMS4yMzktLjQ3My0xLjgtMS4yODItMS40MzR6Ii8+DQo8L3N2Zz4NCg=="/>
                    </a>
                </div>
            </div>
        </div>
    </div>
    """


def restorePassword(avatarUrl, fullName, code):
    return _default_template(avatarUrl, fullName, f"""
    <span style="color: #d5d5d5">пароль опять выпал из памяти, но ты очень хочешь попасть в свой аккаунт? Во-первых <b> пей таблетки</b>, и больше <b>не забывай</b> пароли.</span>
    <br>
    <br>
    <span style="color: #d5d5d5">А во-вторых - так и быть, держи сылку для восстановления пароля:</span>
    <br>
    <a href="{config['frontend_url']}/password/restore?code={code}" target="_blank" style="margin-top:10px;line-height: 1;box-sizing: border-box;display: inline-block;max-width: 100%;padding: 10px 15px;border-radius: 5px;background: linear-gradient(20deg,rgba(45,36,13,0.4) 0%,rgba(90,56,25,0.7) 50%,rgba(55,43,16,0.4) 100%) 50% 50% no-repeat;border: 1px #b08946 solid;box-shadow: inset 0 0 0 transparent, 5px 5px 10px rgb(0 0 0 / 33%);font-weight: bold;color: #fff !important;" rel=" noopener noreferrer"><span style="display: inline-block;width: 14px;height: 18px;vertical-align: middle;"></span> Восстановить пароль</a>
    <br>
    <span style="color: #d5d5d5">Кстати, она действительна всего час</span>    
    """)


def loginByCode(avatarUrl, fullName, code):
    return _default_template(avatarUrl, fullName, f"""
    <span style="color: #d5d5d5">неужели прям так лень запоминать пароль? Вот твой одноразовый код:</span>
    <br>
    <br>
    <div style="font-weight: bold;font-size: 25px;letter-spacing: 5px;color: #f3f3f3">{code}</div>
    <br>
    <span style="color: #d5d5d5">Кстати, он действителен всего час</span>     
    """)


def confirmEmail(avatarUrl, fullName, code):
    return _default_template(avatarUrl, fullName, f"""
    <span style="color: #d5d5d5">ну что за красивое личико смотрит на это письмо с той стороны экрана?</span>
    <br>
    <span style="color: #d5d5d5">Давай к делу - смотри, сколько всего тебе будет доступно после подтверждения этого адреса:</span>
    <br>
    <br>
    <hr>
    <div style="padding: 0 20px;font-size: 0;text-align: left;color: #c9c9c9">
        <div style="display: inline-block;width: 50%;min-width: 200px;vertical-align: top">
            <div style="color: #ff9b9b;box-sizing: border-box;white-space: nowrap;overflow:hidden;padding: 0;font-weight: normal;letter-spacing: 1px;font-size: 14px;">Без подтверждения:</div>
            <div style="box-sizing: border-box;white-space: nowrap;padding: 0;font-weight: bold;font-size: 16px;"><img width="16px" height="16px" alt="+" title="+" style="margin-right: 5px" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAA21BMVEUAAACn3pen3Zek3ZSk3Zuo35ao35in3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pf////fFRzGAAAAR3RSTlMAAAAAAAAACC+hAVLa/A198vaCSwYjqfRtA+6NEkXP8WkC2LIob+rvZD7c00cbm/rtX1HphsFacvnoVQeS5VATseJMJq5JC6ztA3IAAAABYktHREjwAtTqAAAACXBIWXMAAC4jAAAuIwF4pT92AAAAB3RJTUUH5gkeCSMK4LK1EgAAAJlJREFUGNNdj9cSglAMRO9eO/au2Bv23ns3//9HBmQAyUOSM5Ps7ArhLABuDrg4GBJS2qiEI1F9ekyOxRPJlEhnDCVu2RzlC0WhlsqQjKhUqVZvQDSp1dbVOxp1ewof9wc0HGE8mdJs7jWeFyotV2sibfOzBd92R1z7g2kTOJ6YzxfLNnC90f1hx+Dt+Xo7Y/H+8f/F1G1Z/AW0LQ8JQaD9NQAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAyMi0wOS0zMFQwOTozNTowMCswMDowMFdLzoYAAAAldEVYdGRhdGU6bW9kaWZ5ADIwMjItMDktMzBUMDk6MzU6MDArMDA6MDAmFnY6AAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAAABJRU5ErkJggg=="/>Просмотр квестов</div>
            <div style="box-sizing: border-box;white-space: nowrap;padding: 0;font-weight: bold;font-size: 16px;"><img width="16px" height="16px" alt="+" title="+" style="margin-right: 5px" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAA21BMVEUAAACn3pen3Zek3ZSk3Zuo35ao35in3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pf////fFRzGAAAAR3RSTlMAAAAAAAAACC+hAVLa/A198vaCSwYjqfRtA+6NEkXP8WkC2LIob+rvZD7c00cbm/rtX1HphsFacvnoVQeS5VATseJMJq5JC6ztA3IAAAABYktHREjwAtTqAAAACXBIWXMAAC4jAAAuIwF4pT92AAAAB3RJTUUH5gkeCSMK4LK1EgAAAJlJREFUGNNdj9cSglAMRO9eO/au2Bv23ns3//9HBmQAyUOSM5Ps7ArhLABuDrg4GBJS2qiEI1F9ekyOxRPJlEhnDCVu2RzlC0WhlsqQjKhUqVZvQDSp1dbVOxp1ewof9wc0HGE8mdJs7jWeFyotV2sibfOzBd92R1z7g2kTOJ6YzxfLNnC90f1hx+Dt+Xo7Y/H+8f/F1G1Z/AW0LQ8JQaD9NQAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAyMi0wOS0zMFQwOTozNTowMCswMDowMFdLzoYAAAAldEVYdGRhdGU6bW9kaWZ5ADIwMjItMDktMzBUMDk6MzU6MDArMDA6MDAmFnY6AAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAAABJRU5ErkJggg=="/>Прохождение заданий</div>
            <div style="box-sizing: border-box;white-space: nowrap;padding: 0;font-weight: bold;font-size: 16px;">&nbsp;</div>
        </div>
        <div style="display: inline-block;width: 50%;min-width: 200px">
            <div style="color: #afff9c;box-sizing: border-box;white-space: nowrap;overflow:hidden;padding: 0;font-weight: normal;letter-spacing: 1px;font-size: 14px;">С подтверждением:</div>
            <div style="box-sizing: border-box;white-space: nowrap;padding: 0;font-weight: bold;font-size: 16px;"><img width="16px" height="16px" alt="+" title="+" style="margin-right: 5px" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAA21BMVEUAAACn3pen3Zek3ZSk3Zuo35ao35in3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pf////fFRzGAAAAR3RSTlMAAAAAAAAACC+hAVLa/A198vaCSwYjqfRtA+6NEkXP8WkC2LIob+rvZD7c00cbm/rtX1HphsFacvnoVQeS5VATseJMJq5JC6ztA3IAAAABYktHREjwAtTqAAAACXBIWXMAAC4jAAAuIwF4pT92AAAAB3RJTUUH5gkeCSMK4LK1EgAAAJlJREFUGNNdj9cSglAMRO9eO/au2Bv23ns3//9HBmQAyUOSM5Ps7ArhLABuDrg4GBJS2qiEI1F9ekyOxRPJlEhnDCVu2RzlC0WhlsqQjKhUqVZvQDSp1dbVOxp1ewof9wc0HGE8mdJs7jWeFyotV2sibfOzBd92R1z7g2kTOJ6YzxfLNnC90f1hx+Dt+Xo7Y/H+8f/F1G1Z/AW0LQ8JQaD9NQAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAyMi0wOS0zMFQwOTozNTowMCswMDowMFdLzoYAAAAldEVYdGRhdGU6bW9kaWZ5ADIwMjItMDktMzBUMDk6MzU6MDArMDA6MDAmFnY6AAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAAABJRU5ErkJggg=="/>Ты в рейтинге</div>
            <div style="box-sizing: border-box;white-space: nowrap;padding: 0;font-weight: bold;font-size: 16px;"><img width="16px" height="16px" alt="+" title="+" style="margin-right: 5px" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAA21BMVEUAAACn3pen3Zek3ZSk3Zuo35ao35in3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pf////fFRzGAAAAR3RSTlMAAAAAAAAACC+hAVLa/A198vaCSwYjqfRtA+6NEkXP8WkC2LIob+rvZD7c00cbm/rtX1HphsFacvnoVQeS5VATseJMJq5JC6ztA3IAAAABYktHREjwAtTqAAAACXBIWXMAAC4jAAAuIwF4pT92AAAAB3RJTUUH5gkeCSMK4LK1EgAAAJlJREFUGNNdj9cSglAMRO9eO/au2Bv23ns3//9HBmQAyUOSM5Ps7ArhLABuDrg4GBJS2qiEI1F9ekyOxRPJlEhnDCVu2RzlC0WhlsqQjKhUqVZvQDSp1dbVOxp1ewof9wc0HGE8mdJs7jWeFyotV2sibfOzBd92R1z7g2kTOJ6YzxfLNnC90f1hx+Dt+Xo7Y/H+8f/F1G1Z/AW0LQ8JQaD9NQAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAyMi0wOS0zMFQwOTozNTowMCswMDowMFdLzoYAAAAldEVYdGRhdGU6bW9kaWZ5ADIwMjItMDktMzBUMDk6MzU6MDArMDA6MDAmFnY6AAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAAABJRU5ErkJggg=="/>Создание квестов</div>
            <div style="box-sizing: border-box;white-space: nowrap;padding: 0;font-weight: bold;font-size: 16px;"><img width="16px" height="16px" alt="+" title="+" style="margin-right: 5px" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAA21BMVEUAAACn3pen3Zek3ZSk3Zuo35ao35in3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pf////fFRzGAAAAR3RSTlMAAAAAAAAACC+hAVLa/A198vaCSwYjqfRtA+6NEkXP8WkC2LIob+rvZD7c00cbm/rtX1HphsFacvnoVQeS5VATseJMJq5JC6ztA3IAAAABYktHREjwAtTqAAAACXBIWXMAAC4jAAAuIwF4pT92AAAAB3RJTUUH5gkeCSMK4LK1EgAAAJlJREFUGNNdj9cSglAMRO9eO/au2Bv23ns3//9HBmQAyUOSM5Ps7ArhLABuDrg4GBJS2qiEI1F9ekyOxRPJlEhnDCVu2RzlC0WhlsqQjKhUqVZvQDSp1dbVOxp1ewof9wc0HGE8mdJs7jWeFyotV2sibfOzBd92R1z7g2kTOJ6YzxfLNnC90f1hx+Dt+Xo7Y/H+8f/F1G1Z/AW0LQ8JQaD9NQAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAyMi0wOS0zMFQwOTozNTowMCswMDowMFdLzoYAAAAldEVYdGRhdGU6bW9kaWZ5ADIwMjItMDktMzBUMDk6MzU6MDArMDA6MDAmFnY6AAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAAABJRU5ErkJggg=="/>Создание команд</div>
            <div style="box-sizing: border-box;white-space: nowrap;padding: 0;font-weight: bold;font-size: 16px;"><img width="16px" height="16px" alt="+" title="+" style="margin-right: 5px" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAA21BMVEUAAACn3pen3Zek3ZSk3Zuo35ao35in3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pen3pf////fFRzGAAAAR3RSTlMAAAAAAAAACC+hAVLa/A198vaCSwYjqfRtA+6NEkXP8WkC2LIob+rvZD7c00cbm/rtX1HphsFacvnoVQeS5VATseJMJq5JC6ztA3IAAAABYktHREjwAtTqAAAACXBIWXMAAC4jAAAuIwF4pT92AAAAB3RJTUUH5gkeCSMK4LK1EgAAAJlJREFUGNNdj9cSglAMRO9eO/au2Bv23ns3//9HBmQAyUOSM5Ps7ArhLABuDrg4GBJS2qiEI1F9ekyOxRPJlEhnDCVu2RzlC0WhlsqQjKhUqVZvQDSp1dbVOxp1ewof9wc0HGE8mdJs7jWeFyotV2sibfOzBd92R1z7g2kTOJ6YzxfLNnC90f1hx+Dt+Xo7Y/H+8f/F1G1Z/AW0LQ8JQaD9NQAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAyMi0wOS0zMFQwOTozNTowMCswMDowMFdLzoYAAAAldEVYdGRhdGU6bW9kaWZ5ADIwMjItMDktMzBUMDk6MzU6MDArMDA6MDAmFnY6AAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAAABJRU5ErkJggg=="/>Оценка квестов</div>
        </div>
    </div>
    <hr>
    <br>
    <div style="margin-top: 20px;padding: 0 0 0 25px;text-transform: uppercase;font-weight: bold">Осталось только</div>
    <a href="{config['frontend_url']}/email/confirm?code={code}" target="_blank" style="margin-top:10px;line-height: 1;box-sizing: border-box;display: inline-block;max-width: 100%;padding: 10px 15px;border-radius: 5px;background: linear-gradient(20deg,rgba(45,36,13,0.4) 0%,rgba(90,56,25,0.7) 50%,rgba(55,43,16,0.4) 100%) 50% 50% no-repeat;border: 1px #b08946 solid;box-shadow: inset 0 0 0 transparent, 5px 5px 10px rgb(0 0 0 / 33%);font-weight: bold;color: #fff !important;" rel=" noopener noreferrer"><span style="display: inline-block;width: 14px;height: 18px;vertical-align: middle;"></span> Подтвердить регистрацию</a>
    <br>
    <br>
    <span>Ссылка для подтверждения действительна всего день</span>        
    """)
