from supported_apps import Apps
from models import DBHelper, Token


def store(team_id, auth_token, app):
    token, created = Token.get_or_create(issuer=team_id, app=app, defaults={'token': auth_token})
    token.token = auth_token
    token.save()


def remove(team_id):
    token = Token.get(Token.issuer==team_id)
    delete_count = token.delete_instance()


def get(team_id):
    return Token.get(Token.issuer == team_id).token


if __name__ == "__main__":
    try:
        DBHelper.get_db().connect()
        store('2','myTestToken', Apps.SLACK)
        store('3', 'myTestToken', Apps.SLACK)
        store('2', 'someUpdatedToken', Apps.SLACK)
        print(get('2'))
        remove('2')
        #print(get('2'))
    finally:
        if not DBHelper.get_db().is_closed():
            DBHelper.get_db().close()

