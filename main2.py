import sys

import os

from PyQt5 import QtCore, QtGui, QtWidgets, uic

from PyQt5.QtWidgets import QApplication, QMainWindow

from PyQt5.Qt import *

import one, two, three

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


b = 0


def counter(fu):
    def inner(*a, **kw):
        inner.count += 1
        return fu(*a, **kw)

    inner.count = 0
    return inner


@counter
def test():
    pass

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('one.ui', self)
        self.pushButton.clicked.connect(self.NovieOkno_1)

    def NovieOkno_1(self):
        global EnergoTarif
        global komnati
        EnergoTarif = self.spinBox_EnergoTarif.value()
        komnati = self.spinBox_komnati.value()
        self.close()
        self.SecondWindow = SecondWindow()
        self.SecondWindow.show()


class SecondWindow(QMainWindow, QtWidgets.QListWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('two.ui', self)
        self.label_komnati.setText(str(test.count + 1))
        self.pushButton_Dalee.clicked.connect(self.NovieOkno_2)

        self.listWidget_vsego.setDragDropMode(self.DragDrop)
        self.listWidget_vsego.setSelectionMode(self.ExtendedSelection)
        self.listWidget_vsego.setAcceptDrops(False)

        self.listWidget_vkomnate.setDragDropMode(self.DragDrop)
        self.listWidget_vkomnate.setSelectionMode(self.ExtendedSelection)
        self.listWidget_vkomnate.setAcceptDrops(True)

        for text in ['1.Люстра', '2.Светильник', '3.Телевизор','4.Холодильник', '5.Сплит (Если исп.)', '6.Стиральная машина','7.Посудомоечная м.', '8.Электро-плита', '9.Микроволновка','10.Компьютер', '11.Чайник', '12.Духовка', '13.Вытяжка', '14.Кофемашина', '15.Утюг','16.Фен']:
            self.listWidget_vsego.addItem(text)

    def NovieOkno_2(self, list_item):
        kostil2 = test.count + 1
        if kostil2 < komnati:
            test()
            list_item = [self.listWidget_vkomnate.item(row).text() for row in range(self.listWidget_vkomnate.count())]
            self.close()
            self.SecondWindow = SecondWindow()
            self.SecondWindow.show()
            ThirdWindow().CalcElectro(list_item)
        else:
            list_item = [self.listWidget_vkomnate.item(row).text() for row in range(self.listWidget_vkomnate.count())]
            self.Two_OneWindow = Two_OneWindow()
            self.Two_OneWindow.show()
            self.close()
            test()
            ThirdWindow().CalcElectro(list_item)
        return list_item

    def dropEvent(self, event):
        if event.source() == self:
            event.setDropAction(QtCore.Qt.MoveAction)
            QtWidgets.QListWidget.dropEvent(self, event)
        elif isinstance(event.source(), QtWidgets.QTreeWidget):
            item = self.itemAt(event.pos())
            row = self.row(item) if item else self.count()
            ba = event.mimeData().data('application/x-qabstractitemmodeldatalist')
            data_items = decode_data(ba)
            for i, data_item in enumerate(data_items):
                it = QtWidgets.QListWidgetItem()
                self.insertItem(row + i, it)
                for r, v in data_item.items():
                    it.setData(r, v)

class Two_OneWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('two_one.ui', self)
        self.pushButton_OK.clicked.connect(self.NovieOkno_2_1)

    def NovieOkno_2_1(self):
        self.close()
        self.ThirdWindow = ThirdWindow()
        self.ThirdWindow.show()

class ThirdWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('three.ui', self)
        self.pushButton_OK.clicked.connect(self.NovieOkno_3)
        self.label_2.setText(str(b))
        if (test.count + 1) > komnati:
            self.label_4.setText(str(b))
            self.label_MonthCost.setText(str(b * float(EnergoTarif)))

    def CalcElectro(self, list_item):
        aa = 0
        vsego = 0
        spisok = [8, 11.25, 8.1, 55, 280.8, 45.5, 22, 38.5, 13, 37.5, 31, 8, 4.5, 8, 7.5, 21]
        for i in range(len(list_item)):
            if str(list_item[aa][1]) == '0' or str(list_item[aa][1]) == '1' or str(list_item[aa][1]) == '2' or str(list_item[aa][1]) == '3' or str(list_item[aa][1]) == '4' or str(list_item[aa][1]) == '5' or str(list_item[aa][1]) == '6':
                vsego = vsego + spisok[int("".join([list_item[aa][0], list_item[aa][1]])) - 1]
            else:
                vsego = vsego + spisok[int(list_item[aa][0]) - 1]
            aa = + 1
        x = float(ThirdWindow().GetZnach())
        global b
        b = x + vsego
        self.ThirdWindow = ThirdWindow()
        self.ThirdWindow.show()
        self.close()
        return b

    def GetZnach(self):
        Znach = self.label_2.text()
        return Znach

    def NovieOkno_3(self):
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mp = MainWindow()
    mp.show()
    sys.exit(app.exec())