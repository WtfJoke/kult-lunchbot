from supported_apps import Apps
from models import DBHelper, Token


def store(team_id, auth_token, app):
    try:
        DBHelper.connect()
        token, created = Token.get_or_create(issuer=team_id, app=app, defaults={'token': auth_token})
        token.token = auth_token
        token.save()
    finally:
        DBHelper.close()


def remove(team_id):
    try:
        DBHelper.connect()
        token = Token.get(Token.issuer==team_id)
        delete_count = token.delete_instance()
    finally:
        DBHelper.close()


def get(team_id):
    try:
        DBHelper.connect()
        return Token.get(Token.issuer == team_id).token
    finally:
        DBHelper.close()


if __name__ == "__main__":
    store('2','myTestToken', Apps.SLACK)
    store('3', 'myTestToken', Apps.SLACK)
    store('2', 'someUpdatedToken', Apps.SLACK)
    print(get('2'))
    remove('2')
        #print(get('2'))

