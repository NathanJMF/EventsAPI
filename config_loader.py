import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance.load_config()
        return cls._instance

    def load_config(self):
        self.__test_flag = os.getenv("GLOBAL_TEST_FLAG", "false")
        self.__backend_port = os.getenv("BACKEND_PORT")
        self.__db_host = os.getenv("DB_HOST")
        self.__db_port = os.getenv("DB_PORT")
        self.__db_name = os.getenv("DB_NAME")
        self.__db_user = os.getenv("DB_USER")
        self.__db_password = os.getenv("DB_PASSWORD")

    @property
    def test_flag(self):
        return self.__test_flag.lower() in ("true", "1", "yes")

    @property
    def backend_port(self):
        return self.__backend_port

    @property
    def db_host(self):
        return self.__db_host

    @property
    def db_port(self):
        return self.__db_port

    @property
    def db_name(self):
        return self.__db_name

    @property
    def db_user(self):
        return self.__db_user

    @property
    def db_password(self):
        return self.__db_password
