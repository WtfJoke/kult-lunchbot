from peewee import *
from configuration import Config


class DBHelper:

    db = None

    @staticmethod
    def get_db():
        if DBHelper.db is None:
            db = DBHelper.create_db()
        return db

    @staticmethod
    def create_db():
        Config.load_config()
        host = Config.get_db_host_name()
        port = Config.get_db_port()
        db_name = Config.get_db_name()
        user = Config.get_db_user()
        password = Config.get_db_password()

        db = PostgresqlDatabase(db_name, user=user, password=password, host=host, port=port)
        return db

    @staticmethod
    def create_db_tables():
        database = DBHelper.create_db()
        try:
            database.connect()
            database.create_tables([Token], safe=True)
        finally:
            database.close()


# model definitions -- the standard "pattern" is to define a base model class
# that specifies which database to use.  then, any subclasses will automatically
# use the correct storage.
class BaseModel(Model):
    class Meta:
        database = DBHelper.create_db()


# Represents an o-auth token in database
class Token(BaseModel):
    issuer = TextField(unique=True)
    token = TextField()
    app = CharField()


if __name__ == '__main__':
    DBHelper.create_db_tables()