import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'secret_key'

class DeploymentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///forumDB.db'

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # 使用内存中的 SQLite 数据库
    WTF_CSRF_ENABLED = False