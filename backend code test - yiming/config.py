import os
SECRET_KEY = "asdfasdfjasdfjasd;lf"


BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # 获取当前文件的绝对路径
DATABASE = 'frog论坛.db'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, DATABASE)




# 邮箱配置
MAIL_SERVER = "smtp.qq.com"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = "673473446@qq.com"
MAIL_PASSWORD = "gifjutdblutcbbcj"
MAIL_DEFAULT_SENDER = "673473446@qq.com"