from PySide2.QtCore import QFile, QIODevice
from const import stylesheet_path


def get_stylesheet(style_fn):
    try:
        f_style = QFile(str(stylesheet_path / style_fn))
        f_style.open(QIODevice.ReadOnly)
        data = f_style.readAll().data().decode('utf-8')
        f_style.close()
        return data
    except Exception as ex:
        print(ex)
