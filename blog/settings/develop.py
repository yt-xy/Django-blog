from .base import *  # NOQA
# NOQA的作用是，告诉PEP 8规范工具，这里不需要检测


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 连接的数据库类型
        'NAME': "project",  # 数据库名称
        'HOST': '127.0.0.1',  # 连接数据库的地址
        'PORT': 3306,  # 端口
        'USER': 'root',  # 用户
        'PASSWORD': '123456',  # 密码
    }
}