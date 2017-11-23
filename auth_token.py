from supported_apps import Apps
from configuration import Config
import psycopg2


def connect():
    host = Config.get_db_host_name()
    port = Config.get_db_port()
    db = Config.get_db_name()
    user = Config.get_db_user()
    password = Config.get_db_password()

    connection = psycopg2.connect(dbname=db, user=user, password=password, host=host, port=port)
    return connection


def store(team_id, token, app):
    with connect() as connection, connection.cursor() as cursor:
        insert_statement = "INSERT INTO tokens (team_id, token, app) VALUES (%s, %s, %s) " \
                           "ON conflict(team_id) DO UPDATE SET token=%s"
        cursor.execute(insert_statement, (team_id, token, app.value, token))
        connection.commit()


def remove(team_id):
    with connect() as connection, connection.cursor() as cursor:
        delete_statement = "DELETE FROM tokens WHERE team_id=%s"
        cursor.execute(delete_statement, team_id)
        connection.commit()


def get(team_id):
    with connect() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT token FROM tokens WHERE team_id=%s", team_id)
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            print("Error: No token for team-id: " + team_id)
            return ''


def create_table():
    with connect() as connection, connection.cursor() as cursor:
        cursor.execute("CREATE TABLE IF NOT EXISTS "
                       "tokens (id serial PRIMARY KEY, team_id varchar UNIQUE, token varchar, app varchar);")
        connection.commit()


if __name__ == "__main__":
    Config.load_config()
    create_table()
    store('2','myTestToken', Apps.SLACK)
    store('3', 'myTestToken', Apps.SLACK)
    store('2', 'someUpdatedToken', Apps.SLACK)
    print(get('2'))
    remove('2')
    print(get('2'))

