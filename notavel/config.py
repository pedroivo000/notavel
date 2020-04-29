"""Configuration module for Notável App"""
import os


class Config:
    DEBUG = os.environ["DEBUG"]
    DB_NAME = os.environ["POSTGRES_DB"]
    DB_USER = os.environ["POSTGRES_USER"]
    DB_PASS = os.environ["POSTGRES_PASSWORD"]
    DB_SERVICE = os.environ["DB_SERVICE"]
    DB_PORT = os.environ["DB_PORT"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = (
        f"{DB_SERVICE}://{DB_USER}:{DB_PASS}@{DB_SERVICE}:{DB_PORT}/{DB_NAME}"
    )
