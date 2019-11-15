from flask.app import Flask


def register_note_module_blue(app: Flask):
    """
    注册 Note 模块的蓝图
    """
    from app.controller.note.ImgBlue import register_blue_Img

    register_blue_Img(app)


def register_file_module_blue(app: Flask):
    """
    注册 File 模块的蓝图
    """
    from app.controller.file.FileBlue import register_blue_File
    from app.controller.file.FileClassBlue import register_blue_FileClass

    register_blue_File(app)
    register_blue_FileClass(app)


#################################################################################################################################################################################################
#################################################################################################################################################################################################
#################################################################################################################################################################################################

def forward_note_error(error: TypeError):
    """
    转发 Note 模块的错误
    """
    from app.controller.note.ErrorHandler import register_note_error_handler
    return register_note_error_handler(error)


def forward_file_error(error: TypeError):
    """
    转发 File 模块的错误
    """
    from app.controller.file.ErrorHandler import register_file_error_handler
    return register_file_error_handler(error)
