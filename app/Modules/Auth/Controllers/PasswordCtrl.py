from app.Database.UserDAO import UserDAO
from app.Database.TokenDAO import TokenDAO

from app.Modules.Auth.Exceptions.UserExistError import UserExistError
from app.Modules.Auth.Exceptions.UserNotExistError import UserNotExistError
from app.Modules.Auth.Exceptions.UsernameFormatError import UsernameFormatError
from app.Modules.Auth.Exceptions.PasswordFormatError import PasswordFormatError

from app.Config import Config
from app.Utils import PassUtil

def Register(username: str, password: str) -> bool:
    '''
    注册处理，加密存储到数据库

    @return 是否成功注册
    '''
    userDao = UserDAO()
    if not userDao.queryUser(username) == None:
        raise(UserExistError(username))
    elif len(username) < Config.UserNameMinLength or len(username) >= Config.UserNameMaxLength:
        raise(UsernameFormatError(username))
    elif len(password) < Config.PassWordMinLength or len(password) >= Config.PassWordMaxLength:
        raise(PasswordFormatError())
    else:
        return userDao.insertUser(username, password)

def Login(username: str, password: str, expiration: int = 0) -> bool:
    '''
    登录处理，加密后判断与数据库一致

    @param `expiration` token 过期事件，为 0 则默认时间为 Config.Def_Expiration

    @return 是否成功注册
    '''
    if not expiration > 0:
        expiration = Config.Def_Expiration

    userDao = UserDAO()
    if userDao.queryUser(username) == None:
        raise(UserNotExistError(username))
    ok = userDao.checkUserPassword(username, password)

    if ok:
        # 更新 Redis Token
        token = PassUtil.generate_token(username, expiration)
        tokenDao = TokenDAO()
        tokenDao.removeToken(username=username)
        if tokenDao.addToken(username=username, token=token, ex=expiration):
            return True, token
        else:
            return False, ''
    else:
        return False, ''