import sqlite3
import os


def connect():
    connection = sqlite3.connect(os.path.join("resources", "tokens.db"))
    return connection


def store(team_id, token):
    with connect() as connection:
        insert_statement = "INSERT OR IGNORE INTO token (team_id, token) VALUES ('{}', '{}')".format(team_id, token)
        connection.execute(insert_statement)
        connection.commit()


def get(team_id):
    with connect() as connection:
        cursor = connection.cursor()
        token = cursor.execute("SELECT token FROM token WHERE team_id=" + team_id).fetchone()
    if token:
        return token[0]
    else:
        print("Error: No token for team-id: " + team_id)
        return ''


if __name__ == "__main__":
    store('2','myTestToken')
    print(get('2'))

