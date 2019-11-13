from flask.app import Flask


def register_note_module_blue(app: Flask):
    """
    注册 Note 模块的蓝图
    """
    from app.controller.note.NoteBlue import register_blue_Note
    from app.controller.note.GroupBlue import register_blue_Group
    from app.controller.note.ImgBlue import register_blue_Img

    register_blue_Note(app)
    register_blue_Group(app)
    register_blue_Img(app)


def register_star_module_blue(app: Flask):
    """
    注册 Star 模块的蓝图
    """
    from app.controller.star.StarBlue import register_blue_Star

    register_blue_Star(app)


def register_schedule_module_blue(app: Flask):
    """
    注册 Schedule 模块的蓝图
    """
    from app.controller.schedule.ScheduleBlue import register_blue_Schedule

    register_blue_Schedule(app)


def register_file_module_blue(app: Flask):
    """
    注册 File 模块的蓝图
    """
    from app.controller.file.FileBlue import register_blue_File
    from app.controller.file.FileClassBlue import register_blue_FileClass

    register_blue_File(app)
    register_blue_FileClass(app)


def register_auth_module_blue(app: Flask):
    """
    注册 Auth 模块的蓝图
    """
    from app.controller.auth.AuthBlue import register_blue_Auth

    register_blue_Auth(app)


#################################################################################################################################################################################################
#################################################################################################################################################################################################
#################################################################################################################################################################################################

def forward_note_error(error: TypeError):
    """
    转发 Note 模块的错误
    """
    from app.controller.note.ErrorHandler import register_note_error_handler
    return register_note_error_handler(error)


def forward_star_error(error: TypeError):
    """
    转发 Star 模块的错误
    """
    from app.controller.star.ErrorHandler import register_star_error_handler
    return register_star_error_handler(error)


def forward_schedule_error(error: TypeError):
    """
    转发 Schedule 模块的错误
    """
    from app.controller.schedule.ErrorHandler import register_schedule_error_handler
    return register_schedule_error_handler(error)


def forward_file_error(error: TypeError):
    """
    转发 File 模块的错误
    """
    from app.controller.file.ErrorHandler import register_file_error_handler
    return register_file_error_handler(error)


def forward_auth_error(error: TypeError):
    """
    转发 Auth 模块的错误
    """
    from app.controller.auth.ErrorHandler import register_auth_error_handler

    return register_auth_error_handler(error)
