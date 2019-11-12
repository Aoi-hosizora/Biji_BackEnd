# UserPass Format
UserNameMinLength = 5  # >=5
UserNameMaxLength = 30  # <30
PassWordMinLength = 8  # >= 8
PassWordMaxLength = 20  # 20

# App config
SecretKey = ""  # app.config

# Token Setting
Def_Expiration = 2592000  # Token Timeout (s) -> 30d
Def_Redis_Ex = 7200  # Redis zset token Timeout (s) -> 2h

# MySql config
MySQL_Host = 'localhost'
MySQL_Port = 3306
MySQL_User = 'root'
MySQL_Pass = '1234'
MySQL_Db = 'db_biji'

# Redis config
Redis_Host = 'localhost'
Redis_Port = 6379
