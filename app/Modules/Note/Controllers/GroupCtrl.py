from app.Database.GroupDAO import GroupDAO

def test(username: str) -> []:
    groupDao = GroupDAO()
    print(groupDao.queryUserAllNotes(username))
    return [
        {"user" : username},
        {"name" : username},
    ]