from app.database.dao.UserDao import UserDao
from app.database.dao.TokenDao import TokenDao

from app.controller.auth.exception.UserExistError import UserExistError
from app.controller.auth.exception.UserNotExistError import UserNotExistError
from app.controller.auth.exception.UsernameFormatError import UsernameFormatError
from app.controller.auth.exception.PasswordFormatError import PasswordFormatError

from app.config import Config
from app.util import PassUtil

def Register(username: str, password: str) -> bool:
    '''
    注册处理，加密存储到数据库

    @return 是否成功注册
    '''
    userDao = UserDao()
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

    @param `expiration` token 过期事件，为 0 则默认时间为 config.Def_Expiration

    @return 是否成功注册
    '''
    if not expiration > 0:
        expiration = Config.Def_Expiration

    userDao = UserDao()
    if userDao.queryUser(username) == None:
        raise(UserNotExistError(username))
    ok = userDao.checkUserPassword(username, password)

    if ok:
        # 更新 Redis Token
        token = PassUtil.generate_token(username, expiration)
        tokenDao = TokenDao()
        tokenDao.removeToken(username=username)
        if tokenDao.addToken(username=username, token=token):
            return True, token
        else:
            return False, ''
    else:
        return False, ''
    
def Logout(username: str) -> bool:
    '''
    用户注销处理

    @param `username`

    @return 注销是否成功
    '''
    tokenDao = TokenDao()
    return tokenDao.removeToken(username)