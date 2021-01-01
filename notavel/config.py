"""Configuration module for Notável App"""
import os


class Config:
    TESTING = False
    DEBUG = os.environ["DEBUG"]
    DB_NAME = "notaveldev"
    DB_USER = os.environ["POSTGRES_USER"]
    DB_PASS = os.environ["POSTGRES_PASSWORD"]
    DB_SERVICE = os.environ["DB_SERVICE"]
    DB_PORT = os.environ["DB_PORT"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return f"{self.DB_SERVICE}://{self.DB_USER}:{self.DB_PASS}@{self.DB_SERVICE}:{self.DB_PORT}/{self.DB_NAME}"


class TestingConfig(Config):
    DB_NAME = "notaveltest"
    DEBUG = True
    TESTING = True
