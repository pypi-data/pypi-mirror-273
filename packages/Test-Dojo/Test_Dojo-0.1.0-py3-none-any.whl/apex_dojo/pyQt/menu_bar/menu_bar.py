from dataclasses import dataclass

from PyQt5 import QtCore, QtGui, QtWidgets


@dataclass
class UiMainWindow(object):
    def __init__(self):
        self.actionSave = None
        self.actionPaste = None
        self.actionCopy = None
        self.actionNew = None
        self.statusbar = None
        self.menuEdit = None
        self.menuFile = None
        self.menubar = None
        self.label = None
        self.central_widget = None

    def setup_ui(self, main_window):
        main_window.setObjectName("MainWindow")
        main_window.resize(700, 400)
        self.central_widget = QtWidgets.QWidget(main_window)
        self.central_widget.setObjectName("central_widget")
        self.label = QtWidgets.QLabel(self.central_widget)
        self.label.setGeometry(QtCore.QRect(250, 100, 251, 111))

        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(20)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)

        self.label.setFont(font)
        self.label.setStyleSheet("")
        self.label.setObjectName("label")

        main_window.setCentralWidget(self.central_widget)

        self.menubar = QtWidgets.QMenuBar(main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")

        main_window.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")

        main_window.setStatusBar(self.statusbar)

        self.actionNew = QtWidgets.QAction(main_window)
        self.actionNew.setObjectName("actionNew")
        self.actionCopy = QtWidgets.QAction(main_window)
        self.actionCopy.setObjectName("actionCopy")
        self.actionPaste = QtWidgets.QAction(main_window)
        self.actionPaste.setObjectName("actionPaste")
        self.actionSave = QtWidgets.QAction(main_window)
        self.actionSave.setObjectName("actionSave")

        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionSave)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())

        self.re_translate_ui(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

        self.actionNew.triggered.connect(lambda: self.clicked("New was clicked"))
        self.actionSave.triggered.connect(lambda: self.clicked("Save was clicked"))
        self.actionCopy.triggered.connect(lambda: self.clicked("Copy was clicked"))
        self.actionPaste.triggered.connect(lambda: self.clicked("Paste was clicked"))

    def re_translate_ui(self, main_window):
        _translate = QtCore.QCoreApplication.translate

        main_window.setWindowTitle(_translate("MainWindow", "MainWindow"))

        self.label.setText(_translate("MainWindow", "TextLabel"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))

        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionNew.setStatusTip(_translate("MainWindow", "Create a new file"))
        self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N"))

        self.actionCopy.setText(_translate("MainWindow", "Copy"))
        self.actionCopy.setStatusTip(_translate("MainWindow", "Copy a file"))
        self.actionCopy.setShortcut(_translate("MainWindow", "Ctrl+C"))

        self.actionPaste.setText(_translate("MainWindow", "Paste"))
        self.actionPaste.setStatusTip(_translate("MainWindow", "Paste a file"))
        self.actionPaste.setShortcut(_translate("MainWindow", "Ctrl+V"))

        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setStatusTip(_translate("MainWindow", "Save a file"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))

    def clicked(self, text):
        self.label.setText(text)
        self.label.adjustSize()
