class Config(object):
    # server
    SERVER_HOST = '0.0.0.0'
    SERVER_PORT = 8001

    SECRET_KEY = '{786C8A4B-9492-47C2-982D-74CECD921E74}'  # random uuid
    UPLOAD_FOLDER = './user/'
    UPLOAD_IMAGE_FOLDER = './user/image'
    UPLOAD_DOC_FOLDER = './user/document'

    # database
    MYSQL_HOST = 'localhost'
    MYSQL_PORT = 3306
    MYSQL_USER = 'root'
    MYSQL_PASS = '123'
    MYSQL_DB = 'db_biji'

    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    REDIS_DB = 0

    # token ex (Second)
    LOGIN_TOKEN_EX = 86400  # 1 * 24 * 3600 = 1 day
    SHARE_TOKEN_EX = 3600  # 1 * 3600 = 1 hour

    # format <= >=
    FMT_USERNAME_MIN = 5
    FMT_USERNAME_MAX = 30
    FMT_PASSWORD_MIN = 8
    FMT_PASSWORD_MAX = 20

    FMT_NOTE_TITLE_MIN = 1
    FMT_NOTE_TITLE_MAX = 50
    FMT_GROUP_NAME_MIN = 1
    FMT_GROUP_NAME_MAX = 30

    FMT_STAR_TITLE_MAX = 100
    FMT_STAR_CONTENT_MAX = 200

    FMT_DOCCLASS_NAME_MIN = 1
    FMT_DOCCLASS_NAME_MAX = 30
    FMT_DOCUMENT_UUID_LEN = 18 + 10  # 18 uuid + 10 Ext
