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
        project_root = os.path.dirname(os.path.realpath(__file__))
        config_path = os.path.join(project_root, filename)

        if os.path.exists(config_path):
            Config.load_from_file(config_path)
        else:
            Config.load_from_environment()

        Config.is_config_initialized = True

    @staticmethod
    def load_from_environment():
        logging.warning("Cant load config, assume variables get passed by environment variables")
        if not Config.get_db_host_name() \
                or not Config.get_db_port() or not Config.get_db_name() \
                or not Config.get_db_user() or not Config.get_db_password():
            message = "Please set all db configs"
            print("Error: " + message)
            raise Exception(message)

    @staticmethod
    def load_from_file(filename):
        with open(filename, 'r') as yml_file:
            cfg = yaml.safe_load(yml_file)
        Config.load_db_config(cfg)
        Config.load_sti_api_config(cfg)
        logging.info("Set environment-variables successfully")

    @staticmethod
    def load_db_config(cfg):
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

    @staticmethod
    def load_sti_api_config(cfg):
        if 'sti-api' not in cfg:
            logging.warning("No STI-API credentials - Menu of Restaurant Stiftsberg cant be fetched")
            # TODO use disable flag in STI-* classes
            return
        api_config = cfg['sti-api']
        user = api_config['user']
        password = api_config['password']

        os.environ['STI_API_USER'] = user
        os.environ['STI_API_PASSWORD'] = password

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

