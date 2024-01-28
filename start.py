from PyQt5 import QtCore, QtGui, QtWidgets
from pathlib import Path
from mainboard import MainWindow as ui_mainwindow
import resource
import Dashboard
import json
from pprint import pprint
import time

class Ui_MainWindow(object):
    def setupUi(self, MainWindow: QtWidgets.QMainWindow):
        self.main_window = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(500, 400)
        MainWindow.setMaximumSize(480, 400)
        MainWindow.setMinimumSize(480, 400)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        verticalLayoutWidget.setGeometry(QtCore.QRect(10, 30, 461, 331))
        verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        
        layout = QtWidgets.QVBoxLayout(verticalLayoutWidget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setObjectName("verticalLayout")
        
        label = QtWidgets.QLabel(verticalLayoutWidget)
        label.setMinimumSize(QtCore.QSize(40, 30))
        label.setMaximumSize(QtCore.QSize(100, 150))
        label.setPixmap(QtGui.QPixmap(":/icons/icons/mechanics.png"))
        label.setScaledContents(True)
        label.setObjectName("label")
        layout.addWidget(label, 0, QtCore.Qt.AlignHCenter)

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        layout.addItem(spacerItem)

        font = QtGui.QFont()
        font.setFamily("Yu Gothic Medium")
        font.setPointSize(10)

        label = QtWidgets.QLabel(
            '<html><head/><body><p align=\"center\"><span style=\"'
            ' font-weight:600;\">WELCOME TO ENERGHX PLUS 3.0</span>'
            '</p></body></html>',
            verticalLayoutWidget)
        label.setFont(font)
        label.setScaledContents(False)
        label.setWordWrap(True)
        label.setOpenExternalLinks(False)
        label.setObjectName("label_2")
        layout.addWidget(label)
        
        line = QtWidgets.QFrame(verticalLayoutWidget)
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        line.setObjectName("line")
        layout.addWidget(line)

        font = QtGui.QFont()
        font.setFamily("Yu Gothic Medium")
        font.setPointSize(10)

        label = QtWidgets.QLabel(
            '<html><head/><body><p align=\"center\">'
            'The software is to help audit appliance, '
            'determine the power required for a installing a '
            'renewable energy (wind energy or solar energy) source on site,'
            ' determine the energy required from a battery to power an electric'
            ' vehicle and optimize energy consuming systems.</p></body></html>',
            verticalLayoutWidget)
        label.setMinimumSize(QtCore.QSize(400, 100))
        label.setMaximumSize(QtCore.QSize(16777215, 100))
        label.setFont(font)
        label.setWordWrap(True)
        label.setObjectName("label_3")
        layout.addWidget(label)
        
        hLayout = QtWidgets.QHBoxLayout()
        hLayout.setObjectName("horizontalLayout")

        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum
        )
        hLayout.addItem(spacerItem1)

        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setBold(True)
        font.setWeight(75)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/new-file.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        
        self.toolButton = QtWidgets.QToolButton(verticalLayoutWidget)
        self.toolButton.setFont(font)
        self.toolButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.toolButton.setIcon(icon)
        self.toolButton.setIconSize(QtCore.QSize(30, 30))
        self.toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolButton.setAutoRaise(True)
        self.toolButton.setObjectName("toolButton")
        hLayout.addWidget(self.toolButton)
        
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        hLayout.addItem(spacerItem2)
        
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setBold(True)
        font.setWeight(75)
        
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/open-folder-outline.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        
        self.toolButton_2 = QtWidgets.QToolButton(verticalLayoutWidget)
        self.toolButton_2.setFont(font)
        self.toolButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.toolButton_2.setIcon(icon1)
        self.toolButton_2.setIconSize(QtCore.QSize(30, 30))
        self.toolButton_2.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolButton_2.setAutoRaise(True)
        self.toolButton_2.setObjectName("toolButton_2")
        hLayout.addWidget(self.toolButton_2)
        
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        hLayout.addItem(spacerItem3)
        layout.addLayout(hLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        # This did not put the window center in all display sizes
        # self.main_window.setGeometry(600, 300, 500, 400)  # this determines the position of the application

        MainWindow.move(
            QtWidgets.QApplication.desktop().rect().center() - MainWindow.rect().center()
        )

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Energhx Plus 3.0"))
        self.toolButton.setText(_translate("MainWindow", "Create Project"))
        self.toolButton_2.setText(_translate("MainWindow", "Open Project"))

        self.toolButton.clicked.connect(lambda x: self.new_project())
        self.toolButton_2.clicked.connect(lambda x: self.open_project())
    
    @QtCore.pyqtSlot()
    def new_project(self):
        print('New Project')
        self.new_project_window()
    
    @QtCore.pyqtSlot()
    def open_project(self):
        print('Open Project')
        file, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.centralwidget, 'Select File',
            str(Path.cwd() / 'created_projects'), 'JSON(*json)'

        )

        if file:
            file = Path(file)
            f = file.open()
            data = json.load(f)
            self.new_project_window(data=data, file_name=file.name)
    
    def new_project_window(self, data={'rooms': {}, 'retrofit':{}}, file_name=''):
        self.dboard_window = ui_mainwindow(data=data, file_name=file_name)
        
        self.main_window.hide()
        self.dboard_window.close_app.connect(self.main_window.show)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    # display the splash screen
    splash_pix = QtGui.QPixmap("icons/pure-white-background-85a2a7fd.resized.jpg")
    splash = QtWidgets.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
    splash.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint|QtCore.Qt.FramelessWindowHint)
    splash.setEnabled(False)

    progressBar = QtWidgets.QProgressBar(splash)
    progressBar.setMaximum(10)
    progressBar.setGeometry(0, splash_pix.height() - 50, splash_pix.width(), 20)

    splash.setStyleSheet(
        '''
        QProgressBar {
            text-align: center;
        }
        '''
    )
    splash.show()
    splash.showMessage("<h1><font color='black'>Energhx Plus 3.0</font><img src='icons/mechanics.resized_70.png'/></h1>", 32 | 132, QtCore.Qt.black)

    for i in range(1, 15):
        progressBar.setValue(i)
        t = time.time()
        while time.time() < t + 0.1:
            app.processEvents()

    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    app.setWindowIcon(QtGui.QIcon("icons/renewable-energy.png"))
    splash.finish(MainWindow)
    sys.exit(app.exec_())

