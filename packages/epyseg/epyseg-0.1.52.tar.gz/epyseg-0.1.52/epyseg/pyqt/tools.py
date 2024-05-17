from epyseg.settings.global_settings import set_UI # set the UI to be used py qtpy
set_UI()
from qtpy.QtGui import QPainter

# return true if antialiasing is on
def check_antialiasing(painter):
    # print('testing antialias', painter.testRenderHint(QPainter.Antialiasing))
    return painter.testRenderHint(QPainter.Antialiasing)

def get_items_of_combo(combo_box):
    items = [combo_box.itemText(i) for i in range(combo_box.count())]
    return items
