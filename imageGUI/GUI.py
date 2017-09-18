# from PyQt5.QtWidgets import QMainWindow, QFileDialog, QDialog
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QDialog
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from libImage import do_all
import threading
from time import sleep


class UiSaveDialog(object):
    def setup_ui(self, save_dialog):
        save_dialog.setObjectName("save_dialog")
        save_dialog.resize(311, 293)
        self.gridLayout = QtWidgets.QGridLayout(save_dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.widget = QtWidgets.QWidget(save_dialog)
        self.widget.setObjectName("widget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.separate = QtWidgets.QCheckBox(self.widget)
        self.separate.setObjectName("separate")
        self.gridLayout_2.addWidget(self.separate, 5, 0, 1, 1)
        self.skelet1 = QtWidgets.QCheckBox(self.widget)
        self.skelet1.setObjectName("skelet1")
        self.gridLayout_2.addWidget(self.skelet1, 1, 0, 1, 1)
        self.binarization = QtWidgets.QCheckBox(self.widget)
        self.binarization.setObjectName("binarization")
        self.gridLayout_2.addWidget(self.binarization, 0, 0, 1, 1)
        self.key2 = QtWidgets.QCheckBox(self.widget)
        self.key2.setObjectName("key2")
        self.gridLayout_2.addWidget(self.key2, 4, 0, 1, 1)
        self.skelet2 = QtWidgets.QCheckBox(self.widget)
        self.skelet2.setObjectName("skelet2")
        self.gridLayout_2.addWidget(self.skelet2, 2, 0, 1, 1)
        self.key1 = QtWidgets.QCheckBox(self.widget)
        self.key1.setObjectName("key1")
        self.gridLayout_2.addWidget(self.key1, 3, 0, 1, 1)
        self.edges = QtWidgets.QCheckBox(self.widget)
        self.edges.setObjectName("edges")
        self.gridLayout_2.addWidget(self.edges, 6, 0, 1, 1)
        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(save_dialog)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslate_ui(save_dialog)
        QtCore.QMetaObject.connectSlotsByName(save_dialog)

    def retranslate_ui(self, save_dialog):
        _translate = QtCore.QCoreApplication.translate
        save_dialog.setWindowTitle(_translate("save_dialog", "Сохранять после"))
        self.separate.setText(_translate("save_dialog", "выделения точек изгиба"))
        self.skelet1.setText(_translate("save_dialog", "1 скелетизации"))
        self.binarization.setText(_translate("save_dialog", "бинаризации"))
        self.key2.setText(_translate("save_dialog", "объединения ключевых точек"))
        self.skelet2.setText(_translate("save_dialog", "2 скелетизации"))
        self.key1.setText(_translate("save_dialog", "выделения ключевых точек"))
        self.edges.setText(_translate("save_dialog", "выделения рёбер"))


class UiMainWindow(object):
    def setup_ui(self, main_window):
        main_window.setObjectName("main_window")
        main_window.setEnabled(True)
        main_window.resize(320, 240)
        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.progress = QtWidgets.QProgressBar(self.centralwidget)
        self.progress.setEnabled(False)
        self.progress.setProperty("value", 0)
        self.progress.setObjectName("progress")
        self.gridLayout.addWidget(self.progress, 3, 0, 1, 2)
        self.img = QtWidgets.QLabel(self.centralwidget)
        self.img.setText("")
        self.img.setAlignment(QtCore.Qt.AlignCenter)
        self.img.setObjectName("img")
        self.gridLayout.addWidget(self.img, 1, 0, 1, 2)
        self.filename = QtWidgets.QLabel(self.centralwidget)
        self.filename.setObjectName("filename")
        self.gridLayout.addWidget(self.filename, 0, 0, 1, 1)
        self.filebtn = QtWidgets.QPushButton(self.centralwidget)
        self.filebtn.setObjectName("filebtn")
        self.gridLayout.addWidget(self.filebtn, 0, 1, 1, 1)
        self.output = QtWidgets.QLineEdit(self.centralwidget)
        self.output.setReadOnly(True)
        self.output.setObjectName("output")
        self.gridLayout.addWidget(self.output, 4, 0, 1, 2)
        self.startbtn = QtWidgets.QPushButton(self.centralwidget)
        self.startbtn.setEnabled(False)
        self.startbtn.setObjectName("startbtn")
        self.gridLayout.addWidget(self.startbtn, 2, 0, 1, 1)
        self.setbtn = QtWidgets.QPushButton(self.centralwidget)
        self.setbtn.setObjectName("setbtn")
        self.gridLayout.addWidget(self.setbtn, 2, 1, 1, 1)
        main_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)

        self.retranslate_ui(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslate_ui(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "Распознаватель изображений"))
        self.filename.setText(_translate("main_window", "Выберите файл"))
        self.filebtn.setText(_translate("main_window", "Обзор"))
        self.output.setText(_translate("main_window", "Здесь будет распознанный текст"))
        self.startbtn.setText(_translate("main_window", "Начать"))
        self.setbtn.setText(_translate("main_window", "Настройки"))


class ends():
     sig = QtCore.pyqtSignal()


# noinspection PyUnresolvedReferences
class Ui(QMainWindow, UiMainWindow):
    valarr = {"binarization": False, "skelet1": False, "skelet2": False, "key1": False, "key2": False,
              "separate": False, "edges": True}
    endsignal = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setup_ui(self)
        self.filebtn.clicked.connect(self.file_select)
        self.setbtn.clicked.connect(self.settings)
        self.startbtn.clicked.connect(self.start_processing)
        self.setWindowIcon(QIcon("icon.png"))
        # self.endsignal = QtCore.pyqtSignal()
        self.endsignal.connect(self.end_processing)
        self.show()

    def file_select(self):
        self.progress.setEnabled(False)
        self.progress.setValue(0)
        file = QFileDialog.getOpenFileName(self, "Выбрать файл", "/home/ilya/картинки/", "Изображение (*.png)")[0]
        if file == "":
            self.startbtn.setEnabled(False)
            self.img.setPixmap(QPixmap())
            self.filename.setText("Выберите файл")
        else:
            pixmap = QPixmap(file)
            pixmap = pixmap.scaled(int((pixmap.width() / pixmap.height()) * 250), 250)
            print(type(pixmap))
            self.img.setPixmap(pixmap)
            self.filename.setText(file)
            self.startbtn.setEnabled(True)

    def settings(self):
        dlg = Setd(self.valarr.copy())
        if dlg.exec_() == 1:
            self.valarr = dlg.get_values()
        print(self.valarr)

    def start_processing(self):
        self.progress.setValue(0)
        self.progress.setEnabled(True)
        self.startbtn.setEnabled(False)
        self.setbtn.setEnabled(False)
        self.filebtn.setEnabled(False)
        self.thr = threading.Thread(target=do_all, args=(self.filename.text(), self, self.valarr))
        self.thr.start()

    def end_processing(self):
        while self.thr.is_alive():
            self.thr.join()
        self.startbtn.setEnabled(True)
        self.setbtn.setEnabled(True)
        self.filebtn.setEnabled(True)

    def send_end(self):
        self.endsignal.emit()

# noinspection PyUnresolvedReferences
class Setd(QDialog, UiSaveDialog):
    def __init__(self, valarr, parent=None):
        QDialog.__init__(self, parent)
        self.setup_ui(self)
        self.valarr = valarr
        self.binarization.setChecked(self.valarr["binarization"])
        self.skelet1.setChecked(self.valarr["skelet1"])
        self.skelet2.setChecked(self.valarr["skelet2"])
        self.key1.setChecked(self.valarr["key1"])
        self.key2.setChecked(self.valarr["key2"])
        self.separate.setChecked(self.valarr["separate"])
        self.edges.setChecked(self.valarr["edges"])

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.binarization.stateChanged.connect(self.change_value)
        self.skelet1.stateChanged.connect(self.change_value)
        self.skelet2.stateChanged.connect(self.change_value)
        self.key1.stateChanged.connect(self.change_value)
        self.key2.stateChanged.connect(self.change_value)
        self.separate.stateChanged.connect(self.change_value)
        self.edges.stateChanged.connect(self.change_value)

    def get_values(self):
        return self.valarr

    def change_value(self, state):
        name = self.sender()
        self.valarr[name.objectName()] = bool(state)
