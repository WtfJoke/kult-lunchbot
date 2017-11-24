import yaml
import os
import logging


class Config:
    is_config_initialized = False

    @staticmethod
    def load_config():
        if Config.is_config_initialized:
            return
        filename = "config.yml"

        if os.path.exists(filename):
            with open(filename, 'r') as yml_file:
                cfg = yaml.load(yml_file)
            db_config = cfg['postgres']

            host = db_config['host']
            port = str(db_config['port'])
            user = db_config['user']
            password = db_config['password']
            db = db_config['db_name']

            # load config into environment variable
            os.environ['RDS_HOSTNAME'] = host
            os.environ['RDS_PORT'] = port
            os.environ['RDS_DB_NAME'] = db
            os.environ['RDS_USERNAME'] = user
            os.environ['RDS_PASSWORD'] = password
            logging.info("Set environment-variables successfully")
        else:
            logging.warning("Cant load config, assume variables get passed by environment variables")
            if not Config.get_db_host_name() \
                    or not Config.get_db_port() or not Config.get_db_name() \
                    or not Config.get_db_user() or not Config.get_db_password():
                message = "Please set all db configs"
                print("Error: " + message)
                raise Exception(message)

        Config.is_config_initialized = True

    @staticmethod
    def get_db_host_name():
        return os.environ['RDS_HOSTNAME']

    @staticmethod
    def get_db_port():
        return os.environ['RDS_PORT']

    @staticmethod
    def get_db_name():
        return os.environ['RDS_DB_NAME']

    @staticmethod
    def get_db_user():
        return os.environ['RDS_USERNAME']

    @staticmethod
    def get_db_password():
        return os.environ['RDS_PASSWORD']

