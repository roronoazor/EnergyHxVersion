from PyQt5 import QtCore, QtGui, QtWidgets
from pathlib import Path
from pprint import pprint
import json

from Dashboard import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow):
    close_app = QtCore.pyqtSignal()

    def __init__(self, *args, data={'rooms': {}, 'retrofit':{}},
                file_name='', **kwargs):

        super(MainWindow, self).__init__(*args, **kwargs)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self, data=data, file_name=file_name)

        self.projects_path = str(Path.cwd() / 'created_projects')

        self.create_new = False
        self.open_new = False

        # Connect Signals And Slots
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionOpen_Project.triggered.connect(self.open_project)
        self.ui.actionNew_Project.triggered.connect(self.new_project)
        self.ui.actionSave_Project.triggered.connect(self.save_project)
    
    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        msg = 'Are you sure you want close this project?'

        dlg = QtWidgets.QMessageBox.warning(
            self.ui.centralwidget, 'Close Project', msg,
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )

        if dlg == QtWidgets.QMessageBox.Yes:
            print('Exiting')
            if self.create_new:
                new_window = MainWindow()
                new_window.close_app.connect(self.close_app.emit)
            elif self.open_new:
                new_window = MainWindow(
                    data=self.open_data, file_name=self.open_name
                )
                new_window.close_app.connect(self.close_app.emit)
            else:
                self.close_app.emit()
            return super().closeEvent(event)
        
        self.create_new = False
        event.ignore()
        print('Cancelled exit')
    
    def save_project(self, new=False):
        try:
            if not self.ui.file_name or new:
                file_name, _ = QtWidgets.QFileDialog.getSaveFileName(
                    self.ui.centralwidget,'Select File',
                    self.projects_path, 'JSON(*.json)'
                )

                if not file_name:
                    return
            
            file_name = Path(file_name)
            self.ui.file_name = file_name.name
            file = file_name.open('w')
            self.ui.saved_data['rooms'] = self.ui.rooms
            self.ui.saved_data['retrofit'] = self.ui.retrofit_details
            json.dump(self.ui.saved_data, file, indent=2)
            
            msg = f'Saved {self.ui.file_name} successfully'
        except Exception as e:
            msg = f'Error {type(e)} encountered when saving'
        finally:
            self.ui.statusbar.showMessage(msg, 2000)
    
    def new_project(self):
        self.create_new = True
        self.close()
    
    def open_project(self):
        try:
            file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
                self.ui.centralwidget,'Select File',
                self.projects_path, 'JSON(*.json)'
            )

            if not file_name:
                return
            
            file_name = Path(file_name)
            file = file_name.open()
            self.open_data = data = json.load(file)
            self.open_name = file_name.name
            self.open_new = True

            self.close()

            pprint(data)
            msg = 'Successful'
        except Exception as e:
            msg = f'Error {type(e)} encountered when saving'
        finally:
            self.ui.statusbar.showMessage(msg, 2000)
