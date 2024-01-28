import sys, os, json, random

from PyQt5 import QtCore, QtGui, QtWidgets

import resource
from pprint import pprint

from Libraries.ApplianceAudit import ApplianceAudit
from Libraries.SolarPV import SolarPV
from Libraries.WindTurbine import WindTurbine

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import numpy as np
import appliance_popup
import cl_popup

from Libraries.battery_design import BatteryDesign
from Libraries.ElectricCar import ElectricCar


class Ui_MainWindow(QtCore.QObject):
    close_app = QtCore.pyqtSignal()
    new_app = QtCore.pyqtSignal()
    open_app = QtCore.pyqtSignal()
    temp_continue = False
    current_index = 0
    appliances = []

    # know if optimizing data
    optimizing = False

    # the designer for the battery
    battery_design = None

    # focus is not on child window
    focus_on_main_window = True

    def setupUi(self, MainWindow: QtWidgets.QMainWindow, data, file_name=''):

        self.data_pages = {
            'Rooms':
                {'main': 0, 'solar': 0, 'wind': 0, 'battery': 0, "electric_car": 0, 'prev': False, 'next': True,
                 'analyze': False, 'optimize': True},
            'Retrofit Appliances':
                {'main': 1, 'solar': 0, 'wind': 0, 'battery': 0, "electric_car": 0, 'prev': True, 'next': False,
                 'analyze': True, 'optimize': True},
            'Appliance Audit Result':
                {'main': 2, 'solar': 0, 'wind': 0, 'battery': 0, "electric_car": 0, 'prev': True, 'next': True,
                 'analyze': False, 'optimize': True},
            'Cooling Load Analysis':
                {'main': 0, 'solar': 0, 'wind': 0, 'battery': 0, "electric_car": 0, 'prev': True, 'next': True,
                 'analyze': False, 'optimize': True},
            'Result':
                {'main': 3, 'solar': 0, 'wind': 0, 'battery': 0, "electric_car": 0, 'prev': True, 'next': True,
                 'analyze': False, 'optimize': True},
            'Solar PV':
                {'main': 4, 'solar': 0, 'wind': 0, 'battery': 0, "electric_car": 0, 'prev': True, 'next': True,
                 'analyze': True, 'optimize': True},
            'Input2':
                {'main': 4, 'solar': 1, 'wind': 0, 'battery': 0, "electric_car": 0, 'prev': True, 'next': True,
                 'analyze': False, 'optimize': True},
            'Input3':
                {'main': 4, 'solar': 2, 'wind': 0, 'battery': 0, "electric_car": 0, 'prev': True, 'next': False,
                 'analyze': True, 'optimize': True},
            'Result1':
                {'main': 4, 'solar': 3, 'wind': 0, 'battery': 0, "electric_car": 0, 'prev': True, 'next': True,
                 'analyze': False, 'optimize': True},
            'Wind Turbine':
                {'main': 5, 'solar': 3, 'wind': 0, 'battery': 0, "electric_car": 0, 'prev': True, 'next': False,
                 'analyze': True, 'optimize': True},
            'Result2':
                {'main': 5, 'solar': 3, 'wind': 1, 'battery': 0, "electric_car": 0, 'prev': True, 'next': False,
                 'analyze': False, 'optimize': True},
            'FINAL REPORT':
                {'main': 7, 'solar': 3, 'wind': 3, 'battery': 3, "electric_car": 0, 'prev': True, 'next': False,
                 'analyze': False, 'optimize': True},
            "Electric Vehicle Charging Station":
                {'main': 6, 'solar': 3, 'wind': 0, 'battery': 0, "electric_car": 0, 'prev': True, 'next': False,
                 'analyze': True,
                 'optimize': True},
            "Result3":
                {'main': 8, 'solar': 3, 'wind': 1, 'battery': 0, "electric_car": 0, 'prev': True, 'next': False,
                 'analyze': False, 'optimize': True},
            "Battery Design":
                {'main': 9, 'solar': 0, 'wind': 0, 'battery': 0, "electric_car": 0, 'prev': True, 'next': False,
                 'analyze': False, 'optimize': True},
            "Battery Sizing":
                {'main': 9, 'solar': 0, 'wind': 0, 'battery': 0, "electric_car": 0, 'prev': True, 'next': False,
                 'analyze': False, 'optimize': True},
        }

        # Added this
        self.main_window = MainWindow
        self.create_new = False
        ###############################

        self.file_name = file_name
        if data['rooms'] != {}:
            self.rooms = data['rooms']
            self.retrofit_details = data['retrofit']
        else:
            self.rooms = {}
            self.retrofit_details = {}
        self.energy_sources = {'solar_pv': {}, 'wind_turbine': {}, 'battery_sizing': {}}
        self.saved_data = data

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1318, 689)
        
        font = QtGui.QFont()
        font.setPointSize(9)
        MainWindow.setFont(font)

        MAX_VALUE = 1000000000

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.dck_project_structure = QtWidgets.QDockWidget(self.centralwidget)
        self.dck_project_structure.setMinimumSize(QtCore.QSize(250, 479))
        self.dck_project_structure.setMaximumSize(QtCore.QSize(250, 524287))
        self.dck_project_structure.setFloating(False)
        self.dck_project_structure.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.dck_project_structure.setAllowedAreas(
            QtCore.Qt.BottomDockWidgetArea | QtCore.Qt.RightDockWidgetArea | QtCore.Qt.TopDockWidgetArea)
        self.dck_project_structure.setObjectName("dck_project_structure")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tree_project_structure = QtWidgets.QTreeWidget(self.dockWidgetContents)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.tree_project_structure.setFont(font)
        self.tree_project_structure.setFrameShape(QtWidgets.QFrame.Panel)
        self.tree_project_structure.setFrameShadow(QtWidgets.QFrame.Plain)
        self.tree_project_structure.setAutoScroll(True)
        self.tree_project_structure.setAutoScrollMargin(20)
        self.tree_project_structure.setTabKeyNavigation(True)
        self.tree_project_structure.setProperty("showDropIndicator", True)
        self.tree_project_structure.setDragEnabled(False)
        self.tree_project_structure.setAlternatingRowColors(False)
        self.tree_project_structure.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tree_project_structure.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.tree_project_structure.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.tree_project_structure.setWordWrap(True)
        self.tree_project_structure.setHeaderHidden(False)
        self.tree_project_structure.setExpandsOnDoubleClick(True)
        self.tree_project_structure.setObjectName("tree_project_structure")

        # edit start #

        rooms_tree = QtWidgets.QTreeWidgetItem(self.tree_project_structure)
        retro_tree = QtWidgets.QTreeWidgetItem(self.tree_project_structure)
        appliance_audit_tree = QtWidgets.QTreeWidgetItem(self.tree_project_structure)
        cooling_tree = QtWidgets.QTreeWidgetItem(self.tree_project_structure)

        # cooling result widget is a child of cooling tree
        cooling_result = QtWidgets.QTreeWidgetItem(cooling_tree)

        analysis_tree_widget = QtWidgets.QTreeWidgetItem(self.tree_project_structure)
        solar_pv = QtWidgets.QTreeWidgetItem(analysis_tree_widget)
        solar_pv_result = QtWidgets.QTreeWidgetItem(solar_pv)
        wind_pv = QtWidgets.QTreeWidgetItem(analysis_tree_widget)
        wind_pv_result = QtWidgets.QTreeWidgetItem(wind_pv)
        battery_sizing = QtWidgets.QTreeWidgetItem(analysis_tree_widget)
        battery_sizing_result = QtWidgets.QTreeWidgetItem(battery_sizing)
        electric_car_charger = QtWidgets.QTreeWidgetItem(analysis_tree_widget)
        electric_car_charger_result = QtWidgets.QTreeWidgetItem(electric_car_charger)

        final_report_tree_widget = QtWidgets.QTreeWidgetItem(self.tree_project_structure)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/solar-panel (1).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        solar_pv.setIcon(0, icon)

        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/wind-turbine.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        wind_pv.setIcon(0, icon1)

        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/icons/images (3).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        battery_sizing.setIcon(0, icon2)

        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/electric-car.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        electric_car_charger.setIcon(0, icon3)

        # end edit #

        # removed this old QTreeWidget Structure the code was badly written #
        # and not scalable #

        # item_0 = QtWidgets.QTreeWidgetItem(self.tree_project_structure)
        # item_0 = QtWidgets.QTreeWidgetItem(self.tree_project_structure)
        # item_0 = QtWidgets.QTreeWidgetItem(self.tree_project_structure)
        #
        # item_0 = QtWidgets.QTreeWidgetItem(self.tree_project_structure)
        # item_1 = QtWidgets.QTreeWidgetItem(item_0)
        # item_0 = QtWidgets.QTreeWidgetItem(self.tree_project_structure)
        # item_1 = QtWidgets.QTreeWidgetItem(item_0)
        # icon = QtGui.QIcon()
        # icon.addPixmap(QtGui.QPixmap(":/icons/icons/solar-panel (1).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # item_1.setIcon(0, icon)
        # item_2 = QtWidgets.QTreeWidgetItem(item_1)
        # item_1 = QtWidgets.QTreeWidgetItem(item_0)
        # icon1 = QtGui.QIcon()
        # icon1.addPixmap(QtGui.QPixmap(":/icons/icons/wind-turbine.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # item_1.setIcon(0, icon1)
        # item_2 = QtWidgets.QTreeWidgetItem(item_1)
        # item_1 = QtWidgets.QTreeWidgetItem(item_0)
        # icon2 = QtGui.QIcon()
        # icon2.addPixmap(QtGui.QPixmap(":/icons/icons/images (3).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # item_1.setIcon(0, icon2)
        # item_2 = QtWidgets.QTreeWidgetItem(item_1)
        # item_0 = QtWidgets.QTreeWidgetItem(self.tree_project_structure)
        # # electric charge icon
        # item_3 = QtWidgets.QTreeWidgetItem(item_1)
        # item_1 = QtWidgets.QTreeWidgetItem(item_0)
        # icon3 = QtGui.QIcon()
        # icon3.addPixmap(QtGui.QPixmap("icons/electric-car.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # item_3.setIcon(0, icon3)
        # #item_2 = QtWidgets.QTreeWidgetItem(item_1)

        #####################################################

        self.tree_project_structure.header().setVisible(True)
        self.tree_project_structure.header().setDefaultSectionSize(50)
        self.tree_project_structure.header().setHighlightSections(False)
        self.tree_project_structure.header().setSortIndicatorShown(False)
        self.tree_project_structure.header().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.tree_project_structure)
        self.tab_summary_report = QtWidgets.QTabWidget(self.dockWidgetContents)
        self.tab_summary_report.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.tab_summary_report.setTabBarAutoHide(False)
        self.tab_summary_report.setObjectName("tab_summary_report")
        self.tb_summary = QtWidgets.QWidget()
        self.tb_summary.setObjectName("tb_summary")
        self.gridLayout_18 = QtWidgets.QGridLayout(self.tb_summary)
        self.gridLayout_18.setObjectName("gridLayout_18")
        self.txtEd_summary = QtWidgets.QTextEdit(self.tb_summary)
        self.txtEd_summary.setObjectName("txtEd_summary")
        self.gridLayout_18.addWidget(self.txtEd_summary, 0, 0, 1, 1)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/icons/edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tab_summary_report.addTab(self.tb_summary, icon3, "")
        self.verticalLayout.addWidget(self.tab_summary_report)
        self.dck_project_structure.setWidget(self.dockWidgetContents)
        self.horizontalLayout_8.addWidget(self.dck_project_structure)
        self.stacked_main_windows = QtWidgets.QStackedWidget(self.centralwidget)
        self.stacked_main_windows.setObjectName("stacked_main_windows")
        # room stacks #
        self.stk_rooms = QtWidgets.QWidget()
        self.stk_rooms.setObjectName("stk_rooms")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.stk_rooms)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.scrollArea = QtWidgets.QScrollArea(self.stk_rooms)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.Box)
        self.scrollArea.setFrameShadow(QtWidgets.QFrame.Raised)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 245, 550))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lbl_analysis_type = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_analysis_type.setFont(font)
        self.lbl_analysis_type.setObjectName("lbl_analysis_type")
        self.verticalLayout_2.addWidget(self.lbl_analysis_type, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.gbox_rooms_office = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.gbox_rooms_office.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.gbox_rooms_office.setFlat(True)
        self.gbox_rooms_office.setCheckable(False)
        self.gbox_rooms_office.setObjectName("gbox_rooms_office")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.gbox_rooms_office)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_add_office = QtWidgets.QToolButton(self.gbox_rooms_office)
        self.btn_add_office.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/icons/plus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_add_office.setIcon(icon4)
        self.btn_add_office.setIconSize(QtCore.QSize(35, 35))
        self.btn_add_office.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.btn_add_office.setAutoRaise(True)
        self.btn_add_office.setObjectName("btn_add_office")
        self.horizontalLayout.addWidget(self.btn_add_office, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.verticalLayout_2.addWidget(self.gbox_rooms_office, 0, QtCore.Qt.AlignTop)
        self.gbox_rooms_laboratories = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.gbox_rooms_laboratories.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.gbox_rooms_laboratories.setFlat(True)
        self.gbox_rooms_laboratories.setCheckable(False)
        self.gbox_rooms_laboratories.setObjectName("gbox_rooms_laboratories")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.gbox_rooms_laboratories)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.btn_add_laboratory = QtWidgets.QToolButton(self.gbox_rooms_laboratories)
        self.btn_add_laboratory.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.btn_add_laboratory.setIcon(icon4)
        self.btn_add_laboratory.setIconSize(QtCore.QSize(35, 35))
        self.btn_add_laboratory.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.btn_add_laboratory.setAutoRaise(True)
        self.btn_add_laboratory.setObjectName("btn_add_laboratory")
        self.horizontalLayout_4.addWidget(self.btn_add_laboratory, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.verticalLayout_2.addWidget(self.gbox_rooms_laboratories, 0, QtCore.Qt.AlignTop)
        self.gbox_rooms_lecture_room = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.gbox_rooms_lecture_room.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.gbox_rooms_lecture_room.setFlat(True)
        self.gbox_rooms_lecture_room.setCheckable(False)
        self.gbox_rooms_lecture_room.setObjectName("gbox_rooms_lecture_room")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.gbox_rooms_lecture_room)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.btn_add_lecture_room = QtWidgets.QToolButton(self.gbox_rooms_lecture_room)
        self.btn_add_lecture_room.setIcon(icon4)
        self.btn_add_lecture_room.setIconSize(QtCore.QSize(35, 35))
        self.btn_add_lecture_room.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.btn_add_lecture_room.setAutoRaise(True)
        self.btn_add_lecture_room.setObjectName("btn_add_lecture_room")
        self.horizontalLayout_7.addWidget(self.btn_add_lecture_room, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.verticalLayout_2.addWidget(self.gbox_rooms_lecture_room, 0, QtCore.Qt.AlignTop)
        self.gbox_rooms_conference_room = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.gbox_rooms_conference_room.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.gbox_rooms_conference_room.setFlat(True)
        self.gbox_rooms_conference_room.setCheckable(False)
        self.gbox_rooms_conference_room.setObjectName("gbox_rooms_conference_room")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.gbox_rooms_conference_room)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.btn_add_conference_rooms = QtWidgets.QToolButton(self.gbox_rooms_conference_room)
        self.btn_add_conference_rooms.setIcon(icon4)
        self.btn_add_conference_rooms.setIconSize(QtCore.QSize(35, 35))
        self.btn_add_conference_rooms.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.btn_add_conference_rooms.setAutoRaise(True)
        self.btn_add_conference_rooms.setObjectName("btn_add_conference_rooms")
        self.horizontalLayout_6.addWidget(self.btn_add_conference_rooms, 0,
                                          QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.verticalLayout_2.addWidget(self.gbox_rooms_conference_room, 0, QtCore.Qt.AlignTop)
        self.gbox_rooms_others = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.gbox_rooms_others.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.gbox_rooms_others.setFlat(True)
        self.gbox_rooms_others.setCheckable(False)
        self.gbox_rooms_others.setObjectName("gbox_rooms_others")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.gbox_rooms_others)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.btn_add_others = QtWidgets.QToolButton(self.gbox_rooms_others)
        self.btn_add_others.setIcon(icon4)
        self.btn_add_others.setIconSize(QtCore.QSize(35, 35))
        self.btn_add_others.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.btn_add_others.setAutoRaise(True)
        self.btn_add_others.setObjectName("btn_add_others")
        self.horizontalLayout_5.addWidget(self.btn_add_others, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.verticalLayout_2.addWidget(self.gbox_rooms_others, 0, QtCore.Qt.AlignTop)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout_2.addWidget(self.scrollArea)
        self.stacked_main_windows.addWidget(self.stk_rooms)
        self.RetrofitAppliance = QtWidgets.QWidget()
        self.RetrofitAppliance.setObjectName("RetrofitAppliance")
        self.gridLayout_23 = QtWidgets.QGridLayout(self.RetrofitAppliance)
        self.gridLayout_23.setObjectName("gridLayout_23")
        self.scrollArea_7 = QtWidgets.QScrollArea(self.RetrofitAppliance)
        self.scrollArea_7.setWidgetResizable(True)
        self.scrollArea_7.setObjectName("scrollArea_7")
        self.scrollAreaWidgetContents_7 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_7.setGeometry(QtCore.QRect(0, 0, 1024, 572))
        self.scrollAreaWidgetContents_7.setObjectName("scrollAreaWidgetContents_7")
        self.gridLayout_26 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_7)
        self.gridLayout_26.setContentsMargins(100, -1, 100, -1)
        self.gridLayout_26.setObjectName("gridLayout_26")
        self.tlbx_appliances = QtWidgets.QToolBox(self.scrollAreaWidgetContents_7)
        self.tlbx_appliances.setMinimumSize(QtCore.QSize(0, 0))
        self.tlbx_appliances.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tlbx_appliances.setObjectName("tlbx_appliances")
        self.tlbx_app_sample = QtWidgets.QWidget()
        self.tlbx_app_sample.setGeometry(QtCore.QRect(0, 0, 824, 526))
        self.tlbx_app_sample.setObjectName("tlbx_app_sample")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.tlbx_app_sample)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.frame_9 = QtWidgets.QFrame(self.tlbx_app_sample)
        self.frame_9.setMinimumSize(QtCore.QSize(130, 0))
        self.frame_9.setMaximumSize(QtCore.QSize(130, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.frame_9.setFont(font)
        self.frame_9.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_9.setObjectName("frame_9")
        self.verticalLayout_22 = QtWidgets.QVBoxLayout(self.frame_9)
        self.verticalLayout_22.setObjectName("verticalLayout_22")
        self.lbl_appliance_lbl = QtWidgets.QLabel(self.frame_9)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lbl_appliance_lbl.setFont(font)
        self.lbl_appliance_lbl.setObjectName("lbl_appliance_lbl")
        self.verticalLayout_22.addWidget(self.lbl_appliance_lbl, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom)
        self.lbl_appliance_rating = QtWidgets.QLabel(self.frame_9)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(24)
        self.lbl_appliance_rating.setFont(font)
        self.lbl_appliance_rating.setObjectName("lbl_appliance_rating")
        self.verticalLayout_22.addWidget(self.lbl_appliance_rating, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom)
        self.lbl_kw_appliance = QtWidgets.QLabel(self.frame_9)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lbl_kw_appliance.setFont(font)
        self.lbl_kw_appliance.setObjectName("lbl_kw_appliance")
        self.verticalLayout_22.addWidget(self.lbl_kw_appliance, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.horizontalLayout_3.addWidget(self.frame_9)
        self.line_9 = QtWidgets.QFrame(self.tlbx_app_sample)
        self.line_9.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_9.setObjectName("line_9")
        self.horizontalLayout_3.addWidget(self.line_9)
        self.frame_11 = QtWidgets.QFrame(self.tlbx_app_sample)
        self.frame_11.setMinimumSize(QtCore.QSize(130, 0))
        self.frame_11.setMaximumSize(QtCore.QSize(130, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.frame_11.setFont(font)
        self.frame_11.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_11.setObjectName("frame_11")
        self.verticalLayout_23 = QtWidgets.QVBoxLayout(self.frame_11)
        self.verticalLayout_23.setObjectName("verticalLayout_23")
        self.lbl_retrofit_lbl = QtWidgets.QLabel(self.frame_11)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lbl_retrofit_lbl.setFont(font)
        self.lbl_retrofit_lbl.setObjectName("lbl_retrofit_lbl")
        self.verticalLayout_23.addWidget(self.lbl_retrofit_lbl, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom)
        self.lbl_retrofit_rating = QtWidgets.QLabel(self.frame_11)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(24)
        self.lbl_retrofit_rating.setFont(font)
        self.lbl_retrofit_rating.setObjectName("lbl_retrofit_rating")
        self.verticalLayout_23.addWidget(self.lbl_retrofit_rating, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom)
        self.lbl_kw_retrofit = QtWidgets.QLabel(self.frame_11)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lbl_kw_retrofit.setFont(font)
        self.lbl_kw_retrofit.setObjectName("lbl_kw_retrofit")
        self.verticalLayout_23.addWidget(self.lbl_kw_retrofit, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.horizontalLayout_3.addWidget(self.frame_11)
        self.gb_retrofit_appliances = QtWidgets.QGroupBox(self.tlbx_app_sample)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.gb_retrofit_appliances.setFont(font)
        self.gb_retrofit_appliances.setObjectName("gb_retrofit_appliances")
        self.gridLayout_24 = QtWidgets.QGridLayout(self.gb_retrofit_appliances)
        self.gridLayout_24.setContentsMargins(-1, -1, -1, 10)
        self.gridLayout_24.setHorizontalSpacing(8)
        self.gridLayout_24.setVerticalSpacing(4)
        self.gridLayout_24.setObjectName("gridLayout_24")
        self.rd_5star_retrofit = QtWidgets.QRadioButton(self.gb_retrofit_appliances)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/icons/five star.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rd_5star_retrofit.setIcon(icon5)
        self.rd_5star_retrofit.setIconSize(QtCore.QSize(90, 20))
        self.rd_5star_retrofit.setChecked(True)
        self.rd_5star_retrofit.setObjectName("rd_5star_retrofit")
        self.gridLayout_24.addWidget(self.rd_5star_retrofit, 0, 0, 1, 1)
        self.rd_4star_retrofit = QtWidgets.QRadioButton(self.gb_retrofit_appliances)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icons/icons/four star.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rd_4star_retrofit.setIcon(icon6)
        self.rd_4star_retrofit.setIconSize(QtCore.QSize(90, 20))
        self.rd_4star_retrofit.setObjectName("rd_4star_retrofit")
        self.gridLayout_24.addWidget(self.rd_4star_retrofit, 1, 0, 1, 1)
        self.rd_3star_retrofit = QtWidgets.QRadioButton(self.gb_retrofit_appliances)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icons/icons/three star.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rd_3star_retrofit.setIcon(icon7)
        self.rd_3star_retrofit.setIconSize(QtCore.QSize(90, 16))
        self.rd_3star_retrofit.setObjectName("rd_3star_retrofit")
        self.gridLayout_24.addWidget(self.rd_3star_retrofit, 2, 0, 1, 1)
        self.rd_2star_retrofit = QtWidgets.QRadioButton(self.gb_retrofit_appliances)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/icons/icons/two star.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rd_2star_retrofit.setIcon(icon8)
        self.rd_2star_retrofit.setIconSize(QtCore.QSize(90, 20))
        self.rd_2star_retrofit.setObjectName("rd_2star_retrofit")
        self.gridLayout_24.addWidget(self.rd_2star_retrofit, 3, 0, 1, 1)
        self.rd_1star_retrofi = QtWidgets.QRadioButton(self.gb_retrofit_appliances)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/icons/icons/one star.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rd_1star_retrofi.setIcon(icon9)
        self.rd_1star_retrofi.setIconSize(QtCore.QSize(90, 20))
        self.rd_1star_retrofi.setObjectName("rd_1star_retrofi")
        self.gridLayout_24.addWidget(self.rd_1star_retrofi, 4, 0, 1, 1)
        self.horizontalLayout_3.addWidget(self.gb_retrofit_appliances)
        self.tlbx_appliances.addItem(self.tlbx_app_sample, "")
        self.gridLayout_26.addWidget(self.tlbx_appliances, 0, 0, 1, 1)
        self.scrollArea_7.setWidget(self.scrollAreaWidgetContents_7)
        self.gridLayout_23.addWidget(self.scrollArea_7, 0, 0, 1, 1)
        self.stacked_main_windows.addWidget(self.RetrofitAppliance)
        self.stk_load_summary = QtWidgets.QWidget()
        self.stk_load_summary.setObjectName("stk_load_summary")
        self.gridLayout_15 = QtWidgets.QGridLayout(self.stk_load_summary)
        self.gridLayout_15.setObjectName("gridLayout_15")
        self.scrollArea_6 = QtWidgets.QScrollArea(self.stk_load_summary)
        self.scrollArea_6.setWidgetResizable(True)
        self.scrollArea_6.setObjectName("scrollArea_6")
        self.scrollAreaWidgetContents_6 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_6.setGeometry(QtCore.QRect(0, 0, 1024, 572))
        self.scrollAreaWidgetContents_6.setObjectName("scrollAreaWidgetContents_6")
        self.gridLayout_16 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_6)
        self.gridLayout_16.setObjectName("gridLayout_16")
        self.groupBox_21 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_6)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_21.setFont(font)
        self.groupBox_21.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_21.setFlat(True)
        self.groupBox_21.setObjectName("groupBox_21")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_21)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.plText_summary_aa_report = QtWidgets.QPlainTextEdit(self.groupBox_21)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.plText_summary_aa_report.setFont(font)
        self.plText_summary_aa_report.setObjectName("plText_summary_aa_report")
        self.verticalLayout_4.addWidget(self.plText_summary_aa_report)
        self.wid_summary_aa_graph = QtWidgets.QWidget(self.groupBox_21)
        self.wid_summary_aa_graph.setMinimumSize(QtCore.QSize(0, 300))
        self.wid_summary_aa_graph.setMaximumSize(QtCore.QSize(16777215, 300))
        self.wid_summary_aa_graph.setObjectName("wid_summary_aa_graph")
        self.verticalLayout_4.addWidget(self.wid_summary_aa_graph)
        self.gridLayout_16.addWidget(self.groupBox_21, 1, 1, 2, 1)
        self.tbl_summary_aa_audit = QtWidgets.QTableWidget(self.scrollAreaWidgetContents_6)
        self.tbl_summary_aa_audit.setMinimumSize(QtCore.QSize(550, 0))
        self.tbl_summary_aa_audit.setMaximumSize(QtCore.QSize(550, 16777215))
        self.tbl_summary_aa_audit.setAlternatingRowColors(True)
        self.tbl_summary_aa_audit.setWordWrap(True)
        self.tbl_summary_aa_audit.setObjectName("tbl_summary_aa_audit")
        self.tbl_summary_aa_audit.setColumnCount(6)
        self.tbl_summary_aa_audit.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_summary_aa_audit.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_summary_aa_audit.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_summary_aa_audit.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_summary_aa_audit.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_summary_aa_audit.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_summary_aa_audit.setHorizontalHeaderItem(5, item)
        self.tbl_summary_aa_audit.horizontalHeader().setCascadingSectionResizes(False)
        self.tbl_summary_aa_audit.horizontalHeader().setDefaultSectionSize(89)
        self.tbl_summary_aa_audit.horizontalHeader().setStretchLastSection(True)
        self.gridLayout_16.addWidget(self.tbl_summary_aa_audit, 2, 0, 1, 1)
        self.scrollArea_6.setWidget(self.scrollAreaWidgetContents_6)
        self.gridLayout_15.addWidget(self.scrollArea_6, 0, 0, 1, 1)
        self.stacked_main_windows.addWidget(self.stk_load_summary)
        self.stk_cl_summary = QtWidgets.QWidget()
        self.stk_cl_summary.setObjectName("stk_cl_summary")
        self.gridLayout_27 = QtWidgets.QGridLayout(self.stk_cl_summary)
        self.gridLayout_27.setObjectName("gridLayout_27")
        self.wid_summary_cl_graph = QtWidgets.QFrame(self.stk_cl_summary)
        self.wid_summary_cl_graph.setMinimumSize(QtCore.QSize(500, 0))
        self.wid_summary_cl_graph.setMaximumSize(QtCore.QSize(500, 16777215))
        self.wid_summary_cl_graph.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.wid_summary_cl_graph.setFrameShadow(QtWidgets.QFrame.Raised)
        self.wid_summary_cl_graph.setObjectName("wid_summary_cl_graph")
        self.gridLayout_27.addWidget(self.wid_summary_cl_graph, 0, 1, 1, 1)
        self.tbl_summary_cl = QtWidgets.QTableWidget(self.stk_cl_summary)
        self.tbl_summary_cl.setObjectName("tbl_summary_cl")
        self.tbl_summary_cl.setColumnCount(6)
        self.tbl_summary_cl.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_summary_cl.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_summary_cl.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_summary_cl.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_summary_cl.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_summary_cl.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_summary_cl.setHorizontalHeaderItem(5, item)
        self.tbl_summary_cl.horizontalHeader().setDefaultSectionSize(130)
        self.tbl_summary_cl.verticalHeader().setMinimumSectionSize(25)
        self.gridLayout_27.addWidget(self.tbl_summary_cl, 0, 0, 1, 1)
        self.stacked_main_windows.addWidget(self.stk_cl_summary)

        # begin solar pv definition #
        self.stk_solar_pv = QtWidgets.QWidget()
        self.stk_solar_pv.setObjectName("stk_solar_pv")
        self.gridLayout_20 = QtWidgets.QGridLayout(self.stk_solar_pv)
        self.gridLayout_20.setObjectName("gridLayout_20")
        self.horizontalFrame_9 = QtWidgets.QFrame(self.stk_solar_pv)
        self.horizontalFrame_9.setMinimumSize(QtCore.QSize(0, 40))
        self.horizontalFrame_9.setMaximumSize(QtCore.QSize(16777215, 70))
        self.horizontalFrame_9.setObjectName("horizontalFrame_9")
        self.horizontalLayout_21 = QtWidgets.QHBoxLayout(self.horizontalFrame_9)
        self.horizontalLayout_21.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout_21.setContentsMargins(8, 8, -1, -1)
        self.horizontalLayout_21.setSpacing(10)
        self.horizontalLayout_21.setObjectName("horizontalLayout_21")
        self.label_69 = QtWidgets.QLabel(self.horizontalFrame_9)
        self.label_69.setMinimumSize(QtCore.QSize(50, 50))
        self.label_69.setMaximumSize(QtCore.QSize(50, 50))
        self.label_69.setText("")
        self.label_69.setPixmap(QtGui.QPixmap(":/icons/icons/solar-panel (1).png"))
        self.label_69.setScaledContents(True)
        self.label_69.setObjectName("label_69")
        self.horizontalLayout_21.addWidget(self.label_69, 0, QtCore.Qt.AlignRight)
        self.line_4 = QtWidgets.QFrame(self.horizontalFrame_9)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_4.setLineWidth(2)
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setObjectName("line_4")
        self.horizontalLayout_21.addWidget(self.line_4, 0, QtCore.Qt.AlignLeft)
        self.label_70 = QtWidgets.QLabel(self.horizontalFrame_9)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_70.setFont(font)
        self.label_70.setObjectName("label_70")
        self.horizontalLayout_21.addWidget(self.label_70, 0, QtCore.Qt.AlignLeft)  # handles SOLAR PV display

        self.gridLayout_20.addWidget(self.horizontalFrame_9, 0, 0, 1, 1,
                                     QtCore.Qt.AlignLeft)  # handles SOLAR PV display
        self.line_5 = QtWidgets.QFrame(self.stk_solar_pv)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.gridLayout_20.addWidget(self.line_5, 1, 0, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.gridLayout_20.addItem(spacerItem, 2, 1, 1, 1)
        self.stk_solar_pv_main = QtWidgets.QStackedWidget(self.stk_solar_pv)
        self.stk_solar_pv_main.setObjectName("stk_solar_pv_main")
        self.stk_solar_pv_main_input_1 = QtWidgets.QWidget()
        self.stk_solar_pv_main_input_1.setObjectName("stk_solar_pv_main_input_1")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.stk_solar_pv_main_input_1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.scrollArea_2 = QtWidgets.QScrollArea(self.stk_solar_pv_main_input_1)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")

        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 1006, 466))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents_2)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.gb_solar_stdt = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_2)
        self.gb_solar_stdt.setMaximumSize(QtCore.QSize(300, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.gb_solar_stdt.setFont(font)
        self.gb_solar_stdt.setFlat(True)
        self.gb_solar_stdt.setCheckable(False)
        self.gb_solar_stdt.setObjectName("gb_solar_stdt")
        self.gridLayout = QtWidgets.QGridLayout(self.gb_solar_stdt)
        self.gridLayout.setContentsMargins(15, 7, 20, 6)
        self.gridLayout.setHorizontalSpacing(15)
        self.gridLayout.setVerticalSpacing(9)
        self.gridLayout.setObjectName("gridLayout")

        self.label = QtWidgets.QLabel(self.gb_solar_stdt)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.cmbx_solar_stdt_name = QtWidgets.QComboBox(self.gb_solar_stdt)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbx_solar_stdt_name.sizePolicy().hasHeightForWidth())
        self.cmbx_solar_stdt_name.setSizePolicy(sizePolicy)
        self.cmbx_solar_stdt_name.setMaximumSize(QtCore.QSize(180, 23))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.cmbx_solar_stdt_name.setFont(font)
        self.cmbx_solar_stdt_name.setEditable(True)
        self.cmbx_solar_stdt_name.setObjectName("cmbx_solar_stdt_name")
        self.gridLayout.addWidget(self.cmbx_solar_stdt_name, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gb_solar_stdt)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gb_solar_stdt)
        self.label_3.setObjectName("label_3")

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.txt_solar_stdt_site = QtWidgets.QLineEdit(self.gb_solar_stdt)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txt_solar_stdt_site.sizePolicy().hasHeightForWidth())
        self.txt_solar_stdt_site.setSizePolicy(sizePolicy)
        self.txt_solar_stdt_site.setMaximumSize(QtCore.QSize(180, 23))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txt_solar_stdt_site.setFont(font)
        self.txt_solar_stdt_site.setObjectName("txt_solar_stdt_site")
        self.gridLayout.addWidget(self.txt_solar_stdt_site, 2, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gb_solar_stdt)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.txt_solar_stdt_lat = QtWidgets.QLineEdit(self.gb_solar_stdt)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txt_solar_stdt_lat.sizePolicy().hasHeightForWidth())
        self.txt_solar_stdt_lat.setSizePolicy(sizePolicy)
        self.txt_solar_stdt_lat.setMaximumSize(QtCore.QSize(180, 23))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txt_solar_stdt_lat.setFont(font)
        self.txt_solar_stdt_lat.setObjectName("txt_solar_stdt_lat")
        self.gridLayout.addWidget(self.txt_solar_stdt_lat, 3, 1, 1, 1)

        self.label_5 = QtWidgets.QLabel(self.gb_solar_stdt)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.txt_solar_stdt_long = QtWidgets.QLineEdit(self.gb_solar_stdt)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txt_solar_stdt_long.sizePolicy().hasHeightForWidth())
        self.txt_solar_stdt_long.setSizePolicy(sizePolicy)
        self.txt_solar_stdt_long.setMaximumSize(QtCore.QSize(180, 23))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txt_solar_stdt_long.setFont(font)
        self.txt_solar_stdt_long.setObjectName("txt_solar_stdt_long")
        self.gridLayout.addWidget(self.txt_solar_stdt_long, 4, 1, 1, 1)

        self.label_6 = QtWidgets.QLabel(self.gb_solar_stdt)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1)
        self.txt_solar_stdt_elev = QtWidgets.QLineEdit(self.gb_solar_stdt)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txt_solar_stdt_elev.sizePolicy().hasHeightForWidth())
        self.txt_solar_stdt_elev.setSizePolicy(sizePolicy)
        self.txt_solar_stdt_elev.setMaximumSize(QtCore.QSize(180, 23))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txt_solar_stdt_elev.setFont(font)
        self.txt_solar_stdt_elev.setObjectName("txt_solar_stdt_elev")
        self.gridLayout.addWidget(self.txt_solar_stdt_elev, 5, 1, 1, 1)

        self.label_7 = QtWidgets.QLabel(self.gb_solar_stdt)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 6, 0, 1, 1)
        self.spbox_solar_stdt_no_wings = QtWidgets.QSpinBox(self.gb_solar_stdt)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spbox_solar_stdt_no_wings.sizePolicy().hasHeightForWidth())
        self.spbox_solar_stdt_no_wings.setSizePolicy(sizePolicy)
        self.spbox_solar_stdt_no_wings.setMaximumSize(QtCore.QSize(180, 23))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.spbox_solar_stdt_no_wings.setFont(font)
        self.spbox_solar_stdt_no_wings.setObjectName("spbox_solar_stdt_no_wings")
        self.gridLayout.addWidget(self.spbox_solar_stdt_no_wings, 6, 1, 1, 1)

        self.label_15 = QtWidgets.QLabel(self.gb_solar_stdt)
        self.label_15.setObjectName("label_15")
        self.gridLayout.addWidget(self.label_15, 7, 0, 1, 1)
        self.txt_solar_stdt_area = QtWidgets.QLineEdit(self.gb_solar_stdt)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txt_solar_stdt_area.sizePolicy().hasHeightForWidth())
        self.txt_solar_stdt_area.setSizePolicy(sizePolicy)
        self.txt_solar_stdt_area.setMaximumSize(QtCore.QSize(180, 23))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txt_solar_stdt_area.setFont(font)
        self.txt_solar_stdt_area.setObjectName("txt_solar_stdt_area")
        self.gridLayout.addWidget(self.txt_solar_stdt_area, 7, 1, 1, 1)

        self.label_16 = QtWidgets.QLabel(self.gb_solar_stdt)
        self.label_16.setObjectName("label_16")
        self.gridLayout.addWidget(self.label_16, 8, 0, 1, 1)
        self.spbox_solar_stdt_pitch = QtWidgets.QSpinBox(self.gb_solar_stdt)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spbox_solar_stdt_pitch.sizePolicy().hasHeightForWidth())
        self.spbox_solar_stdt_pitch.setSizePolicy(sizePolicy)
        self.spbox_solar_stdt_pitch.setMaximumSize(QtCore.QSize(180, 23))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.spbox_solar_stdt_pitch.setFont(font)
        self.spbox_solar_stdt_pitch.setObjectName("spbox_solar_stdt_pitch")
        self.gridLayout.addWidget(self.spbox_solar_stdt_pitch, 8, 1, 1, 1)
        self.txt_solar_stdt_type = QtWidgets.QLineEdit(self.gb_solar_stdt)
        self.txt_solar_stdt_type.setMaximumSize(QtCore.QSize(180, 23))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txt_solar_stdt_type.setFont(font)
        self.txt_solar_stdt_type.setObjectName("txt_solar_stdt_type")
        self.gridLayout.addWidget(self.txt_solar_stdt_type, 1, 1, 1, 1)
        self.cbox_solar_stdt_save = QtWidgets.QCheckBox(self.gb_solar_stdt)
        self.cbox_solar_stdt_save.setObjectName("cbox_solar_stdt_save")
        self.gridLayout.addWidget(self.cbox_solar_stdt_save, 9, 0, 1, 2, QtCore.Qt.AlignRight)
        self.horizontalLayout_9.addWidget(self.gb_solar_stdt)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem1)
        self.gb_solar_indt = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_2)
        self.gb_solar_indt.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.gb_solar_indt.setFont(font)
        self.gb_solar_indt.setFlat(True)
        self.gb_solar_indt.setObjectName("gb_solar_indt")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gb_solar_indt)
        self.gridLayout_2.setContentsMargins(15, 7, 20, 6)
        self.gridLayout_2.setHorizontalSpacing(15)
        self.gridLayout_2.setVerticalSpacing(9)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.label_17 = QtWidgets.QLabel(self.gb_solar_indt)
        self.label_17.setMaximumSize(QtCore.QSize(130, 16777215))
        self.label_17.setObjectName("label_17")
        self.gridLayout_2.addWidget(self.label_17, 0, 0, 1, 1)
        self.cmbx_solar_indt_name = QtWidgets.QComboBox(self.gb_solar_indt)
        self.cmbx_solar_indt_name.setMaximumSize(QtCore.QSize(180, 23))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.cmbx_solar_indt_name.setFont(font)
        self.cmbx_solar_indt_name.setEditable(True)
        self.cmbx_solar_indt_name.setObjectName("cmbx_solar_indt_name")
        self.gridLayout_2.addWidget(self.cmbx_solar_indt_name, 0, 1, 1, 1)
        self.label_18 = QtWidgets.QLabel(self.gb_solar_indt)
        self.label_18.setMaximumSize(QtCore.QSize(130, 16777215))
        self.label_18.setObjectName("label_18")
        self.gridLayout_2.addWidget(self.label_18, 1, 0, 1, 1)
        self.label_19 = QtWidgets.QLabel(self.gb_solar_indt)
        self.label_19.setMaximumSize(QtCore.QSize(130, 16777215))
        self.label_19.setObjectName("label_19")
        self.gridLayout_2.addWidget(self.label_19, 2, 0, 1, 1)
        self.txt_solar_indt_max_mpptv = QtWidgets.QLineEdit(self.gb_solar_indt)
        self.txt_solar_indt_max_mpptv.setMaximumSize(QtCore.QSize(180, 23))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txt_solar_indt_max_mpptv.setFont(font)
        self.txt_solar_indt_max_mpptv.setObjectName("txt_solar_indt_max_mpptv")
        self.gridLayout_2.addWidget(self.txt_solar_indt_max_mpptv, 2, 1, 1, 1)
        self.label_23 = QtWidgets.QLabel(self.gb_solar_indt)
        self.label_23.setMaximumSize(QtCore.QSize(130, 16777215))
        self.label_23.setObjectName("label_23")
        self.gridLayout_2.addWidget(self.label_23, 3, 0, 1, 1)
        self.txt_solar_indt_eff = QtWidgets.QLineEdit(self.gb_solar_indt)
        self.txt_solar_indt_eff.setMaximumSize(QtCore.QSize(180, 23))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txt_solar_indt_eff.setFont(font)
        self.txt_solar_indt_eff.setObjectName("txt_solar_indt_eff")
        self.gridLayout_2.addWidget(self.txt_solar_indt_eff, 4, 1, 1, 1)
        self.spbox_solar_indt_mppt_units = QtWidgets.QSpinBox(self.gb_solar_indt)
        self.spbox_solar_indt_mppt_units.setMaximumSize(QtCore.QSize(180, 23))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.spbox_solar_indt_mppt_units.setFont(font)
        self.spbox_solar_indt_mppt_units.setObjectName("spbox_solar_indt_mppt_units")
        self.gridLayout_2.addWidget(self.spbox_solar_indt_mppt_units, 3, 1, 1, 1)
        self.label_24 = QtWidgets.QLabel(self.gb_solar_indt)
        self.label_24.setMaximumSize(QtCore.QSize(130, 16777215))
        self.label_24.setObjectName("label_24")
        self.gridLayout_2.addWidget(self.label_24, 4, 0, 1, 1)
        self.label_25 = QtWidgets.QLabel(self.gb_solar_indt)
        self.label_25.setMaximumSize(QtCore.QSize(130, 16777215))
        self.label_25.setObjectName("label_25")
        self.gridLayout_2.addWidget(self.label_25, 5, 0, 1, 1)
        self.txt_solar_indt_mpptv_u = QtWidgets.QLineEdit(self.gb_solar_indt)
        self.txt_solar_indt_mpptv_u.setMaximumSize(QtCore.QSize(180, 23))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txt_solar_indt_mpptv_u.setFont(font)
        self.txt_solar_indt_mpptv_u.setObjectName("txt_solar_indt_mpptv_u")
        self.gridLayout_2.addWidget(self.txt_solar_indt_mpptv_u, 5, 1, 1, 1)
        self.label_26 = QtWidgets.QLabel(self.gb_solar_indt)
        self.label_26.setMaximumSize(QtCore.QSize(130, 16777215))
        self.label_26.setObjectName("label_26")
        self.gridLayout_2.addWidget(self.label_26, 6, 0, 1, 1)

        self.txt_solar_indt_mpptv_l = QtWidgets.QLineEdit(self.gb_solar_indt)
        self.txt_solar_indt_mpptv_l.setMaximumSize(QtCore.QSize(180, 23))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txt_solar_indt_mpptv_l.setFont(font)
        self.txt_solar_indt_mpptv_l.setObjectName("txt_solar_indt_mpptv_l")
        self.gridLayout_2.addWidget(self.txt_solar_indt_mpptv_l, 6, 1, 1, 1)
        self.txt_solar_indt_type = QtWidgets.QLineEdit(self.gb_solar_indt)
        self.txt_solar_indt_type.setMaximumSize(QtCore.QSize(180, 23))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txt_solar_indt_type.setFont(font)
        self.txt_solar_indt_type.setObjectName("txt_solar_indt_type")
        self.gridLayout_2.addWidget(self.txt_solar_indt_type, 1, 1, 1, 1)
        self.cbox_solar_indt_save = QtWidgets.QCheckBox(self.gb_solar_indt)
        self.cbox_solar_indt_save.setObjectName("cbox_solar_indt_save")
        self.gridLayout_2.addWidget(self.cbox_solar_indt_save, 7, 0, 1, 2, QtCore.Qt.AlignRight)
        self.horizontalLayout_9.addWidget(self.gb_solar_indt)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayout_3.addWidget(self.scrollArea_2)
        self.stk_solar_pv_main.addWidget(self.stk_solar_pv_main_input_1)
        self.stk_solar_pv_main_input_2 = QtWidgets.QWidget()
        self.stk_solar_pv_main_input_2.setObjectName("stk_solar_pv_main_input_2")
        self.gridLayout_21 = QtWidgets.QGridLayout(self.stk_solar_pv_main_input_2)
        self.gridLayout_21.setObjectName("gridLayout_21")
        self.scrollArea_3 = QtWidgets.QScrollArea(self.stk_solar_pv_main_input_2)
        self.scrollArea_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea_3.setWidgetResizable(True)
        self.scrollArea_3.setObjectName("scrollArea_3")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 1008, 444))
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents_3)
        self.horizontalLayout_10.setContentsMargins(0, 0, -1, 9)
        self.horizontalLayout_10.setSpacing(13)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.groupBox_9 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_3)
        self.groupBox_9.setObjectName("groupBox_9")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_9)
        self.gridLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.txt_solar_mddt_type = QtWidgets.QLineEdit(self.groupBox_9)
        self.txt_solar_mddt_type.setObjectName("txt_solar_mddt_type")
        self.gridLayout_3.addWidget(self.txt_solar_mddt_type, 1, 1, 1, 1)
        self.txt_solar_mddt_rated_power = QtWidgets.QLineEdit(self.groupBox_9)
        self.txt_solar_mddt_rated_power.setObjectName("txt_solar_mddt_rated_power")
        self.gridLayout_3.addWidget(self.txt_solar_mddt_rated_power, 2, 1, 1, 1)
        self.label_20 = QtWidgets.QLabel(self.groupBox_9)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_20.setFont(font)
        self.label_20.setObjectName("label_20")
        self.gridLayout_3.addWidget(self.label_20, 0, 0, 1, 1)
        self.label_21 = QtWidgets.QLabel(self.groupBox_9)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_21.setFont(font)
        self.label_21.setObjectName("label_21")
        self.gridLayout_3.addWidget(self.label_21, 1, 0, 1, 1)
        self.label_22 = QtWidgets.QLabel(self.groupBox_9)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_22.setFont(font)
        self.label_22.setObjectName("label_22")
        self.gridLayout_3.addWidget(self.label_22, 2, 0, 1, 1)
        self.cmbx_solar_mddt_name = QtWidgets.QComboBox(self.groupBox_9)
        self.cmbx_solar_mddt_name.setEditable(True)
        self.cmbx_solar_mddt_name.setObjectName("cmbx_solar_mddt_name")
        self.gridLayout_3.addWidget(self.cmbx_solar_mddt_name, 0, 1, 1, 1)
        self.label_29 = QtWidgets.QLabel(self.groupBox_9)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_29.setFont(font)
        self.label_29.setObjectName("label_29")
        self.gridLayout_3.addWidget(self.label_29, 5, 0, 1, 1)
        self.label_31 = QtWidgets.QLabel(self.groupBox_9)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_31.setFont(font)
        self.label_31.setObjectName("label_31")
        self.gridLayout_3.addWidget(self.label_31, 7, 0, 1, 1)
        self.label_27 = QtWidgets.QLabel(self.groupBox_9)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_27.setFont(font)
        self.label_27.setObjectName("label_27")
        self.gridLayout_3.addWidget(self.label_27, 3, 0, 1, 1)
        self.label_28 = QtWidgets.QLabel(self.groupBox_9)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_28.setFont(font)
        self.label_28.setObjectName("label_28")
        self.gridLayout_3.addWidget(self.label_28, 4, 0, 1, 1)
        self.txt_solar_mddt_open_circuit_volt = QtWidgets.QLineEdit(self.groupBox_9)
        self.txt_solar_mddt_open_circuit_volt.setObjectName("txt_solar_mddt_open_circuit_volt")
        self.gridLayout_3.addWidget(self.txt_solar_mddt_open_circuit_volt, 5, 1, 1, 1)
        self.label_30 = QtWidgets.QLabel(self.groupBox_9)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_30.setFont(font)
        self.label_30.setObjectName("label_30")
        self.gridLayout_3.addWidget(self.label_30, 6, 0, 1, 1)
        self.label_32 = QtWidgets.QLabel(self.groupBox_9)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_32.setFont(font)
        self.label_32.setObjectName("label_32")
        self.gridLayout_3.addWidget(self.label_32, 8, 0, 1, 1)
        self.txt_solar_mddt_max_pow_volt = QtWidgets.QLineEdit(self.groupBox_9)
        self.txt_solar_mddt_max_pow_volt.setObjectName("txt_solar_mddt_max_pow_volt")
        self.gridLayout_3.addWidget(self.txt_solar_mddt_max_pow_volt, 3, 1, 1, 1)
        self.txt_solar_mddt_max_pow_curr = QtWidgets.QLineEdit(self.groupBox_9)
        self.txt_solar_mddt_max_pow_curr.setObjectName("txt_solar_mddt_max_pow_curr")
        self.gridLayout_3.addWidget(self.txt_solar_mddt_max_pow_curr, 4, 1, 1, 1)
        self.txt_solar_mddt_fuse_rating = QtWidgets.QLineEdit(self.groupBox_9)
        self.txt_solar_mddt_fuse_rating.setObjectName("txt_solar_mddt_fuse_rating")
        self.gridLayout_3.addWidget(self.txt_solar_mddt_fuse_rating, 7, 1, 1, 1)
        self.txt_solar_mddt_max_sys_volt = QtWidgets.QLineEdit(self.groupBox_9)
        self.txt_solar_mddt_max_sys_volt.setObjectName("txt_solar_mddt_max_sys_volt")
        self.gridLayout_3.addWidget(self.txt_solar_mddt_max_sys_volt, 8, 1, 1, 1)
        self.txt_solar_mddt_short_circuit_volt = QtWidgets.QLineEdit(self.groupBox_9)
        self.txt_solar_mddt_short_circuit_volt.setObjectName("txt_solar_mddt_short_circuit_volt")
        self.gridLayout_3.addWidget(self.txt_solar_mddt_short_circuit_volt, 6, 1, 1, 1)
        self.horizontalLayout_10.addWidget(self.groupBox_9)
        spacerItem2 = QtWidgets.QSpacerItem(100, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem2)
        self.line = QtWidgets.QFrame(self.scrollAreaWidgetContents_3)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_10.addWidget(self.line)
        spacerItem3 = QtWidgets.QSpacerItem(100, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem3)
        self.frame_10 = QtWidgets.QFrame(self.scrollAreaWidgetContents_3)
        self.frame_10.setObjectName("frame_10")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.frame_10)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.gbox_solar_mddt_op_temp = QtWidgets.QGroupBox(self.frame_10)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.gbox_solar_mddt_op_temp.setFont(font)
        self.gbox_solar_mddt_op_temp.setFlat(True)
        self.gbox_solar_mddt_op_temp.setObjectName("gbox_solar_mddt_op_temp")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.gbox_solar_mddt_op_temp)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_12 = QtWidgets.QLabel(self.gbox_solar_mddt_op_temp)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.verticalLayout_10.addWidget(self.label_12)
        self.txt_solar_mddt_op_temp_u = QtWidgets.QLineEdit(self.gbox_solar_mddt_op_temp)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txt_solar_mddt_op_temp_u.setFont(font)
        self.txt_solar_mddt_op_temp_u.setObjectName("txt_solar_mddt_op_temp_u")
        self.verticalLayout_10.addWidget(self.txt_solar_mddt_op_temp_u)
        self.label_13 = QtWidgets.QLabel(self.gbox_solar_mddt_op_temp)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.verticalLayout_10.addWidget(self.label_13)
        self.txt_solar_mddt_op_temp_l = QtWidgets.QLineEdit(self.gbox_solar_mddt_op_temp)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txt_solar_mddt_op_temp_l.setFont(font)
        self.txt_solar_mddt_op_temp_l.setObjectName("txt_solar_mddt_op_temp_l")
        self.verticalLayout_10.addWidget(self.txt_solar_mddt_op_temp_l)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_10.addItem(spacerItem4)
        self.gridLayout_9.addWidget(self.gbox_solar_mddt_op_temp, 1, 0, 1, 1)
        self.gbox_solar_mddt_pow_tol = QtWidgets.QGroupBox(self.frame_10)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.gbox_solar_mddt_pow_tol.setFont(font)
        self.gbox_solar_mddt_pow_tol.setFlat(True)
        self.gbox_solar_mddt_pow_tol.setObjectName("gbox_solar_mddt_pow_tol")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.gbox_solar_mddt_pow_tol)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_8 = QtWidgets.QLabel(self.gbox_solar_mddt_pow_tol)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_8.addWidget(self.label_8)
        self.txt_solar_mddt_pow_tol_u = QtWidgets.QLineEdit(self.gbox_solar_mddt_pow_tol)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txt_solar_mddt_pow_tol_u.setFont(font)
        self.txt_solar_mddt_pow_tol_u.setObjectName("txt_solar_mddt_pow_tol_u")
        self.verticalLayout_8.addWidget(self.txt_solar_mddt_pow_tol_u)
        self.label_9 = QtWidgets.QLabel(self.gbox_solar_mddt_pow_tol)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_8.addWidget(self.label_9)
        self.txt_solar_mddt_pow_tol_l = QtWidgets.QLineEdit(self.gbox_solar_mddt_pow_tol)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txt_solar_mddt_pow_tol_l.setFont(font)
        self.txt_solar_mddt_pow_tol_l.setObjectName("txt_solar_mddt_pow_tol_l")
        self.verticalLayout_8.addWidget(self.txt_solar_mddt_pow_tol_l)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_8.addItem(spacerItem5)
        self.gridLayout_9.addWidget(self.gbox_solar_mddt_pow_tol, 0, 0, 1, 1)
        self.horizontalLayout_10.addWidget(self.frame_10)
        spacerItem6 = QtWidgets.QSpacerItem(100, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem6)
        self.line_2 = QtWidgets.QFrame(self.scrollAreaWidgetContents_3)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_10.addWidget(self.line_2)
        spacerItem7 = QtWidgets.QSpacerItem(100, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem7)
        self.frame_13 = QtWidgets.QFrame(self.scrollAreaWidgetContents_3)
        self.frame_13.setObjectName("frame_13")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_13)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.gbox_solar_mddt_temp_coeff = QtWidgets.QGroupBox(self.frame_13)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.gbox_solar_mddt_temp_coeff.setFont(font)
        self.gbox_solar_mddt_temp_coeff.setFlat(True)
        self.gbox_solar_mddt_temp_coeff.setObjectName("gbox_solar_mddt_temp_coeff")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.gbox_solar_mddt_temp_coeff)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.label_41 = QtWidgets.QLabel(self.gbox_solar_mddt_temp_coeff)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_41.setFont(font)
        self.label_41.setObjectName("label_41")
        self.gridLayout_7.addWidget(self.label_41, 0, 0, 1, 1)
        self.txt_solar_mddt_temp_coeff_p = QtWidgets.QLineEdit(self.gbox_solar_mddt_temp_coeff)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txt_solar_mddt_temp_coeff_p.setFont(font)
        self.txt_solar_mddt_temp_coeff_p.setObjectName("txt_solar_mddt_temp_coeff_p")
        self.gridLayout_7.addWidget(self.txt_solar_mddt_temp_coeff_p, 0, 1, 1, 1)
        self.label_42 = QtWidgets.QLabel(self.gbox_solar_mddt_temp_coeff)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_42.setFont(font)
        self.label_42.setObjectName("label_42")
        self.gridLayout_7.addWidget(self.label_42, 1, 0, 1, 1)
        self.txt_solar_mddt_temp_coeff_v = QtWidgets.QLineEdit(self.gbox_solar_mddt_temp_coeff)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txt_solar_mddt_temp_coeff_v.setFont(font)
        self.txt_solar_mddt_temp_coeff_v.setObjectName("txt_solar_mddt_temp_coeff_v")
        self.gridLayout_7.addWidget(self.txt_solar_mddt_temp_coeff_v, 1, 1, 1, 1)
        self.label_43 = QtWidgets.QLabel(self.gbox_solar_mddt_temp_coeff)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_43.setFont(font)
        self.label_43.setObjectName("label_43")
        self.gridLayout_7.addWidget(self.label_43, 2, 0, 1, 1)
        self.txt_solar_mddt_temp_coeff_c = QtWidgets.QLineEdit(self.gbox_solar_mddt_temp_coeff)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txt_solar_mddt_temp_coeff_c.setFont(font)
        self.txt_solar_mddt_temp_coeff_c.setObjectName("txt_solar_mddt_temp_coeff_c")
        self.gridLayout_7.addWidget(self.txt_solar_mddt_temp_coeff_c, 2, 1, 1, 1)
        self.verticalLayout_5.addWidget(self.gbox_solar_mddt_temp_coeff)
        self.gbox_solar_mddt_dim = QtWidgets.QGroupBox(self.frame_13)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.gbox_solar_mddt_dim.setFont(font)
        self.gbox_solar_mddt_dim.setFlat(True)
        self.gbox_solar_mddt_dim.setObjectName("gbox_solar_mddt_dim")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.gbox_solar_mddt_dim)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_36 = QtWidgets.QLabel(self.gbox_solar_mddt_dim)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_36.setFont(font)
        self.label_36.setObjectName("label_36")
        self.gridLayout_5.addWidget(self.label_36, 0, 0, 1, 1)
        self.txt_solar_mddt_dim_l = QtWidgets.QLineEdit(self.gbox_solar_mddt_dim)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txt_solar_mddt_dim_l.setFont(font)
        self.txt_solar_mddt_dim_l.setObjectName("txt_solar_mddt_dim_l")
        self.gridLayout_5.addWidget(self.txt_solar_mddt_dim_l, 0, 1, 1, 1)
        self.label_37 = QtWidgets.QLabel(self.gbox_solar_mddt_dim)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_37.setFont(font)
        self.label_37.setObjectName("label_37")
        self.gridLayout_5.addWidget(self.label_37, 1, 0, 1, 1)
        self.txt_solar_mddt_dim_b = QtWidgets.QLineEdit(self.gbox_solar_mddt_dim)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txt_solar_mddt_dim_b.setFont(font)
        self.txt_solar_mddt_dim_b.setObjectName("txt_solar_mddt_dim_b")
        self.gridLayout_5.addWidget(self.txt_solar_mddt_dim_b, 1, 1, 1, 1)
        self.label_38 = QtWidgets.QLabel(self.gbox_solar_mddt_dim)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_38.setFont(font)
        self.label_38.setObjectName("label_38")
        self.gridLayout_5.addWidget(self.label_38, 2, 0, 1, 1)
        self.txt_solar_mddt_dim_h = QtWidgets.QLineEdit(self.gbox_solar_mddt_dim)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txt_solar_mddt_dim_h.setFont(font)
        self.txt_solar_mddt_dim_h.setObjectName("txt_solar_mddt_dim_h")
        self.gridLayout_5.addWidget(self.txt_solar_mddt_dim_h, 2, 1, 1, 1)
        self.verticalLayout_5.addWidget(self.gbox_solar_mddt_dim)
        self.groupBox_12 = QtWidgets.QGroupBox(self.frame_13)
        self.groupBox_12.setTitle("")
        self.groupBox_12.setFlat(True)
        self.groupBox_12.setObjectName("groupBox_12")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox_12)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.label_39 = QtWidgets.QLabel(self.groupBox_12)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_39.setFont(font)
        self.label_39.setObjectName("label_39")
        self.gridLayout_6.addWidget(self.label_39, 0, 0, 1, 1)
        self.txt_solar_mddt_weight = QtWidgets.QLineEdit(self.groupBox_12)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txt_solar_mddt_weight.setFont(font)
        self.txt_solar_mddt_weight.setObjectName("txt_solar_mddt_weight")
        self.gridLayout_6.addWidget(self.txt_solar_mddt_weight, 0, 1, 1, 1)
        self.label_40 = QtWidgets.QLabel(self.groupBox_12)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_40.setFont(font)
        self.label_40.setObjectName("label_40")
        self.gridLayout_6.addWidget(self.label_40, 1, 0, 1, 1)
        self.txt_solar_mddt_eff = QtWidgets.QLineEdit(self.groupBox_12)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txt_solar_mddt_eff.setFont(font)
        self.txt_solar_mddt_eff.setObjectName("txt_solar_mddt_eff")
        self.gridLayout_6.addWidget(self.txt_solar_mddt_eff, 1, 1, 1, 1)
        self.verticalLayout_5.addWidget(self.groupBox_12)
        self.horizontalLayout_10.addWidget(self.frame_13)
        self.scrollArea_3.setWidget(self.scrollAreaWidgetContents_3)
        self.gridLayout_21.addWidget(self.scrollArea_3, 0, 0, 1, 1)
        self.cbox_solar_mddt_save = QtWidgets.QCheckBox(self.stk_solar_pv_main_input_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.cbox_solar_mddt_save.setFont(font)
        self.cbox_solar_mddt_save.setObjectName("cbox_solar_mddt_save")
        self.gridLayout_21.addWidget(self.cbox_solar_mddt_save, 1, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.stk_solar_pv_main.addWidget(self.stk_solar_pv_main_input_2)
        self.stk_solar_pv_main_input_3 = QtWidgets.QWidget()
        self.stk_solar_pv_main_input_3.setObjectName("stk_solar_pv_main_input_3")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.stk_solar_pv_main_input_3)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.scrollArea_4 = QtWidgets.QScrollArea(self.stk_solar_pv_main_input_3)
        self.scrollArea_4.setWidgetResizable(True)
        self.scrollArea_4.setObjectName("scrollArea_4")
        self.scrollAreaWidgetContents_4 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_4.setGeometry(QtCore.QRect(0, 0, 1006, 466))
        self.scrollAreaWidgetContents_4.setObjectName("scrollAreaWidgetContents_4")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents_4)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.gbox_solar_constants = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_4)
        self.gbox_solar_constants.setMinimumSize(QtCore.QSize(400, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.gbox_solar_constants.setFont(font)
        self.gbox_solar_constants.setObjectName("gbox_solar_constants")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.gbox_solar_constants)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.label_54 = QtWidgets.QLabel(self.gbox_solar_constants)
        self.label_54.setObjectName("label_54")
        self.gridLayout_10.addWidget(self.label_54, 7, 0, 1, 1)
        self.hslider_solar_const_tol = QtWidgets.QSlider(self.gbox_solar_constants)
        self.hslider_solar_const_tol.setMaximumSize(QtCore.QSize(300, 16777215))
        self.hslider_solar_const_tol.setMaximum(100)
        self.hslider_solar_const_tol.setPageStep(5)
        self.hslider_solar_const_tol.setOrientation(QtCore.Qt.Horizontal)
        self.hslider_solar_const_tol.setInvertedAppearance(False)
        self.hslider_solar_const_tol.setInvertedControls(True)
        self.hslider_solar_const_tol.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.hslider_solar_const_tol.setObjectName("hslider_solar_const_tol")
        self.gridLayout_10.addWidget(self.hslider_solar_const_tol, 1, 1, 1, 1)
        self.label_47 = QtWidgets.QLabel(self.gbox_solar_constants)
        self.label_47.setObjectName("label_47")
        self.gridLayout_10.addWidget(self.label_47, 0, 0, 1, 1)
        self.label_51 = QtWidgets.QLabel(self.gbox_solar_constants)
        self.label_51.setObjectName("label_51")
        self.gridLayout_10.addWidget(self.label_51, 4, 0, 1, 1)
        self.dspbox_solar_const_eff_cel_temp = QtWidgets.QDoubleSpinBox(self.gbox_solar_constants)
        self.dspbox_solar_const_eff_cel_temp.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.dspbox_solar_const_eff_cel_temp.setFont(font)
        self.dspbox_solar_const_eff_cel_temp.setObjectName("dspbox_solar_const_eff_cel_temp")
        self.gridLayout_10.addWidget(self.dspbox_solar_const_eff_cel_temp, 7, 1, 1, 1)
        self.hslider_solar_const_temp_effect = QtWidgets.QSlider(self.gbox_solar_constants)
        self.hslider_solar_const_temp_effect.setMaximumSize(QtCore.QSize(300, 16777215))
        self.hslider_solar_const_temp_effect.setMaximum(100)
        self.hslider_solar_const_temp_effect.setPageStep(5)
        self.hslider_solar_const_temp_effect.setOrientation(QtCore.Qt.Horizontal)
        self.hslider_solar_const_temp_effect.setInvertedAppearance(False)
        self.hslider_solar_const_temp_effect.setInvertedControls(True)
        self.hslider_solar_const_temp_effect.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.hslider_solar_const_temp_effect.setObjectName("hslider_solar_const_temp_effect")
        self.gridLayout_10.addWidget(self.hslider_solar_const_temp_effect, 5, 1, 1, 1)
        self.label_48 = QtWidgets.QLabel(self.gbox_solar_constants)
        self.label_48.setObjectName("label_48")
        self.gridLayout_10.addWidget(self.label_48, 1, 0, 1, 1)
        self.label_52 = QtWidgets.QLabel(self.gbox_solar_constants)
        self.label_52.setObjectName("label_52")
        self.gridLayout_10.addWidget(self.label_52, 5, 0, 1, 1)
        self.hslider_solar_const_safety_margin = QtWidgets.QSlider(self.gbox_solar_constants)
        self.hslider_solar_const_safety_margin.setMaximumSize(QtCore.QSize(300, 16777215))
        self.hslider_solar_const_safety_margin.setMaximum(100)
        self.hslider_solar_const_safety_margin.setPageStep(5)
        self.hslider_solar_const_safety_margin.setOrientation(QtCore.Qt.Horizontal)
        self.hslider_solar_const_safety_margin.setInvertedAppearance(False)
        self.hslider_solar_const_safety_margin.setInvertedControls(True)
        self.hslider_solar_const_safety_margin.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.hslider_solar_const_safety_margin.setObjectName("hslider_solar_const_safety_margin")
        self.gridLayout_10.addWidget(self.hslider_solar_const_safety_margin, 6, 1, 1, 1)
        self.hslider_solar_const_dirt_loss = QtWidgets.QSlider(self.gbox_solar_constants)
        self.hslider_solar_const_dirt_loss.setMaximumSize(QtCore.QSize(300, 16777215))
        self.hslider_solar_const_dirt_loss.setMaximum(100)
        self.hslider_solar_const_dirt_loss.setPageStep(5)
        self.hslider_solar_const_dirt_loss.setOrientation(QtCore.Qt.Horizontal)
        self.hslider_solar_const_dirt_loss.setInvertedAppearance(False)
        self.hslider_solar_const_dirt_loss.setInvertedControls(True)
        self.hslider_solar_const_dirt_loss.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.hslider_solar_const_dirt_loss.setObjectName("hslider_solar_const_dirt_loss")
        self.gridLayout_10.addWidget(self.hslider_solar_const_dirt_loss, 2, 1, 1, 1)
        self.hslider_solar_const_assumed_ac_loss = QtWidgets.QSlider(self.gbox_solar_constants)
        self.hslider_solar_const_assumed_ac_loss.setMaximumSize(QtCore.QSize(300, 16777215))
        self.hslider_solar_const_assumed_ac_loss.setMaximum(100)
        self.hslider_solar_const_assumed_ac_loss.setPageStep(5)
        self.hslider_solar_const_assumed_ac_loss.setOrientation(QtCore.Qt.Horizontal)
        self.hslider_solar_const_assumed_ac_loss.setInvertedAppearance(False)
        self.hslider_solar_const_assumed_ac_loss.setInvertedControls(True)
        self.hslider_solar_const_assumed_ac_loss.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.hslider_solar_const_assumed_ac_loss.setObjectName("hslider_solar_const_assumed_ac_loss")
        self.gridLayout_10.addWidget(self.hslider_solar_const_assumed_ac_loss, 3, 1, 1, 1)
        self.label_53 = QtWidgets.QLabel(self.gbox_solar_constants)
        self.label_53.setObjectName("label_53")
        self.gridLayout_10.addWidget(self.label_53, 6, 0, 1, 1)
        self.label_50 = QtWidgets.QLabel(self.gbox_solar_constants)
        self.label_50.setObjectName("label_50")
        self.gridLayout_10.addWidget(self.label_50, 3, 0, 1, 1)
        self.hslider_solar_const_assumed_dc_loss = QtWidgets.QSlider(self.gbox_solar_constants)
        self.hslider_solar_const_assumed_dc_loss.setMaximumSize(QtCore.QSize(300, 16777215))
        self.hslider_solar_const_assumed_dc_loss.setMaximum(100)
        self.hslider_solar_const_assumed_dc_loss.setPageStep(5)
        self.hslider_solar_const_assumed_dc_loss.setOrientation(QtCore.Qt.Horizontal)
        self.hslider_solar_const_assumed_dc_loss.setInvertedAppearance(False)
        self.hslider_solar_const_assumed_dc_loss.setInvertedControls(True)
        self.hslider_solar_const_assumed_dc_loss.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.hslider_solar_const_assumed_dc_loss.setObjectName("hslider_solar_const_assumed_dc_loss")
        self.gridLayout_10.addWidget(self.hslider_solar_const_assumed_dc_loss, 4, 1, 1, 1)
        self.txt_solar_const_tol = QtWidgets.QLineEdit(self.gbox_solar_constants)
        self.txt_solar_const_tol.setMaximumSize(QtCore.QSize(50, 22))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txt_solar_const_tol.setFont(font)
        self.txt_solar_const_tol.setObjectName("txt_solar_const_tol")
        self.gridLayout_10.addWidget(self.txt_solar_const_tol, 1, 2, 1, 1)
        self.label_49 = QtWidgets.QLabel(self.gbox_solar_constants)
        self.label_49.setObjectName("label_49")
        self.gridLayout_10.addWidget(self.label_49, 2, 0, 1, 1)
        self.txt_solar_const_assumed_ac_loss = QtWidgets.QLineEdit(self.gbox_solar_constants)
        self.txt_solar_const_assumed_ac_loss.setMaximumSize(QtCore.QSize(50, 22))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txt_solar_const_assumed_ac_loss.setFont(font)
        self.txt_solar_const_assumed_ac_loss.setObjectName("txt_solar_const_assumed_ac_loss")
        self.gridLayout_10.addWidget(self.txt_solar_const_assumed_ac_loss, 3, 2, 1, 1)
        self.txt_solar_const_dirt_loss = QtWidgets.QLineEdit(self.gbox_solar_constants)
        self.txt_solar_const_dirt_loss.setMaximumSize(QtCore.QSize(50, 22))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txt_solar_const_dirt_loss.setFont(font)
        self.txt_solar_const_dirt_loss.setObjectName("txt_solar_const_dirt_loss")
        self.gridLayout_10.addWidget(self.txt_solar_const_dirt_loss, 2, 2, 1, 1)
        self.txt_solar_const_temp_effect = QtWidgets.QLineEdit(self.gbox_solar_constants)
        self.txt_solar_const_temp_effect.setMaximumSize(QtCore.QSize(50, 22))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txt_solar_const_temp_effect.setFont(font)
        self.txt_solar_const_temp_effect.setObjectName("txt_solar_const_temp_effect")
        self.gridLayout_10.addWidget(self.txt_solar_const_temp_effect, 5, 2, 1, 1)
        self.txt_solar_const_assumed_dc_loss = QtWidgets.QLineEdit(self.gbox_solar_constants)
        self.txt_solar_const_assumed_dc_loss.setMaximumSize(QtCore.QSize(50, 22))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txt_solar_const_assumed_dc_loss.setFont(font)
        self.txt_solar_const_assumed_dc_loss.setObjectName("txt_solar_const_assumed_dc_loss")
        self.gridLayout_10.addWidget(self.txt_solar_const_assumed_dc_loss, 4, 2, 1, 1)
        self.txt_solar_const_safety_margin = QtWidgets.QLineEdit(self.gbox_solar_constants)
        self.txt_solar_const_safety_margin.setMaximumSize(QtCore.QSize(50, 22))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txt_solar_const_safety_margin.setFont(font)
        self.txt_solar_const_safety_margin.setObjectName("txt_solar_const_safety_margin")
        self.gridLayout_10.addWidget(self.txt_solar_const_safety_margin, 6, 2, 1, 1)
        self.dspbox_solar_const_amb_temp = QtWidgets.QDoubleSpinBox(self.gbox_solar_constants)
        self.dspbox_solar_const_amb_temp.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.dspbox_solar_const_amb_temp.setFont(font)
        self.dspbox_solar_const_amb_temp.setObjectName("dspbox_solar_const_amb_temp")
        self.gridLayout_10.addWidget(self.dspbox_solar_const_amb_temp, 0, 1, 1, 1)
        self.horizontalLayout_12.addWidget(self.gbox_solar_constants)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem8)
        self.tbl_solar_insolation = QtWidgets.QTableWidget(self.scrollAreaWidgetContents_4)
        self.tbl_solar_insolation.setMaximumSize(QtCore.QSize(230, 430))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.tbl_solar_insolation.setFont(font)
        self.tbl_solar_insolation.setAlternatingRowColors(True)
        self.tbl_solar_insolation.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tbl_solar_insolation.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tbl_solar_insolation.setShowGrid(True)
        self.tbl_solar_insolation.setObjectName("tbl_solar_insolation")
        self.tbl_solar_insolation.setColumnCount(3)
        self.tbl_solar_insolation.setRowCount(12)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_solar_insolation.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_solar_insolation.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_solar_insolation.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_solar_insolation.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_solar_insolation.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_solar_insolation.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_solar_insolation.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_solar_insolation.setVerticalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_solar_insolation.setVerticalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_solar_insolation.setVerticalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_solar_insolation.setVerticalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_solar_insolation.setVerticalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_solar_insolation.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_solar_insolation.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_solar_insolation.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tbl_solar_insolation.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tbl_solar_insolation.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tbl_solar_insolation.setItem(0, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tbl_solar_insolation.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tbl_solar_insolation.setItem(1, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tbl_solar_insolation.setItem(1, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tbl_solar_insolation.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tbl_solar_insolation.setItem(2, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tbl_solar_insolation.setItem(2, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tbl_solar_insolation.setItem(3, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tbl_solar_insolation.setItem(3, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tbl_solar_insolation.setItem(3, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tbl_solar_insolation.setItem(4, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tbl_solar_insolation.setItem(4, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tbl_solar_insolation.setItem(4, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tbl_solar_insolation.setItem(5, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tbl_solar_insolation.setItem(5, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tbl_solar_insolation.setItem(5, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tbl_solar_insolation.setItem(6, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tbl_solar_insolation.setItem(6, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tbl_solar_insolation.setItem(6, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tbl_solar_insolation.setItem(7, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tbl_solar_insolation.setItem(7, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tbl_solar_insolation.setItem(7, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tbl_solar_insolation.setItem(8, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tbl_solar_insolation.setItem(8, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tbl_solar_insolation.setItem(8, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tbl_solar_insolation.setItem(9, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tbl_solar_insolation.setItem(9, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tbl_solar_insolation.setItem(9, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tbl_solar_insolation.setItem(10, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tbl_solar_insolation.setItem(10, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tbl_solar_insolation.setItem(10, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tbl_solar_insolation.setItem(11, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tbl_solar_insolation.setItem(11, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tbl_solar_insolation.setItem(11, 2, item)
        self.tbl_solar_insolation.horizontalHeader().setDefaultSectionSize(60)
        self.tbl_solar_insolation.horizontalHeader().setSortIndicatorShown(False)
        self.tbl_solar_insolation.horizontalHeader().setStretchLastSection(True)
        self.tbl_solar_insolation.verticalHeader().setDefaultSectionSize(32)
        self.tbl_solar_insolation.verticalHeader().setMinimumSectionSize(25)
        self.tbl_solar_insolation.verticalHeader().setStretchLastSection(True)
        self.horizontalLayout_12.addWidget(self.tbl_solar_insolation)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem9)
        self.gb_solar_months = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_4)
        self.gb_solar_months.setMinimumSize(QtCore.QSize(150, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.gb_solar_months.setFont(font)
        self.gb_solar_months.setObjectName("gb_solar_months")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.gb_solar_months)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.cbox_solar_months_selectall = QtWidgets.QCheckBox(self.gb_solar_months)
        self.cbox_solar_months_selectall.setObjectName("cbox_solar_months_selectall")
        self.verticalLayout_11.addWidget(self.cbox_solar_months_selectall)
        self.cbox_solar_months_jan = QtWidgets.QCheckBox(self.gb_solar_months)
        self.cbox_solar_months_jan.setObjectName("cbox_solar_months_jan")
        self.verticalLayout_11.addWidget(self.cbox_solar_months_jan)
        self.cbox_solar_months_feb = QtWidgets.QCheckBox(self.gb_solar_months)
        self.cbox_solar_months_feb.setObjectName("cbox_solar_months_feb")
        self.verticalLayout_11.addWidget(self.cbox_solar_months_feb)
        self.cbox_solar_months_mar = QtWidgets.QCheckBox(self.gb_solar_months)
        self.cbox_solar_months_mar.setObjectName("cbox_solar_months_mar")
        self.verticalLayout_11.addWidget(self.cbox_solar_months_mar)
        self.cbox_solar_months_apr = QtWidgets.QCheckBox(self.gb_solar_months)
        self.cbox_solar_months_apr.setObjectName("cbox_solar_months_apr")
        self.verticalLayout_11.addWidget(self.cbox_solar_months_apr)
        self.cbox_solar_months_may = QtWidgets.QCheckBox(self.gb_solar_months)
        self.cbox_solar_months_may.setObjectName("cbox_solar_months_may")
        self.verticalLayout_11.addWidget(self.cbox_solar_months_may)
        self.cbox_solar_months_jun = QtWidgets.QCheckBox(self.gb_solar_months)
        self.cbox_solar_months_jun.setObjectName("cbox_solar_months_jun")
        self.verticalLayout_11.addWidget(self.cbox_solar_months_jun)
        self.cbox_solar_months_jul = QtWidgets.QCheckBox(self.gb_solar_months)
        self.cbox_solar_months_jul.setObjectName("cbox_solar_months_jul")
        self.verticalLayout_11.addWidget(self.cbox_solar_months_jul)
        self.cbox_solar_months_aug = QtWidgets.QCheckBox(self.gb_solar_months)
        self.cbox_solar_months_aug.setObjectName("cbox_solar_months_aug")
        self.verticalLayout_11.addWidget(self.cbox_solar_months_aug)
        self.cbox_solar_months_sept = QtWidgets.QCheckBox(self.gb_solar_months)
        self.cbox_solar_months_sept.setObjectName("cbox_solar_months_sept")
        self.verticalLayout_11.addWidget(self.cbox_solar_months_sept)
        self.cbox_solar_months_oct = QtWidgets.QCheckBox(self.gb_solar_months)
        self.cbox_solar_months_oct.setObjectName("cbox_solar_months_oct")
        self.verticalLayout_11.addWidget(self.cbox_solar_months_oct)
        self.cbox_solar_months_nov = QtWidgets.QCheckBox(self.gb_solar_months)
        self.cbox_solar_months_nov.setObjectName("cbox_solar_months_nov")
        self.verticalLayout_11.addWidget(self.cbox_solar_months_nov)
        self.cbox_solar_months_dec = QtWidgets.QCheckBox(self.gb_solar_months)
        self.cbox_solar_months_dec.setObjectName("cbox_solar_months_dec")
        self.verticalLayout_11.addWidget(self.cbox_solar_months_dec)
        self.horizontalLayout_12.addWidget(self.gb_solar_months)
        self.scrollArea_4.setWidget(self.scrollAreaWidgetContents_4)
        self.verticalLayout_7.addWidget(self.scrollArea_4)
        self.stk_solar_pv_main.addWidget(self.stk_solar_pv_main_input_3)  # this shows solar results
        self.stk_solar_pv_main_output = QtWidgets.QWidget()
        self.stk_solar_pv_main_output.setObjectName("stk_solar_pv_main_output")
        self.gridLayout_28 = QtWidgets.QGridLayout(self.stk_solar_pv_main_output)
        self.gridLayout_28.setObjectName("gridLayout_28")
        self.tbl_solar_output_result = QtWidgets.QTableWidget(self.stk_solar_pv_main_output)
        self.tbl_solar_output_result.setMinimumSize(QtCore.QSize(350, 0))
        self.tbl_solar_output_result.setMaximumSize(QtCore.QSize(350, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.tbl_solar_output_result.setFont(font)
        self.tbl_solar_output_result.setObjectName("tbl_solar_output_result")
        self.tbl_solar_output_result.setColumnCount(1)
        self.tbl_solar_output_result.setRowCount(22)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_solar_output_result.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_solar_output_result.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_solar_output_result.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_solar_output_result.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_solar_output_result.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_solar_output_result.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_solar_output_result.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_solar_output_result.setVerticalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_solar_output_result.setVerticalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_solar_output_result.setVerticalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_solar_output_result.setVerticalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_solar_output_result.setVerticalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_solar_output_result.setVerticalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_solar_output_result.setVerticalHeaderItem(13, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_solar_output_result.setVerticalHeaderItem(14, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_solar_output_result.setVerticalHeaderItem(15, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_solar_output_result.setVerticalHeaderItem(16, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_solar_output_result.setVerticalHeaderItem(17, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_solar_output_result.setVerticalHeaderItem(18, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_solar_output_result.setVerticalHeaderItem(19, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_solar_output_result.setVerticalHeaderItem(20, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_solar_output_result.setVerticalHeaderItem(21, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_solar_output_result.setHorizontalHeaderItem(0, item)
        self.tbl_solar_output_result.horizontalHeader().setDefaultSectionSize(48)
        self.tbl_solar_output_result.horizontalHeader().setStretchLastSection(True)
        self.tbl_solar_output_result.verticalHeader().setStretchLastSection(True)
        self.gridLayout_28.addWidget(self.tbl_solar_output_result, 0, 0, 1, 1)
        self.tbl_solar_output_psh = QtWidgets.QTableWidget(self.stk_solar_pv_main_output)
        self.tbl_solar_output_psh.setMinimumSize(QtCore.QSize(200, 0))
        self.tbl_solar_output_psh.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.tbl_solar_output_psh.setFont(font)
        self.tbl_solar_output_psh.setObjectName("tbl_solar_output_psh")
        self.tbl_solar_output_psh.setColumnCount(1)
        self.tbl_solar_output_psh.setRowCount(12)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_solar_output_psh.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_solar_output_psh.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_solar_output_psh.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_solar_output_psh.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_solar_output_psh.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_solar_output_psh.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_solar_output_psh.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_solar_output_psh.setVerticalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_solar_output_psh.setVerticalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_solar_output_psh.setVerticalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_solar_output_psh.setVerticalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_solar_output_psh.setVerticalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_solar_output_psh.setHorizontalHeaderItem(0, item)
        self.tbl_solar_output_psh.horizontalHeader().setStretchLastSection(True)
        self.tbl_solar_output_psh.verticalHeader().setDefaultSectionSize(39)
        self.tbl_solar_output_psh.verticalHeader().setMinimumSectionSize(32)
        self.tbl_solar_output_psh.verticalHeader().setStretchLastSection(True)
        self.gridLayout_28.addWidget(self.tbl_solar_output_psh, 0, 1, 1, 1)
        self.gb_solar_output = QtWidgets.QGroupBox(self.stk_solar_pv_main_output)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.gb_solar_output.setFont(font)
        self.gb_solar_output.setAlignment(QtCore.Qt.AlignCenter)
        self.gb_solar_output.setFlat(True)
        self.gb_solar_output.setObjectName("gb_solar_output")
        self.verticalLayout_19 = QtWidgets.QVBoxLayout(self.gb_solar_output)
        self.verticalLayout_19.setObjectName("verticalLayout_19")
        self.tb_solar_output_barchart = QtWidgets.QWidget(self.gb_solar_output)
        self.tb_solar_output_barchart.setObjectName("tb_solar_output_barchart")
        self.verticalLayout_19.addWidget(self.tb_solar_output_barchart)
        self.tb_solar_output_expand_fig = QtWidgets.QToolButton(self.gb_solar_output)
        self.tb_solar_output_expand_fig.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setUnderline(True)
        self.tb_solar_output_expand_fig.setFont(font)
        self.tb_solar_output_expand_fig.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/icons/icons/maximize.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tb_solar_output_expand_fig.setIcon(icon10)
        self.tb_solar_output_expand_fig.setIconSize(QtCore.QSize(20, 20))
        self.tb_solar_output_expand_fig.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.tb_solar_output_expand_fig.setAutoRaise(True)
        self.tb_solar_output_expand_fig.setObjectName("tb_solar_output_expand_fig")
        self.verticalLayout_19.addWidget(self.tb_solar_output_expand_fig, 0, QtCore.Qt.AlignHCenter)
        self.gridLayout_28.addWidget(self.gb_solar_output, 0, 2, 1, 1)
        self.stk_solar_pv_main.addWidget(self.stk_solar_pv_main_output)  # handles result as well
        self.gridLayout_20.addWidget(self.stk_solar_pv_main, 3, 0, 1, 2)
        self.horizontalFrame_9.raise_()
        self.stk_solar_pv_main.raise_()
        self.line_5.raise_()
        self.stacked_main_windows.addWidget(self.stk_solar_pv)
        # end solar pv definition #

        # begin wind turbine definition #
        self.stk_wind_turbine = QtWidgets.QWidget()
        self.stk_wind_turbine.setObjectName("stk_wind_turbine")
        self.gridLayout_22 = QtWidgets.QGridLayout(self.stk_wind_turbine)
        self.gridLayout_22.setObjectName("gridLayout_22")
        self.horizontalFrame_10 = QtWidgets.QFrame(self.stk_wind_turbine)
        self.horizontalFrame_10.setMinimumSize(QtCore.QSize(0, 40))
        self.horizontalFrame_10.setMaximumSize(QtCore.QSize(16777215, 70))
        self.horizontalFrame_10.setObjectName("horizontalFrame_10")
        self.horizontalLayout_22 = QtWidgets.QHBoxLayout(self.horizontalFrame_10)
        self.horizontalLayout_22.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout_22.setContentsMargins(8, 8, -1, -1)
        self.horizontalLayout_22.setSpacing(10)
        self.horizontalLayout_22.setObjectName("horizontalLayout_22")
        self.label_71 = QtWidgets.QLabel(self.horizontalFrame_10)
        self.label_71.setMinimumSize(QtCore.QSize(50, 50))
        self.label_71.setMaximumSize(QtCore.QSize(50, 50))
        self.label_71.setText("")
        self.label_71.setPixmap(QtGui.QPixmap(":/icons/icons/wind-engine.png"))
        self.label_71.setScaledContents(True)
        self.label_71.setObjectName("label_71")
        self.horizontalLayout_22.addWidget(self.label_71, 0, QtCore.Qt.AlignRight)
        self.line_6 = QtWidgets.QFrame(self.horizontalFrame_10)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_6.setLineWidth(2)
        self.line_6.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_6.setObjectName("line_6")
        self.horizontalLayout_22.addWidget(self.line_6, 0, QtCore.Qt.AlignLeft)
        self.label_72 = QtWidgets.QLabel(self.horizontalFrame_10)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_72.setFont(font)
        self.label_72.setObjectName("label_72")
        self.horizontalLayout_22.addWidget(self.label_72, 0, QtCore.Qt.AlignLeft)
        self.gridLayout_22.addWidget(self.horizontalFrame_10, 0, 0, 1, 1, QtCore.Qt.AlignLeft)
        self.line_7 = QtWidgets.QFrame(self.stk_wind_turbine)
        self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.gridLayout_22.addWidget(self.line_7, 1, 0, 1, 1)
        self.stk_wind_turb_main = QtWidgets.QStackedWidget(self.stk_wind_turbine)
        self.stk_wind_turb_main.setObjectName("stk_wind_turb_main")
        self.stk_wind_turb_main_input = QtWidgets.QWidget()
        self.stk_wind_turb_main_input.setObjectName("stk_wind_turb_main_input")
        self.gridLayout_14 = QtWidgets.QGridLayout(self.stk_wind_turb_main_input)
        self.gridLayout_14.setObjectName("gridLayout_14")
        self.scrollArea_5 = QtWidgets.QScrollArea(self.stk_wind_turb_main_input)
        self.scrollArea_5.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea_5.setWidgetResizable(True)
        self.scrollArea_5.setObjectName("scrollArea_5")
        self.scrollAreaWidgetContents_5 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_5.setGeometry(QtCore.QRect(0, 0, 615, 482))
        self.scrollAreaWidgetContents_5.setObjectName("scrollAreaWidgetContents_5")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents_5)
        self.horizontalLayout_13.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout_13.setSpacing(3)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.gb_wind_turb_stdt = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_5)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.gb_wind_turb_stdt.setFont(font)
        self.gb_wind_turb_stdt.setObjectName("gb_wind_turb_stdt")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.gb_wind_turb_stdt)
        self.gridLayout_11.setContentsMargins(-1, -1, 30, 5)
        self.gridLayout_11.setHorizontalSpacing(68)
        self.gridLayout_11.setVerticalSpacing(5)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.label_10 = QtWidgets.QLabel(self.gb_wind_turb_stdt)
        self.label_10.setMinimumSize(QtCore.QSize(50, 29))
        self.label_10.setMaximumSize(QtCore.QSize(70, 29))
        self.label_10.setObjectName("label_10")
        self.gridLayout_11.addWidget(self.label_10, 0, 0, 1, 1)
        self.txt_wind_turb_stdt_lat = QtWidgets.QLineEdit(self.gb_wind_turb_stdt)
        self.txt_wind_turb_stdt_lat.setMinimumSize(QtCore.QSize(120, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txt_wind_turb_stdt_lat.setFont(font)
        self.txt_wind_turb_stdt_lat.setFrame(True)
        self.txt_wind_turb_stdt_lat.setObjectName("txt_wind_turb_stdt_lat")
        self.gridLayout_11.addWidget(self.txt_wind_turb_stdt_lat, 1, 1, 1, 1)
        self.label_33 = QtWidgets.QLabel(self.gb_wind_turb_stdt)
        self.label_33.setMinimumSize(QtCore.QSize(65, 39))
        self.label_33.setObjectName("label_33")
        self.gridLayout_11.addWidget(self.label_33, 2, 0, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.gb_wind_turb_stdt)
        self.label_11.setMinimumSize(QtCore.QSize(65, 39))
        self.label_11.setObjectName("label_11")
        self.gridLayout_11.addWidget(self.label_11, 1, 0, 1, 1)
        self.txt_wind_turb_stdt_long = QtWidgets.QLineEdit(self.gb_wind_turb_stdt)
        self.txt_wind_turb_stdt_long.setMinimumSize(QtCore.QSize(133, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txt_wind_turb_stdt_long.setFont(font)
        self.txt_wind_turb_stdt_long.setObjectName("txt_wind_turb_stdt_long")
        self.gridLayout_11.addWidget(self.txt_wind_turb_stdt_long, 2, 1, 1, 1)
        self.cmbx_wind_turb_site_name = QtWidgets.QComboBox(self.gb_wind_turb_stdt)
        self.cmbx_wind_turb_site_name.setMinimumSize(QtCore.QSize(100, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.cmbx_wind_turb_site_name.setFont(font)
        self.cmbx_wind_turb_site_name.setEditable(True)
        self.cmbx_wind_turb_site_name.setFrame(True)
        self.cmbx_wind_turb_site_name.setObjectName("cmbx_wind_turb_site_name")
        self.gridLayout_11.addWidget(self.cmbx_wind_turb_site_name, 0, 1, 1, 1)
        self.gb_wind_turb_ardt = QtWidgets.QGroupBox(self.gb_wind_turb_stdt)
        self.gb_wind_turb_ardt.setFlat(True)
        self.gb_wind_turb_ardt.setCheckable(False)
        self.gb_wind_turb_ardt.setObjectName("gb_wind_turb_ardt")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.gb_wind_turb_ardt)
        self.gridLayout_4.setContentsMargins(4, -1, 1, -1)
        self.gridLayout_4.setHorizontalSpacing(48)
        self.gridLayout_4.setVerticalSpacing(15)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_45 = QtWidgets.QLabel(self.gb_wind_turb_ardt)
        self.label_45.setMinimumSize(QtCore.QSize(65, 20))
        self.label_45.setObjectName("label_45")
        self.gridLayout_4.addWidget(self.label_45, 0, 0, 1, 1)
        self.txt_wind_turb_ardt_den = QtWidgets.QLineEdit(self.gb_wind_turb_ardt)
        self.txt_wind_turb_ardt_den.setMinimumSize(QtCore.QSize(100, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txt_wind_turb_ardt_den.setFont(font)
        self.txt_wind_turb_ardt_den.setObjectName("txt_wind_turb_ardt_den")
        self.gridLayout_4.addWidget(self.txt_wind_turb_ardt_den, 0, 1, 1, 1)
        self.label_44 = QtWidgets.QLabel(self.gb_wind_turb_ardt)
        self.label_44.setMinimumSize(QtCore.QSize(65, 20))
        self.label_44.setObjectName("label_44")
        self.gridLayout_4.addWidget(self.label_44, 1, 0, 1, 1)
        self.txt_wind_turb_ardt_temp = QtWidgets.QLineEdit(self.gb_wind_turb_ardt)
        self.txt_wind_turb_ardt_temp.setMinimumSize(QtCore.QSize(100, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txt_wind_turb_ardt_temp.setFont(font)
        self.txt_wind_turb_ardt_temp.setObjectName("txt_wind_turb_ardt_temp")
        self.gridLayout_4.addWidget(self.txt_wind_turb_ardt_temp, 1, 1, 1, 1)
        self.label_34 = QtWidgets.QLabel(self.gb_wind_turb_ardt)
        self.label_34.setMinimumSize(QtCore.QSize(65, 20))
        self.label_34.setObjectName("label_34")
        self.gridLayout_4.addWidget(self.label_34, 2, 0, 1, 1)
        self.txt_wind_turb_ardt_alt = QtWidgets.QLineEdit(self.gb_wind_turb_ardt)
        self.txt_wind_turb_ardt_alt.setMinimumSize(QtCore.QSize(100, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txt_wind_turb_ardt_alt.setFont(font)
        self.txt_wind_turb_ardt_alt.setObjectName("txt_wind_turb_ardt_alt")
        self.gridLayout_4.addWidget(self.txt_wind_turb_ardt_alt, 2, 1, 1, 1)
        self.label_35 = QtWidgets.QLabel(self.gb_wind_turb_ardt)
        self.label_35.setMinimumSize(QtCore.QSize(65, 20))
        self.label_35.setObjectName("label_35")
        self.gridLayout_4.addWidget(self.label_35, 3, 0, 1, 1)
        self.txt_wind_turb_ardt_press = QtWidgets.QLineEdit(self.gb_wind_turb_ardt)
        self.txt_wind_turb_ardt_press.setMinimumSize(QtCore.QSize(100, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txt_wind_turb_ardt_press.setFont(font)
        self.txt_wind_turb_ardt_press.setObjectName("txt_wind_turb_ardt_press")
        self.gridLayout_4.addWidget(self.txt_wind_turb_ardt_press, 3, 1, 1, 1)
        self.gridLayout_11.addWidget(self.gb_wind_turb_ardt, 3, 0, 1, 2)
        self.gb_wind_turb_wddt = QtWidgets.QGroupBox(self.gb_wind_turb_stdt)
        self.gb_wind_turb_wddt.setFlat(True)
        self.gb_wind_turb_wddt.setObjectName("gb_wind_turb_wddt")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.gb_wind_turb_wddt)
        self.gridLayout_8.setContentsMargins(5, -1, 1, -1)
        self.gridLayout_8.setHorizontalSpacing(21)
        self.gridLayout_8.setVerticalSpacing(9)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.txt_wind_turb_wddt_vel = QtWidgets.QLineEdit(self.gb_wind_turb_wddt)
        self.txt_wind_turb_wddt_vel.setMinimumSize(QtCore.QSize(100, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txt_wind_turb_wddt_vel.setFont(font)
        self.txt_wind_turb_wddt_vel.setObjectName("txt_wind_turb_wddt_vel")
        self.gridLayout_8.addWidget(self.txt_wind_turb_wddt_vel, 0, 1, 1, 1)
        self.label_46 = QtWidgets.QLabel(self.gb_wind_turb_wddt)
        self.label_46.setMinimumSize(QtCore.QSize(65, 20))
        self.label_46.setObjectName("label_46")
        self.gridLayout_8.addWidget(self.label_46, 3, 0, 1, 1)
        self.txt_wind_turb_wddt_height = QtWidgets.QLineEdit(self.gb_wind_turb_wddt)
        self.txt_wind_turb_wddt_height.setMinimumSize(QtCore.QSize(100, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txt_wind_turb_wddt_height.setFont(font)
        self.txt_wind_turb_wddt_height.setObjectName("txt_wind_turb_wddt_height")
        self.gridLayout_8.addWidget(self.txt_wind_turb_wddt_height, 1, 1, 1, 1)
        self.label_57 = QtWidgets.QLabel(self.gb_wind_turb_wddt)
        self.label_57.setMinimumSize(QtCore.QSize(65, 20))
        self.label_57.setObjectName("label_57")
        self.gridLayout_8.addWidget(self.label_57, 0, 0, 1, 1)
        self.label_55 = QtWidgets.QLabel(self.gb_wind_turb_wddt)
        self.label_55.setMinimumSize(QtCore.QSize(65, 20))
        self.label_55.setObjectName("label_55")
        self.gridLayout_8.addWidget(self.label_55, 1, 0, 1, 1)
        self.txt_wind_turb_wddt_shape_param = QtWidgets.QLineEdit(self.gb_wind_turb_wddt)
        self.txt_wind_turb_wddt_shape_param.setMinimumSize(QtCore.QSize(100, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txt_wind_turb_wddt_shape_param.setFont(font)
        self.txt_wind_turb_wddt_shape_param.setObjectName("txt_wind_turb_wddt_shape_param")
        self.gridLayout_8.addWidget(self.txt_wind_turb_wddt_shape_param, 2, 1, 1, 1)
        self.txt_wind_turb_wddt_scale_param = QtWidgets.QLineEdit(self.gb_wind_turb_wddt)
        self.txt_wind_turb_wddt_scale_param.setMinimumSize(QtCore.QSize(100, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txt_wind_turb_wddt_scale_param.setFont(font)
        self.txt_wind_turb_wddt_scale_param.setObjectName("txt_wind_turb_wddt_scale_param")
        self.gridLayout_8.addWidget(self.txt_wind_turb_wddt_scale_param, 3, 1, 1, 1)
        self.label_56 = QtWidgets.QLabel(self.gb_wind_turb_wddt)
        self.label_56.setMinimumSize(QtCore.QSize(65, 20))
        self.label_56.setObjectName("label_56")
        self.gridLayout_8.addWidget(self.label_56, 2, 0, 1, 1)
        self.gridLayout_11.addWidget(self.gb_wind_turb_wddt, 4, 0, 1, 2)
        self.cbox_wind_turb_stdt_save = QtWidgets.QCheckBox(self.gb_wind_turb_stdt)
        self.cbox_wind_turb_stdt_save.setObjectName("cbox_wind_turb_stdt_save")
        self.gridLayout_11.addWidget(self.cbox_wind_turb_stdt_save, 5, 0, 1, 2, QtCore.Qt.AlignRight)
        self.horizontalLayout_13.addWidget(self.gb_wind_turb_stdt)
        spacerItem10 = QtWidgets.QSpacerItem(800, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem10)
        self.gb_wind_turb_tbin = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_5)
        self.gb_wind_turb_tbin.setMinimumSize(QtCore.QSize(300, 0))
        self.gb_wind_turb_tbin.setMaximumSize(QtCore.QSize(600, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.gb_wind_turb_tbin.setFont(font)
        self.gb_wind_turb_tbin.setObjectName("gb_wind_turb_tbin")
        self.gridLayout_13 = QtWidgets.QGridLayout(self.gb_wind_turb_tbin)
        self.gridLayout_13.setHorizontalSpacing(39)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.groupBox_22 = QtWidgets.QGroupBox(self.gb_wind_turb_tbin)
        self.groupBox_22.setTitle("")
        self.groupBox_22.setFlat(True)
        self.groupBox_22.setObjectName("groupBox_22")
        self.gridLayout_12 = QtWidgets.QGridLayout(self.groupBox_22)
        self.gridLayout_12.setContentsMargins(2, -1, -1, -1)
        self.gridLayout_12.setHorizontalSpacing(20)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.label_60 = QtWidgets.QLabel(self.groupBox_22)
        self.label_60.setMinimumSize(QtCore.QSize(120, 20))
        self.label_60.setObjectName("label_60")
        self.gridLayout_12.addWidget(self.label_60, 0, 0, 1, 1)
        self.txt_wind_turb_tbin_rated_pow = QtWidgets.QLineEdit(self.groupBox_22)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txt_wind_turb_tbin_rated_pow.setFont(font)
        self.txt_wind_turb_tbin_rated_pow.setObjectName("txt_wind_turb_tbin_rated_pow")
        self.gridLayout_12.addWidget(self.txt_wind_turb_tbin_rated_pow, 0, 1, 1, 1)
        self.label_58 = QtWidgets.QLabel(self.groupBox_22)
        self.label_58.setMinimumSize(QtCore.QSize(120, 20))
        self.label_58.setObjectName("label_58")
        self.gridLayout_12.addWidget(self.label_58, 1, 0, 1, 1)
        self.txt_wind_turb_tbin_cut_in = QtWidgets.QLineEdit(self.groupBox_22)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txt_wind_turb_tbin_cut_in.setFont(font)
        self.txt_wind_turb_tbin_cut_in.setObjectName("txt_wind_turb_tbin_cut_in")
        self.gridLayout_12.addWidget(self.txt_wind_turb_tbin_cut_in, 1, 1, 1, 1)
        self.label_61 = QtWidgets.QLabel(self.groupBox_22)
        self.label_61.setMinimumSize(QtCore.QSize(120, 20))
        self.label_61.setObjectName("label_61")
        self.gridLayout_12.addWidget(self.label_61, 2, 0, 1, 1)
        self.txt_wind_turb_tbin_cut_out = QtWidgets.QLineEdit(self.groupBox_22)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txt_wind_turb_tbin_cut_out.setFont(font)
        self.txt_wind_turb_tbin_cut_out.setObjectName("txt_wind_turb_tbin_cut_out")
        self.gridLayout_12.addWidget(self.txt_wind_turb_tbin_cut_out, 2, 1, 1, 1)
        self.label_59 = QtWidgets.QLabel(self.groupBox_22)
        self.label_59.setMinimumSize(QtCore.QSize(120, 20))
        self.label_59.setObjectName("label_59")
        self.gridLayout_12.addWidget(self.label_59, 3, 0, 1, 1)
        self.txt_wind_turb_tbin_rotor_diam = QtWidgets.QLineEdit(self.groupBox_22)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txt_wind_turb_tbin_rotor_diam.setFont(font)
        self.txt_wind_turb_tbin_rotor_diam.setObjectName("txt_wind_turb_tbin_rotor_diam")
        self.gridLayout_12.addWidget(self.txt_wind_turb_tbin_rotor_diam, 3, 1, 1, 1)
        self.label_64 = QtWidgets.QLabel(self.groupBox_22)
        self.label_64.setMinimumSize(QtCore.QSize(120, 20))
        self.label_64.setObjectName("label_64")
        self.gridLayout_12.addWidget(self.label_64, 4, 0, 1, 1)
        self.txt_wind_turb_tbin_hub_height = QtWidgets.QLineEdit(self.groupBox_22)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txt_wind_turb_tbin_hub_height.setFont(font)
        self.txt_wind_turb_tbin_hub_height.setObjectName("txt_wind_turb_tbin_hub_height")
        self.gridLayout_12.addWidget(self.txt_wind_turb_tbin_hub_height, 4, 1, 1, 1)
        self.label_63 = QtWidgets.QLabel(self.groupBox_22)
        self.label_63.setMinimumSize(QtCore.QSize(120, 20))
        self.label_63.setObjectName("label_63")
        self.gridLayout_12.addWidget(self.label_63, 5, 0, 1, 1)
        self.spbx_wind_turb_tbin_units = QtWidgets.QSpinBox(self.groupBox_22)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.spbx_wind_turb_tbin_units.setFont(font)
        self.spbx_wind_turb_tbin_units.setObjectName("spbx_wind_turb_tbin_units")
        self.gridLayout_12.addWidget(self.spbx_wind_turb_tbin_units, 5, 1, 1, 1)
        self.label_62 = QtWidgets.QLabel(self.groupBox_22)
        self.label_62.setMinimumSize(QtCore.QSize(120, 20))
        self.label_62.setObjectName("label_62")
        self.gridLayout_12.addWidget(self.label_62, 6, 0, 1, 1)
        self.txt_wind_turb_tbin_blade_length = QtWidgets.QLineEdit(self.groupBox_22)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txt_wind_turb_tbin_blade_length.setFont(font)
        self.txt_wind_turb_tbin_blade_length.setObjectName("txt_wind_turb_tbin_blade_length")
        self.gridLayout_12.addWidget(self.txt_wind_turb_tbin_blade_length, 6, 1, 1, 1)
        self.label_65 = QtWidgets.QLabel(self.groupBox_22)
        self.label_65.setMinimumSize(QtCore.QSize(120, 20))
        self.label_65.setObjectName("label_65")
        self.gridLayout_12.addWidget(self.label_65, 7, 0, 1, 1)
        self.spbx_wind_turb_tbin_no_blades = QtWidgets.QSpinBox(self.groupBox_22)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.spbx_wind_turb_tbin_no_blades.setFont(font)
        self.spbx_wind_turb_tbin_no_blades.setObjectName("spbx_wind_turb_tbin_no_blades")
        self.gridLayout_12.addWidget(self.spbx_wind_turb_tbin_no_blades, 7, 1, 1, 1)
        self.gridLayout_13.addWidget(self.groupBox_22, 1, 0, 1, 2)
        self.cmbx_wind_turb_tbin_name = QtWidgets.QComboBox(self.gb_wind_turb_tbin)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.cmbx_wind_turb_tbin_name.setFont(font)
        self.cmbx_wind_turb_tbin_name.setEditable(True)
        self.cmbx_wind_turb_tbin_name.setObjectName("cmbx_wind_turb_tbin_name")
        self.gridLayout_13.addWidget(self.cmbx_wind_turb_tbin_name, 0, 1, 1, 1)
        self.label_66 = QtWidgets.QLabel(self.gb_wind_turb_tbin)
        self.label_66.setMinimumSize(QtCore.QSize(100, 39))
        self.label_66.setMaximumSize(QtCore.QSize(120, 39))
        self.label_66.setObjectName("label_66")
        self.gridLayout_13.addWidget(self.label_66, 0, 0, 1, 1)
        self.cbox_wind_turb_tbin_save = QtWidgets.QCheckBox(self.gb_wind_turb_tbin)
        self.cbox_wind_turb_tbin_save.setObjectName("cbox_wind_turb_tbin_save")
        self.gridLayout_13.addWidget(self.cbox_wind_turb_tbin_save, 2, 0, 1, 2, QtCore.Qt.AlignRight)
        self.horizontalLayout_13.addWidget(self.gb_wind_turb_tbin)
        self.scrollArea_5.setWidget(self.scrollAreaWidgetContents_5)
        self.gridLayout_14.addWidget(self.scrollArea_5, 0, 0, 1, 1)
        self.stk_wind_turb_main.addWidget(self.stk_wind_turb_main_input)
        # added till here
        self.stk_wind_turb_main_output = QtWidgets.QWidget()
        self.stk_wind_turb_main_output.setObjectName("stk_wind_turb_main_output")
        self.gridLayout_57 = QtWidgets.QGridLayout(self.stk_wind_turb_main_output)
        self.gridLayout_57.setObjectName("gridLayout_57")
        self.frm_wind_turb_output_pow = QtWidgets.QWidget(self.stk_wind_turb_main_output)
        self.frm_wind_turb_output_pow.setObjectName("frm_wind_turb_output_pow")
        self.verticalLayout_38 = QtWidgets.QVBoxLayout(self.frm_wind_turb_output_pow)
        self.verticalLayout_38.setContentsMargins(-1, 30, -1, 30)
        self.verticalLayout_38.setObjectName("verticalLayout_38")
        self.label_212 = QtWidgets.QLabel(self.frm_wind_turb_output_pow)
        self.label_212.setMinimumSize(QtCore.QSize(200, 200))
        self.label_212.setMaximumSize(QtCore.QSize(200, 200))
        self.label_212.setText("")
        self.label_212.setPixmap(QtGui.QPixmap(":/icons/icons/renewable-energy.png"))
        self.label_212.setScaledContents(True)
        self.label_212.setAlignment(QtCore.Qt.AlignCenter)
        self.label_212.setObjectName("label_212")
        self.verticalLayout_38.addWidget(self.label_212, 0, QtCore.Qt.AlignHCenter)
        self.label_213 = QtWidgets.QLabel(self.frm_wind_turb_output_pow)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiLight")
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.label_213.setFont(font)
        self.label_213.setObjectName("label_213")
        self.verticalLayout_38.addWidget(self.label_213, 0, QtCore.Qt.AlignHCenter)
        self.line_27 = QtWidgets.QFrame(self.frm_wind_turb_output_pow)
        self.line_27.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_27.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_27.setObjectName("line_27")
        self.verticalLayout_38.addWidget(self.line_27)
        self.lbl_wind_turb_output_pow = QtWidgets.QLabel(self.frm_wind_turb_output_pow)
        font = QtGui.QFont()
        font.setFamily("Maiandra GD")
        font.setPointSize(36)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_wind_turb_output_pow.setFont(font)
        self.lbl_wind_turb_output_pow.setTextFormat(QtCore.Qt.PlainText)
        self.lbl_wind_turb_output_pow.setScaledContents(True)
        self.lbl_wind_turb_output_pow.setWordWrap(True)
        self.lbl_wind_turb_output_pow.setObjectName("lbl_wind_turb_output_pow")
        self.verticalLayout_38.addWidget(self.lbl_wind_turb_output_pow, 0, QtCore.Qt.AlignHCenter)
        self.label_214 = QtWidgets.QLabel(self.frm_wind_turb_output_pow)
        self.label_214.setMinimumSize(QtCore.QSize(30, 40))
        font = QtGui.QFont()
        font.setFamily("Maiandra GD")
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.label_214.setFont(font)
        self.label_214.setObjectName("label_214")
        self.verticalLayout_38.addWidget(self.label_214, 0, QtCore.Qt.AlignHCenter)
        self.gridLayout_57.addWidget(self.frm_wind_turb_output_pow, 0, 0, 1, 1)
        spacerItem11 = QtWidgets.QSpacerItem(80, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_57.addItem(spacerItem11, 0, 1, 1, 1)
        self.line_23 = QtWidgets.QFrame(self.stk_wind_turb_main_output)
        self.line_23.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_23.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_23.setObjectName("line_23")
        self.gridLayout_57.addWidget(self.line_23, 0, 2, 1, 1)
        spacerItem12 = QtWidgets.QSpacerItem(80, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_57.addItem(spacerItem12, 0, 3, 1, 1)
        self.frm_wind_turb_output_eff = QtWidgets.QWidget(self.stk_wind_turb_main_output)
        self.frm_wind_turb_output_eff.setObjectName("frm_wind_turb_output_eff")
        self.verticalLayout_37 = QtWidgets.QVBoxLayout(self.frm_wind_turb_output_eff)
        self.verticalLayout_37.setContentsMargins(-1, 30, -1, 30)
        self.verticalLayout_37.setObjectName("verticalLayout_37")
        self.label_209 = QtWidgets.QLabel(self.frm_wind_turb_output_eff)
        self.label_209.setMinimumSize(QtCore.QSize(200, 200))
        self.label_209.setMaximumSize(QtCore.QSize(200, 200))
        self.label_209.setText("")
        self.label_209.setPixmap(QtGui.QPixmap(":/icons/icons/efficiency.png"))
        self.label_209.setScaledContents(True)
        self.label_209.setAlignment(QtCore.Qt.AlignCenter)
        self.label_209.setObjectName("label_209")
        self.verticalLayout_37.addWidget(self.label_209, 0, QtCore.Qt.AlignHCenter)
        self.label_210 = QtWidgets.QLabel(self.frm_wind_turb_output_eff)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiLight")
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.label_210.setFont(font)
        self.label_210.setObjectName("label_210")
        self.verticalLayout_37.addWidget(self.label_210, 0, QtCore.Qt.AlignHCenter)
        self.line_26 = QtWidgets.QFrame(self.frm_wind_turb_output_eff)
        self.line_26.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_26.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_26.setObjectName("line_26")
        self.verticalLayout_37.addWidget(self.line_26)
        self.lbl_wind_turb_output_eff = QtWidgets.QLabel(self.frm_wind_turb_output_eff)
        font = QtGui.QFont()
        font.setFamily("Maiandra GD")
        font.setPointSize(36)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_wind_turb_output_eff.setFont(font)
        self.lbl_wind_turb_output_eff.setTextFormat(QtCore.Qt.PlainText)
        self.lbl_wind_turb_output_eff.setScaledContents(True)
        self.lbl_wind_turb_output_eff.setWordWrap(True)
        self.lbl_wind_turb_output_eff.setObjectName("lbl_wind_turb_output_eff")
        self.verticalLayout_37.addWidget(self.lbl_wind_turb_output_eff, 0, QtCore.Qt.AlignHCenter)
        self.label_211 = QtWidgets.QLabel(self.frm_wind_turb_output_eff)
        self.label_211.setMinimumSize(QtCore.QSize(30, 40))
        font = QtGui.QFont()
        font.setFamily("Maiandra GD")
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.label_211.setFont(font)
        self.label_211.setObjectName("label_211")
        self.verticalLayout_37.addWidget(self.label_211, 0, QtCore.Qt.AlignHCenter)
        self.gridLayout_57.addWidget(self.frm_wind_turb_output_eff, 0, 4, 1, 1)
        self.stk_wind_turb_main.addWidget(self.stk_wind_turb_main_output)
        self.gridLayout_22.addWidget(self.stk_wind_turb_main, 2, 0, 1, 1)
        self.stacked_main_windows.addWidget(self.stk_wind_turbine)

        # final result
        self.stk_final_result = QtWidgets.QWidget()
        self.stk_final_result.setObjectName("stk_final_result")
        self.frame = QtWidgets.QFrame(self.stk_final_result)
        self.frame.setGeometry(QtCore.QRect(9, 9, 170, 526))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_17 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_17.setObjectName("gridLayout_17")
        self.gb_final_solar_pv = QtWidgets.QGroupBox(self.frame)
        self.gb_final_solar_pv.setMinimumSize(QtCore.QSize(150, 250))
        self.gb_final_solar_pv.setMaximumSize(QtCore.QSize(180, 250))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.gb_final_solar_pv.setFont(font)
        self.gb_final_solar_pv.setAlignment(QtCore.Qt.AlignCenter)
        self.gb_final_solar_pv.setFlat(False)
        self.gb_final_solar_pv.setCheckable(True)
        self.gb_final_solar_pv.setChecked(True)
        self.gb_final_solar_pv.setObjectName("gb_final_solar_pv")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.gb_final_solar_pv)
        self.verticalLayout_12.setContentsMargins(13, 30, 15, -1)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.label_79 = QtWidgets.QLabel(self.gb_final_solar_pv)
        self.label_79.setMinimumSize(QtCore.QSize(60, 60))
        self.label_79.setMaximumSize(QtCore.QSize(60, 60))
        self.label_79.setText("")
        self.label_79.setPixmap(QtGui.QPixmap(":/icons/icons/solar-panel (1).png"))
        self.label_79.setScaledContents(True)
        self.label_79.setObjectName("label_79")
        self.verticalLayout_12.addWidget(self.label_79, 0, QtCore.Qt.AlignHCenter)
        self.lbl_solar_pv_pow = QtWidgets.QLabel(self.gb_final_solar_pv)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_solar_pv_pow.setFont(font)
        self.lbl_solar_pv_pow.setObjectName("lbl_solar_pv_pow")
        self.verticalLayout_12.addWidget(self.lbl_solar_pv_pow, 0, QtCore.Qt.AlignHCenter)
        self.gridLayout_17.addWidget(self.gb_final_solar_pv, 0, 0, 1, 1, QtCore.Qt.AlignLeft)
        self.gb_final_wind_turb = QtWidgets.QGroupBox(self.frame)
        self.gb_final_wind_turb.setMinimumSize(QtCore.QSize(150, 250))
        self.gb_final_wind_turb.setMaximumSize(QtCore.QSize(180, 250))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.gb_final_wind_turb.setFont(font)
        self.gb_final_wind_turb.setAlignment(QtCore.Qt.AlignCenter)
        self.gb_final_wind_turb.setFlat(False)
        self.gb_final_wind_turb.setCheckable(True)
        self.gb_final_wind_turb.setChecked(True)
        self.gb_final_wind_turb.setObjectName("gb_final_wind_turb")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.gb_final_wind_turb)
        self.verticalLayout_14.setContentsMargins(15, 30, 15, -1)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.label_83 = QtWidgets.QLabel(self.gb_final_wind_turb)
        self.label_83.setMinimumSize(QtCore.QSize(60, 60))
        self.label_83.setMaximumSize(QtCore.QSize(60, 60))
        self.label_83.setText("")
        self.label_83.setPixmap(QtGui.QPixmap(":/icons/icons/wind-engine.png"))
        self.label_83.setScaledContents(True)
        self.label_83.setObjectName("label_83")
        self.verticalLayout_14.addWidget(self.label_83, 0, QtCore.Qt.AlignHCenter)
        self.lbl_wind_turb_pow = QtWidgets.QLabel(self.gb_final_wind_turb)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_wind_turb_pow.setFont(font)
        self.lbl_wind_turb_pow.setObjectName("lbl_wind_turb_pow")
        self.verticalLayout_14.addWidget(self.lbl_wind_turb_pow, 0, QtCore.Qt.AlignHCenter)
        self.gridLayout_17.addWidget(self.gb_final_wind_turb, 1, 0, 1, 1, QtCore.Qt.AlignLeft)
        self.line_8 = QtWidgets.QFrame(self.stk_final_result)
        self.line_8.setGeometry(QtCore.QRect(275, 9, 16, 589))
        self.line_8.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.frame_5 = QtWidgets.QFrame(self.stk_final_result)
        self.frame_5.setGeometry(QtCore.QRect(290, 10, 721, 589))
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.verticalLayout_18 = QtWidgets.QVBoxLayout(self.frame_5)
        self.verticalLayout_18.setObjectName("verticalLayout_18")
        self.btn_referesh_final_result = QtWidgets.QToolButton(self.frame_5)
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.btn_referesh_final_result.setFont(font)
        self.btn_referesh_final_result.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/icons/icons/refresh-button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_referesh_final_result.setIcon(icon11)
        self.btn_referesh_final_result.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.btn_referesh_final_result.setAutoRaise(True)
        self.btn_referesh_final_result.setObjectName("btn_referesh_final_result")
        self.verticalLayout_18.addWidget(self.btn_referesh_final_result, 0, QtCore.Qt.AlignRight)
        self.frm_final_dmd_sup = QtWidgets.QFrame(self.frame_5)
        self.frm_final_dmd_sup.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frm_final_dmd_sup.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_final_dmd_sup.setObjectName("frm_final_dmd_sup")
        self.gridLayout_19 = QtWidgets.QGridLayout(self.frm_final_dmd_sup)
        self.gridLayout_19.setObjectName("gridLayout_19")
        self.lbl_final_pow_consumed = QtWidgets.QLabel(self.frm_final_dmd_sup)
        font = QtGui.QFont()
        font.setFamily("Maiandra GD")
        font.setPointSize(27)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_final_pow_consumed.setFont(font)
        self.lbl_final_pow_consumed.setObjectName("lbl_final_pow_consumed")
        self.gridLayout_19.addWidget(self.lbl_final_pow_consumed, 1, 0, 1, 1, QtCore.Qt.AlignTop)
        self.lbl_power_available_lbl = QtWidgets.QLabel(self.frm_final_dmd_sup)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.lbl_power_available_lbl.setFont(font)
        self.lbl_power_available_lbl.setObjectName("lbl_power_available_lbl")
        self.gridLayout_19.addWidget(self.lbl_power_available_lbl, 3, 0, 1, 1, QtCore.Qt.AlignBottom)
        self.lbl_final_pow_trend = QtWidgets.QLabel(self.frm_final_dmd_sup)
        self.lbl_final_pow_trend.setMinimumSize(QtCore.QSize(15, 15))
        self.lbl_final_pow_trend.setMaximumSize(QtCore.QSize(15, 15))
        self.lbl_final_pow_trend.setText("")
        self.lbl_final_pow_trend.setPixmap(QtGui.QPixmap(":/icons/icons/high.png"))
        self.lbl_final_pow_trend.setScaledContents(True)
        self.lbl_final_pow_trend.setObjectName("lbl_final_pow_trend")
        self.gridLayout_19.addWidget(self.lbl_final_pow_trend, 4, 1, 1, 1, QtCore.Qt.AlignTop)
        self.lbl_power_consumed_lbl = QtWidgets.QLabel(self.frm_final_dmd_sup)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.lbl_power_consumed_lbl.setFont(font)
        self.lbl_power_consumed_lbl.setObjectName("lbl_power_consumed_lbl")
        self.gridLayout_19.addWidget(self.lbl_power_consumed_lbl, 0, 0, 1, 1, QtCore.Qt.AlignBottom)
        self.lbl_final_pow_available = QtWidgets.QLabel(self.frm_final_dmd_sup)
        font = QtGui.QFont()
        font.setFamily("Maiandra GD")
        font.setPointSize(27)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_final_pow_available.setFont(font)
        self.lbl_final_pow_available.setObjectName("lbl_final_pow_available")
        self.gridLayout_19.addWidget(self.lbl_final_pow_available, 4, 0, 1, 1)
        spacerItem13 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_19.addItem(spacerItem13, 2, 0, 1, 1)
        self.wid_final_audit_graph = QtWidgets.QWidget(self.frm_final_dmd_sup)
        self.wid_final_audit_graph.setMinimumSize(QtCore.QSize(500, 0))
        self.wid_final_audit_graph.setObjectName("wid_final_audit_graph")
        self.gridLayout_19.addWidget(self.wid_final_audit_graph, 0, 2, 5, 1)
        self.verticalLayout_18.addWidget(self.frm_final_dmd_sup)
        self.wid_final_comp_graph = QtWidgets.QWidget(self.frame_5)
        self.wid_final_comp_graph.setMinimumSize(QtCore.QSize(200, 190))
        self.wid_final_comp_graph.setMaximumSize(QtCore.QSize(200, 190))
        self.wid_final_comp_graph.setObjectName("wid_final_comp_graph")
        self.verticalLayout_18.addWidget(self.wid_final_comp_graph, 0, QtCore.Qt.AlignHCenter)
        # end wind definition #

        # begin electric car stack widget definition #
        self.onlyFloat = QtGui.QDoubleValidator()  # validator for input field
        
        self.stk_electric_car_pv = QtWidgets.QWidget()
        self.stk_electric_car_pv.setObjectName("stk_electric_car_pv")

        self.gridLayout_electric_car = QtWidgets.QGridLayout(self.stk_electric_car_pv)
        self.gridLayout_electric_car.setObjectName("gridLayout_electric_car")

        self.horizontalFrame_electric_car = QtWidgets.QFrame(self.stk_electric_car_pv)
        self.horizontalFrame_electric_car.setMinimumSize(QtCore.QSize(0, 40))
        self.horizontalFrame_electric_car.setMaximumSize(QtCore.QSize(16777215, 70))
        self.horizontalFrame_electric_car.setObjectName("horizontalFrame_electric_car")

        self.horizontalLayout_electric_car = QtWidgets.QHBoxLayout(self.horizontalFrame_electric_car)
        self.horizontalLayout_electric_car.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout_electric_car.setContentsMargins(8, 8, -1, -1)
        self.horizontalLayout_electric_car.setSpacing(10)
        self.horizontalLayout_electric_car.setObjectName("horizontalLayout_electric_car")

        self.label_electric_car = QtWidgets.QLabel(self.horizontalFrame_electric_car)
        self.label_electric_car.setMinimumSize(QtCore.QSize(50, 50))
        self.label_electric_car.setMaximumSize(QtCore.QSize(50, 50))
        self.label_electric_car.setText("")
        self.label_electric_car.setPixmap(QtGui.QPixmap("icons/electric-car.png"))
        self.label_electric_car.setScaledContents(True)
        self.label_electric_car.setObjectName("label_electric_car")
        self.horizontalLayout_electric_car.addWidget(self.label_electric_car, 0, QtCore.Qt.AlignRight)

        self.line_electric_car = QtWidgets.QFrame(self.horizontalFrame_electric_car)  # line_4 -> line_electric_carF
        self.line_electric_car.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_electric_car.setLineWidth(2)
        self.line_electric_car.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_electric_car.setObjectName("line_electric_car")
        self.horizontalLayout_electric_car.addWidget(self.line_electric_car, 0, QtCore.Qt.AlignLeft)

        self.label_electric_car_2 = QtWidgets.QLabel(
            'ELECTRIC VEHICLE CHARGING STATION', self.horizontalFrame_electric_car
        )
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_electric_car_2.setFont(font)
        self.label_electric_car_2.setObjectName("label_electric_car_2")
        self.horizontalLayout_electric_car.addWidget(self.label_electric_car_2, 0, QtCore.Qt.AlignLeft)
        self.gridLayout_electric_car.addWidget(self.horizontalFrame_electric_car, 0, 0, 1, 1, QtCore.Qt.AlignLeft)

        self.line_electric_car_2 = QtWidgets.QFrame(self.stk_electric_car_pv)
        self.line_electric_car_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_electric_car_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_electric_car_2.setObjectName("line_electric_car_2")
        self.gridLayout_electric_car.addWidget(self.line_electric_car_2, 1, 0, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.gridLayout_electric_car.addItem(spacerItem, 2, 1, 1, 1)

        self.stk_electric_car_pv_main = QtWidgets.QStackedWidget(self.stk_electric_car_pv)
        self.stk_electric_car_pv_main.setObjectName("stk_electric_car_pv_main")


        # Electric Home Page

        # Power Data Page
        qTabPages_e_h_pages = QtWidgets.QTabWidget()
        qTabPages_e_h_pages.setObjectName('qTabPages_e_h_pages')

        qTabPage_e_h_power = QtWidgets.QWidget(qTabPages_e_h_pages)
        qTabPage_e_h_power.setObjectName('qTabPage_e_h_power')

        qVLayout_e_h_power = QtWidgets.QVBoxLayout(qTabPage_e_h_power)
        qVLayout_e_h_power.setObjectName('qVLayout_e_h_power')

        # Power Data Input
        qFrame_e_h_power = QtWidgets.QFrame(qTabPage_e_h_power)
        qFrame_e_h_power.setFrameShape(QtWidgets.QFrame.StyledPanel)
        qFrame_e_h_power.setFrameShadow(QtWidgets.QFrame.Raised)
        qFrame_e_h_power.setObjectName("qFrame_e_h_power")
        
        qGLayout_e_h_power = QtWidgets.QGridLayout(qFrame_e_h_power)
        qGLayout_e_h_power.setObjectName('qGLayout_e_h_power')

        label = QtWidgets.QLabel(
            'Location', qFrame_e_h_power
        )
        label.setObjectName('qLabel_e_h_location')
        qGLayout_e_h_power.addWidget(label, 1, 0, 1, 1)

        label = QtWidgets.QLabel(
            'Solar Power Generated', qFrame_e_h_power
        )
        label.setObjectName('qLabel_e_h_solar_power')
        qGLayout_e_h_power.addWidget(label, 2, 0, 1, 1)

        label = QtWidgets.QLabel(
            'Biomass Power Generated', qFrame_e_h_power
        )
        label.setObjectName('qLabel_e_h_biomass_power')
        qGLayout_e_h_power.addWidget(label, 3, 0, 1, 1)

        label = QtWidgets.QLabel(
            'Wind Power Generated', qFrame_e_h_power
        )
        label.setObjectName('qLabel_e_h_wind_power')
        qGLayout_e_h_power.addWidget(label, 4, 0, 1, 1)

        label = QtWidgets.QLabel(
            'EV Charger Name', qFrame_e_h_power
        )
        label.setObjectName('qLabel_e_h_ev_charger')
        qGLayout_e_h_power.addWidget(label, 5, 0, 1, 1)

        label = QtWidgets.QLabel(
            'Power Rating Of Slow EV Charger(s)', qFrame_e_h_power
        )
        label.setObjectName('qLabel_e_h_rating_s_charger')
        qGLayout_e_h_power.addWidget(label, 6, 0, 1, 1)

        label = QtWidgets.QLabel(
            'Power Rating Of Medium EV Charger(s)', qFrame_e_h_power
        )
        label.setObjectName('qLabel_e_h_rating_m_charger')
        qGLayout_e_h_power.addWidget(label, 7, 0, 1, 1)

        label = QtWidgets.QLabel(
            'Power Rating Of Fast EV Charger(s)', qFrame_e_h_power
        )
        label.setObjectName('qLabel_e_h_rating_f_charger')
        qGLayout_e_h_power.addWidget(label, 8, 0, 1, 1)

        label = QtWidgets.QLabel('No. Of Slow Ev Charger(s)', qFrame_e_h_power)
        label.setObjectName('qLabel_e_h_num_s_charger')
        qGLayout_e_h_power.addWidget(label, 9, 0, 1, 1)

        label = QtWidgets.QLabel('No. Of Medium EV Charger(s)', qFrame_e_h_power)
        label.setObjectName('qLabel_e_h_num_m_charger')
        qGLayout_e_h_power.addWidget(label, 10, 0, 1, 1)

        label = QtWidgets.QLabel('No. Of Fast EV Charger(s)', qFrame_e_h_power)
        label.setObjectName('qLabel_e_h_num_f_charger')
        qGLayout_e_h_power.addWidget(label, 11, 0, 1, 1)

        label = QtWidgets.QLabel('BESS Name', qFrame_e_h_power)
        label.setObjectName('qLabel_bess_name')
        qGLayout_e_h_power.addWidget(label, 12, 0, 1, 1)

        label = QtWidgets.QLabel('Maximum BESS Capacity', qFrame_e_h_power)
        label.setObjectName('qLabel_max_bess_capacity')
        qGLayout_e_h_power.addWidget(label, 13, 0, 1, 1)

        self.qComboBox_e_h_location = QtWidgets.QComboBox(qFrame_e_h_power)
        self.qComboBox_e_h_location.setObjectName('qComboBox_e_h_location')
        qGLayout_e_h_power.addWidget(self.qComboBox_e_h_location, 1, 1, 1, 1)

        self.qDoubleSB_e_h_solar_power_gen = QtWidgets.QDoubleSpinBox(
            qFrame_e_h_power
        )
        self.qDoubleSB_e_h_solar_power_gen.setMaximum(MAX_VALUE)
        self.qDoubleSB_e_h_solar_power_gen.setObjectName(
            'qDoubleSB_e_h_solar_power_gen'
        )
        qGLayout_e_h_power.addWidget(
            self.qDoubleSB_e_h_solar_power_gen, 2, 1, 1, 1
        )

        self.qDoubleSB_e_h_biomass_power_gen = QtWidgets.QDoubleSpinBox(
            qFrame_e_h_power
        )
        self.qDoubleSB_e_h_biomass_power_gen.setObjectName(
            'qDoubleSB_e_h_biomass_power_gen'
        )
        self.qDoubleSB_e_h_biomass_power_gen.setMaximum(MAX_VALUE)
        qGLayout_e_h_power.addWidget(
            self.qDoubleSB_e_h_biomass_power_gen, 3, 1, 1, 1
        )
        
        self.qDoubleSB_e_h_wind_power_gen = QtWidgets.QDoubleSpinBox(
            qFrame_e_h_power
        )
        self.qDoubleSB_e_h_wind_power_gen.setMaximum(MAX_VALUE)
        self.qDoubleSB_e_h_wind_power_gen.setObjectName(
            'qDoubleSB_e_h_wind_power_gen'
        )
        qGLayout_e_h_power.addWidget(
            self.qDoubleSB_e_h_wind_power_gen, 4, 1, 1, 1
        )
        self.qComboBox_e_h_charger_name = QtWidgets.QLineEdit(qFrame_e_h_power)
        self.qComboBox_e_h_charger_name.setObjectName('qComboBox_e_h_charger_name')
        qGLayout_e_h_power.addWidget(self.qComboBox_e_h_charger_name, 5, 1, 1, 1)

        self.qDoubleSB_rating_s_charger = QtWidgets.QDoubleSpinBox(
            qFrame_e_h_power
        )
        self.qDoubleSB_rating_s_charger.setMaximum(MAX_VALUE)
        self.qDoubleSB_rating_s_charger.setObjectName('qDoubleSB_rating_s_charger')
        qGLayout_e_h_power.addWidget(self.qDoubleSB_rating_s_charger, 6, 1, 1, 1)

        self.qDoubleSB_rating_m_charger = QtWidgets.QDoubleSpinBox(
            qFrame_e_h_power
        )
        self.qDoubleSB_rating_m_charger.setMaximum(MAX_VALUE)
        self.qDoubleSB_rating_m_charger.setObjectName('qDoubleSB_rating_m_charger')
        qGLayout_e_h_power.addWidget(self.qDoubleSB_rating_m_charger, 7, 1, 1, 1)

        self.qDoubleSB_rating_f_charger = QtWidgets.QDoubleSpinBox(
            qFrame_e_h_power
        )
        self.qDoubleSB_rating_f_charger.setMaximum(MAX_VALUE)
        self.qDoubleSB_rating_f_charger.setObjectName('qDoubleSB_rating_f_charger')
        qGLayout_e_h_power.addWidget(self.qDoubleSB_rating_f_charger, 8, 1, 1, 1)

        self.qDoubleSB_num_s_charger = QtWidgets.QDoubleSpinBox(
            qFrame_e_h_power
        )
        self.qDoubleSB_num_s_charger.setObjectName('qDoubleSB_num_s_charger')
        self.qDoubleSB_num_s_charger.setMaximum(MAX_VALUE)
        qGLayout_e_h_power.addWidget(self.qDoubleSB_num_s_charger, 9, 1, 1, 1)

        self.qDoubleSB_num_m_charger = QtWidgets.QDoubleSpinBox(
            qFrame_e_h_power
        )
        self.qDoubleSB_num_m_charger.setMaximum(MAX_VALUE)
        self.qDoubleSB_num_m_charger.setObjectName('qDoubleSB_num_m_charger')
        qGLayout_e_h_power.addWidget(self.qDoubleSB_num_m_charger, 10, 1, 1, 1)

        self.qDoubleSB_num_f_charger = QtWidgets.QDoubleSpinBox(
            qFrame_e_h_power
        )
        self.qDoubleSB_num_f_charger.setMaximum(MAX_VALUE)
        self.qDoubleSB_num_f_charger.setObjectName('qDoubleSB_num_f_charger')
        qGLayout_e_h_power.addWidget(self.qDoubleSB_num_f_charger, 11, 1, 1, 1)

        self.qComboBox_e_h_bess_name = QtWidgets.QLineEdit(qFrame_e_h_power)
        self.qComboBox_e_h_bess_name.setObjectName('qComboBox_e_h_bess_name')
        qGLayout_e_h_power.addWidget(self.qComboBox_e_h_bess_name, 12, 1, 1, 1)

        self.qDoubleSB_e_h_max_bess_capacity = QtWidgets.QDoubleSpinBox(
            qFrame_e_h_power
        )
        self.qDoubleSB_e_h_max_bess_capacity.setMaximum(MAX_VALUE)
        self.qDoubleSB_e_h_max_bess_capacity.setObjectName('qDoubleSB_e_h_max_bess_capacity')
        qGLayout_e_h_power.addWidget(self.qDoubleSB_e_h_max_bess_capacity, 13, 1, 1, 1)

        self.qCheckBox_e_h_save_power = QtWidgets.QCheckBox(
            'Save EVCS Power Data', qFrame_e_h_power
        )
        self.qCheckBox_e_h_save_power.setObjectName('qCheckBox_e_h_save_power')
        qGLayout_e_h_power.addWidget(self.qCheckBox_e_h_save_power, 14, 1, 1, 1)

        qVLayout_e_h_power.addWidget(qFrame_e_h_power)
        qTabPages_e_h_pages.addTab(qTabPage_e_h_power, 'Power Data') 
        ############# END POWER DATA #################################

        # Cost Data Page
        qTabPage_e_h_cost = QtWidgets.QWidget(qTabPages_e_h_pages)
        qTabPage_e_h_cost.setObjectName('qTabPage_e_h_cost')

        qVLayout_e_h_cost = QtWidgets.QVBoxLayout(qTabPage_e_h_cost)
        qVLayout_e_h_cost.setObjectName('qVLayout_e_h_cost')

        qFrame_e_h_cost_main = QtWidgets.QFrame(qTabPage_e_h_cost)
        qFrame_e_h_cost_main.setObjectName('qFrame_e_h_cost_main')

        qHLayout_cost_main = QtWidgets.QHBoxLayout(qFrame_e_h_cost_main)
        qHLayout_cost_main.setContentsMargins(0, 0, 0, 0)
        qHLayout_cost_main.setObjectName('qHLayout_cost_main')

        # Cost Data Input

        qFrame_e_h_cost_1 = QtWidgets.QFrame(qTabPage_e_h_cost)
        qFrame_e_h_cost_1.setFrameShadow(QtWidgets.QFrame.Raised)
        qFrame_e_h_cost_1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        qFrame_e_h_cost_1.setObjectName('qFrame_e_h_cost_1')

        qGLayout_e_h_cost = QtWidgets.QGridLayout(qFrame_e_h_cost_1)
        qGLayout_e_h_cost.setObjectName('qGLayout_e_h_cost')
        
        self.qComboBox_e_h_cost_location = QtWidgets.QComboBox(qFrame_e_h_cost_1)
        self.qComboBox_e_h_cost_location.setObjectName("qComboBox_e_h_cost_location")
        qGLayout_e_h_cost.addWidget(self.qComboBox_e_h_cost_location, 0, 1, 1, 1)
        
        self.qDoubleSB_e_h_cost_land = QtWidgets.QDoubleSpinBox(qFrame_e_h_cost_1)
        self.qDoubleSB_e_h_cost_land.setMaximum(MAX_VALUE)
        self.qDoubleSB_e_h_cost_land.setObjectName("qDoubleSB_e_h_cost_land")
        qGLayout_e_h_cost.addWidget(self.qDoubleSB_e_h_cost_land, 1, 1, 1, 1)
        
        self.qComboBox_e_h_cost_charger_name = QtWidgets.QComboBox(qFrame_e_h_cost_1)
        self.qComboBox_e_h_cost_charger_name.setObjectName("qComboBox_e_h_cost_charger_name")
        qGLayout_e_h_cost.addWidget(self.qComboBox_e_h_cost_charger_name, 2, 1, 1, 1)
        
        self.qDoubleSB_e_h_cost_s_charger = QtWidgets.QDoubleSpinBox(qFrame_e_h_cost_1)
        self.qDoubleSB_e_h_cost_s_charger.setMaximum(MAX_VALUE)
        self.qDoubleSB_e_h_cost_s_charger.setObjectName("qDoubleSB_e_h_cost_s_charger")
        qGLayout_e_h_cost.addWidget(self.qDoubleSB_e_h_cost_s_charger, 3, 1, 1, 1)
        
        self.qDoubleSB_e_h_cost_m_charger = QtWidgets.QDoubleSpinBox(qFrame_e_h_cost_1)
        self.qDoubleSB_e_h_cost_m_charger.setMaximum(MAX_VALUE)
        self.qDoubleSB_e_h_cost_m_charger.setObjectName("qDoubleSB_e_h_cost_m_charger")
        qGLayout_e_h_cost.addWidget(self.qDoubleSB_e_h_cost_m_charger, 4, 1, 1, 1)
        
        self.qDoubleSB_e_h_cost_f_charge = QtWidgets.QDoubleSpinBox(qFrame_e_h_cost_1)
        self.qDoubleSB_e_h_cost_f_charge.setMaximum(MAX_VALUE)
        self.qDoubleSB_e_h_cost_f_charge.setObjectName("qDoubleSB_e_h_cost_f_charge")
        qGLayout_e_h_cost.addWidget(self.qDoubleSB_e_h_cost_f_charge, 5, 1, 1, 1)
        
        self.qComboBox_e_h_cost_battery_name = QtWidgets.QComboBox(qFrame_e_h_cost_1)
        self.qComboBox_e_h_cost_battery_name.setObjectName("qComboBox_e_h_cost_battery_name")
        qGLayout_e_h_cost.addWidget(self.qComboBox_e_h_cost_battery_name, 6, 1, 1, 1)
        
        self.qDoubleSB_e_h_cost_battery = QtWidgets.QDoubleSpinBox(qFrame_e_h_cost_1)
        self.qDoubleSB_e_h_cost_battery.setMaximum(MAX_VALUE)
        self.qDoubleSB_e_h_cost_battery.setObjectName("qDoubleSB_e_h_cost_battery")
        qGLayout_e_h_cost.addWidget(self.qDoubleSB_e_h_cost_battery, 7, 1, 1, 1)

        self.qDoubleSB_e_h_cost_num_battery = QtWidgets.QSpinBox(qFrame_e_h_cost_1)
        self.qDoubleSB_e_h_cost_num_battery.setMaximum(MAX_VALUE)
        self.qDoubleSB_e_h_cost_num_battery.setObjectName("qDoubleSB_e_h_cost_num_battery")
        qGLayout_e_h_cost.addWidget(self.qDoubleSB_e_h_cost_num_battery, 8, 1, 1, 1)
        
        self.qComboBox_e_h_cost_solar_panel_name = QtWidgets.QComboBox(qFrame_e_h_cost_1)
        self.qComboBox_e_h_cost_solar_panel_name.setObjectName("qComboBox_e_h_cost_solar_panel_name")
        qGLayout_e_h_cost.addWidget(self.qComboBox_e_h_cost_solar_panel_name, 9, 1, 1, 1)
        
        self.qDoubleSB_e_h_cost_solar_panel = QtWidgets.QDoubleSpinBox(qFrame_e_h_cost_1)
        self.qDoubleSB_e_h_cost_solar_panel.setMaximum(MAX_VALUE)
        self.qDoubleSB_e_h_cost_solar_panel.setObjectName("qDoubleSB_e_h_cost_solar_panel")
        qGLayout_e_h_cost.addWidget(self.qDoubleSB_e_h_cost_solar_panel, 10, 1, 1, 1)
        
        self.qSpinBox_e_h_cost_num_solar_panel = QtWidgets.QSpinBox(qFrame_e_h_cost_1)
        self.qSpinBox_e_h_cost_num_solar_panel.setMaximum(MAX_VALUE)
        self.qSpinBox_e_h_cost_num_solar_panel.setObjectName("qSpinBox_e_h_cost_num_solar_panel")
        qGLayout_e_h_cost.addWidget(self.qSpinBox_e_h_cost_num_solar_panel, 11, 1, 1, 1)
        
        self.qDoubleSB_e_h_cost_combustor = QtWidgets.QDoubleSpinBox(qFrame_e_h_cost_1)
        self.qDoubleSB_e_h_cost_combustor.setMaximum(MAX_VALUE)
        self.qDoubleSB_e_h_cost_combustor.setObjectName("qDoubleSB_e_h_cost_combustor")
        qGLayout_e_h_cost.addWidget(self.qDoubleSB_e_h_cost_combustor, 12, 1, 1, 1)
        
        self.qDoubleSB_e_h_cost_boiler = QtWidgets.QDoubleSpinBox(qFrame_e_h_cost_1)
        self.qDoubleSB_e_h_cost_boiler.setMaximum(MAX_VALUE)
        self.qDoubleSB_e_h_cost_boiler.setObjectName("qDoubleSB_e_h_cost_boiler")
        qGLayout_e_h_cost.addWidget(self.qDoubleSB_e_h_cost_boiler, 13, 1, 1, 1)
        
        self.qDoubleSB_e_h_cost_steam_turbine = QtWidgets.QDoubleSpinBox(qFrame_e_h_cost_1)
        self.qDoubleSB_e_h_cost_steam_turbine.setMaximum(MAX_VALUE)
        self.qDoubleSB_e_h_cost_steam_turbine.setObjectName("qDoubleSB_e_h_cost_steam_turbine")
        qGLayout_e_h_cost.addWidget(self.qDoubleSB_e_h_cost_steam_turbine, 14, 1, 1, 1)
        
        self.qDoubleSB_e_h_cost_generator = QtWidgets.QDoubleSpinBox(qFrame_e_h_cost_1)
        self.qDoubleSB_e_h_cost_generator.setMaximum(MAX_VALUE)
        self.qDoubleSB_e_h_cost_generator.setObjectName("qDoubleSB_e_h_cost_generator")
        qGLayout_e_h_cost.addWidget(self.qDoubleSB_e_h_cost_generator, 15, 1, 1, 1)
        
        label = QtWidgets.QLabel('Location', qFrame_e_h_cost_1)
        label.setObjectName("qLabel_e_h_cost_location")
        qGLayout_e_h_cost.addWidget(label, 0, 0, 1, 1)

        label = QtWidgets.QLabel('Cost Of Land', qFrame_e_h_cost_1)
        label.setObjectName("qLabel_e_h_cost_land")
        qGLayout_e_h_cost.addWidget(label, 1, 0, 1, 1)
        
        label = QtWidgets.QLabel('EV Charger Name', qFrame_e_h_cost_1)
        label.setObjectName("qLabel_e_h_cost_ev_charger_name")
        qGLayout_e_h_cost.addWidget(label, 2, 0, 1, 1)
        
        label = QtWidgets.QLabel('Cost Of Slow Speed EV Charger', qFrame_e_h_cost_1)
        label.setObjectName("qLabel_e_h_cost_s_charger")
        qGLayout_e_h_cost.addWidget(label, 3, 0, 1, 1)
        
        label = QtWidgets.QLabel('Cost Of Medium Speed EV Charger', qFrame_e_h_cost_1)
        label.setObjectName("qLabel_e_h_cost_m_charger")
        qGLayout_e_h_cost.addWidget(label, 4, 0, 1, 1)
        
        label = QtWidgets.QLabel('Cost Of Fast Speed EV Charger', qFrame_e_h_cost_1)
        label.setObjectName("qLabel_e_h_cost_f_charger")
        qGLayout_e_h_cost.addWidget(label, 5, 0, 1, 1)

        label = QtWidgets.QLabel('Battery Name', qFrame_e_h_cost_1)
        label.setObjectName("qLabel_e_h_battery_name")
        qGLayout_e_h_cost.addWidget(label, 6, 0, 1, 1)
        
        label = QtWidgets.QLabel('Cost Of Single Battery', qFrame_e_h_cost_1)
        label.setObjectName("qLabel_e_h_cost_battery")
        qGLayout_e_h_cost.addWidget(label, 7, 0, 1, 1)
        
        label = QtWidgets.QLabel('No. Of Batteries', qFrame_e_h_cost_1)
        label.setObjectName("qLabel_e_h_cost_num_batteries")
        qGLayout_e_h_cost.addWidget(label, 8, 0, 1, 1)
        
        label = QtWidgets.QLabel('Solar Panel Name', qFrame_e_h_cost_1)
        label.setObjectName("qLabel_e_h_cost_solar_panel_name")
        qGLayout_e_h_cost.addWidget(label, 9, 0, 1, 1)
        
        label = QtWidgets.QLabel('Cost Of Single Solar Panel', qFrame_e_h_cost_1)
        label.setObjectName("qLabel_e_h_cost_single_solar_panel")
        qGLayout_e_h_cost.addWidget(label, 10, 0, 1, 1)

        label = QtWidgets.QLabel('No. Of Solar Panel', qFrame_e_h_cost_1)
        label.setObjectName("qLabel_e_h_num_solar_panel")
        qGLayout_e_h_cost.addWidget(label, 11, 0, 1, 1)
        
        label = QtWidgets.QLabel('Cost Of Combustor', qFrame_e_h_cost_1)
        label.setObjectName("qLabel_e_h_cost_combustor")
        qGLayout_e_h_cost.addWidget(label, 12, 0, 1, 1)
        
        label = QtWidgets.QLabel('Cost Of Boiler', qFrame_e_h_cost_1)
        label.setObjectName("qLabel_e_h_cost_boiler")
        qGLayout_e_h_cost.addWidget(label, 13, 0, 1, 1)
        
        label = QtWidgets.QLabel('Cost Of Steam Turbine', qFrame_e_h_cost_1)
        label.setObjectName("qLabel_e_h_cost_steam_turbine")
        qGLayout_e_h_cost.addWidget(label, 14, 0, 1, 1)
        
        label = QtWidgets.QLabel('Cost Of Generator', qFrame_e_h_cost_1)
        label.setObjectName("qLabel_e_h_cost_generator")
        qGLayout_e_h_cost.addWidget(label, 15, 0, 1, 1)

        qHLayout_cost_main.addWidget(qFrame_e_h_cost_1)

        
        # 2nd Grid
        qFrame_e_h_cost_2 = QtWidgets.QFrame(qTabPage_e_h_cost)
        qFrame_e_h_cost_2.setFrameShadow(QtWidgets.QFrame.Raised)
        qFrame_e_h_cost_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        qFrame_e_h_cost_2.setObjectName('qFrame_e_h_cost_2')

        qGLayout_e_h_cost_2 = QtWidgets.QGridLayout(qFrame_e_h_cost_2)
        qGLayout_e_h_cost_2.setObjectName('qGLayout_e_h_cost_2')

        self.qComboBox_e_h_cost_condeser = QtWidgets.QDoubleSpinBox(qFrame_e_h_cost_2)
        self.qComboBox_e_h_cost_condeser.setMaximum(MAX_VALUE)
        self.qComboBox_e_h_cost_condeser.setObjectName("qComboBox_e_h_cost_condeser")
        qGLayout_e_h_cost_2.addWidget(self.qComboBox_e_h_cost_condeser, 0, 1, 1, 1)

        self.qDoubleSB_e_h_cost_cooling_tower = QtWidgets.QDoubleSpinBox(qFrame_e_h_cost_2)
        self.qDoubleSB_e_h_cost_cooling_tower.setMaximum(MAX_VALUE)
        self.qDoubleSB_e_h_cost_cooling_tower.setObjectName("qDoubleSB_e_h_cost_cooling_tower")
        qGLayout_e_h_cost_2.addWidget(self.qDoubleSB_e_h_cost_cooling_tower, 1, 1, 1, 1)

        self.qDoubleSB_e_h_cost_pump = QtWidgets.QDoubleSpinBox(qFrame_e_h_cost_2)
        self.qDoubleSB_e_h_cost_pump.setMaximum(MAX_VALUE)
        self.qDoubleSB_e_h_cost_pump.setObjectName("qDoubleSB_e_h_cost_pump")
        qGLayout_e_h_cost_2.addWidget(self.qDoubleSB_e_h_cost_pump, 2, 1, 1, 1)

        self.qDoubleSB_e_h_cost_stack = QtWidgets.QDoubleSpinBox(qFrame_e_h_cost_2)
        self.qDoubleSB_e_h_cost_stack.setMaximum(MAX_VALUE)
        self.qDoubleSB_e_h_cost_stack.setObjectName("qDoubleSB_e_h_cost_stack")
        qGLayout_e_h_cost_2.addWidget(self.qDoubleSB_e_h_cost_stack, 3, 1, 1, 1)

        self.qDoubleSB_e_h_cost_wind_turbine = QtWidgets.QDoubleSpinBox(qFrame_e_h_cost_2)
        self.qDoubleSB_e_h_cost_wind_turbine.setMaximum(MAX_VALUE)
        self.qDoubleSB_e_h_cost_wind_turbine.setObjectName("qDoubleSB_e_h_cost_wind_turbine")
        qGLayout_e_h_cost_2.addWidget(self.qDoubleSB_e_h_cost_wind_turbine, 4, 1, 1, 1)

        self.qSpinBox_e_h_cost_num_wind_turbine = QtWidgets.QSpinBox(qFrame_e_h_cost_2)
        self.qSpinBox_e_h_cost_num_wind_turbine.setMaximum(MAX_VALUE)
        self.qSpinBox_e_h_cost_num_wind_turbine.setObjectName("qSpinBox_e_h_cost_num_wind_turbine")
        qGLayout_e_h_cost_2.addWidget(self.qSpinBox_e_h_cost_num_wind_turbine, 5, 1, 1, 1)

        self.qDoubleSB_e_h_cost_charging_rate = QtWidgets.QDoubleSpinBox(qFrame_e_h_cost_2)
        self.qDoubleSB_e_h_cost_charging_rate.setMaximum(MAX_VALUE)
        self.qDoubleSB_e_h_cost_charging_rate.setObjectName("qDoubleSB_e_h_cost_charging_rate")
        qGLayout_e_h_cost_2.addWidget(self.qDoubleSB_e_h_cost_charging_rate, 6, 1, 1, 1)

        self.qSpinBox_e_h_cost_time_s_charger = QtWidgets.QSpinBox(qFrame_e_h_cost_2)
        self.qSpinBox_e_h_cost_time_s_charger.setMaximum(MAX_VALUE)
        self.qSpinBox_e_h_cost_time_s_charger.setObjectName("qSpinBox_e_h_cost_time_s_charger")
        qGLayout_e_h_cost_2.addWidget(self.qSpinBox_e_h_cost_time_s_charger, 7, 1, 1, 1)

        self.qSpinBox_e_h_cost_time_m_charger = QtWidgets.QSpinBox(qFrame_e_h_cost_2)
        self.qSpinBox_e_h_cost_time_m_charger.setMaximum(MAX_VALUE)
        self.qSpinBox_e_h_cost_time_m_charger.setObjectName("qSpinBox_e_h_cost_time_m_charger")
        qGLayout_e_h_cost_2.addWidget(self.qSpinBox_e_h_cost_time_m_charger, 8, 1, 1, 1)

        self.qSpinBox_e_h_cost_time_f_charger = QtWidgets.QSpinBox(qFrame_e_h_cost_2)
        self.qSpinBox_e_h_cost_time_f_charger.setMaximum(MAX_VALUE)
        self.qSpinBox_e_h_cost_time_f_charger.setObjectName("qSpinBox_e_h_cost_time_f_charger")
        qGLayout_e_h_cost_2.addWidget(self.qSpinBox_e_h_cost_time_f_charger, 9, 1, 1, 1)

        self.qDoubleSB_e_h_cost_tariff_rate = QtWidgets.QDoubleSpinBox(qFrame_e_h_cost_2)
        self.qDoubleSB_e_h_cost_tariff_rate.setMaximum(MAX_VALUE)
        self.qDoubleSB_e_h_cost_tariff_rate.setObjectName("qDoubleSB_e_h_cost_tariff_rate")
        qGLayout_e_h_cost_2.addWidget(self.qDoubleSB_e_h_cost_tariff_rate, 10, 1, 1, 1)

        self.qSpinBox_e_h_cost_time_to_grid = QtWidgets.QSpinBox(qFrame_e_h_cost_2)
        self.qSpinBox_e_h_cost_time_to_grid.setMaximum(MAX_VALUE)
        self.qSpinBox_e_h_cost_time_to_grid.setObjectName("qSpinBox_e_h_cost_time_to_grid")
        qGLayout_e_h_cost_2.addWidget(self.qSpinBox_e_h_cost_time_to_grid, 11, 1, 1, 1)

        self.qDoubleSB_e_h_cost_maintenance = QtWidgets.QDoubleSpinBox(qFrame_e_h_cost_2)
        self.qDoubleSB_e_h_cost_maintenance.setMaximum(MAX_VALUE)
        self.qDoubleSB_e_h_cost_maintenance.setObjectName("qDoubleSB_e_h_cost_maintenance")
        qGLayout_e_h_cost_2.addWidget(self.qDoubleSB_e_h_cost_maintenance, 12, 1, 1, 1)
        
        self.qCheckBox_e_h_save_cost = QtWidgets.QCheckBox('Save EVCS Cost Data', qFrame_e_h_cost_2)
        self.qCheckBox_e_h_save_cost.setObjectName("qCheckBox_e_h_save_cost")
        qGLayout_e_h_cost_2.addWidget(self.qCheckBox_e_h_save_cost, 13, 1, 1, 1)

        label = QtWidgets.QLabel('Cost OF Condenser', qFrame_e_h_cost_2)
        label.setObjectName("qLabel_e_h_cost_condenser")
        qGLayout_e_h_cost_2.addWidget(label, 0, 0, 1, 1)

        label = QtWidgets.QLabel('Cost Of Cooling Tower', qFrame_e_h_cost_2)
        label.setObjectName("qLabel_e_h_cost_cooling_tower")
        qGLayout_e_h_cost_2.addWidget(label, 1, 0, 1, 1)

        label = QtWidgets.QLabel('Cost Of Pump', qFrame_e_h_cost_2)
        label.setObjectName("qLabel_e_h_cost_pump")
        qGLayout_e_h_cost_2.addWidget(label, 2, 0, 1, 1)

        label = QtWidgets.QLabel('Cost Of Stack', qFrame_e_h_cost_2)
        label.setObjectName("qLabel_e_h_cost_stack")
        qGLayout_e_h_cost_2.addWidget(label, 3, 0, 1, 1)

        label = QtWidgets.QLabel('Cost Of Wind Turbine', qFrame_e_h_cost_2)
        label.setObjectName("qLabel_e_h_cost_wind_turbine")
        qGLayout_e_h_cost_2.addWidget(label, 4, 0, 1, 1)

        label = QtWidgets.QLabel('No. Of Wind Turbine', qFrame_e_h_cost_2)
        label.setObjectName("qLabel_e_h_cost_num_wind_turbine")
        qGLayout_e_h_cost_2.addWidget(label, 5, 0, 1, 1)

        label = QtWidgets.QLabel('Charging Rate (N/KW)', qFrame_e_h_cost_2)
        label.setObjectName("qLabel_e_h_cost_charging_rate")
        qGLayout_e_h_cost_2.addWidget(label, 6, 0, 1, 1)

        label = QtWidgets.QLabel('Charging Time W/Slow Charger', qFrame_e_h_cost_2)
        label.setObjectName("qLabel_e_h_cost_time_s_charger")
        qGLayout_e_h_cost_2.addWidget(label, 7, 0, 1, 1)

        label = QtWidgets.QLabel('Charging Time W/Medium Charger', qFrame_e_h_cost_2)
        label.setObjectName("qLabel_e_h_cost_time_m_charger")
        qGLayout_e_h_cost_2.addWidget(label, 8, 0, 1, 1)

        label = QtWidgets.QLabel('Charging Time W/Fast Charger', qFrame_e_h_cost_2)
        label.setObjectName("qLabel_e_h_cost_time_f_charger")
        qGLayout_e_h_cost_2.addWidget(label, 9, 0, 1, 1)

        label = QtWidgets.QLabel(
            'Tariff Rate Transmitting To Grid (N/KW)', qFrame_e_h_cost_2
        )
        label.setObjectName("qLabel_e_h_cost_tariff_to_grid")
        qGLayout_e_h_cost_2.addWidget(label, 10, 0, 1, 1)

        label = QtWidgets.QLabel(
            'Power Transmission Time To Grid', qFrame_e_h_cost_2
        )
        label.setObjectName("qLabel_e_h_cost_trans_to_grid")
        qGLayout_e_h_cost_2.addWidget(label, 11, 0, 1, 1)

        label = QtWidgets.QLabel('Maintenance Cost For Charging Station', qFrame_e_h_cost_2)
        label.setObjectName("qLabel_e_h_cost_maintenance_charging")
        qGLayout_e_h_cost_2.addWidget(label, 12, 0, 1, 1)
        
        qHLayout_cost_main.addWidget(qFrame_e_h_cost_2)
        
        qVLayout_e_h_cost.addWidget(qFrame_e_h_cost_main)
        qTabPages_e_h_pages.addTab(qTabPage_e_h_cost, 'Cost Data')
               

        # self.stk_electric_car_pv_main.addWidget(self.gb_electric_car_stdt)
        self.stk_electric_car_pv_main.addWidget(qTabPages_e_h_pages)
        self.gridLayout_electric_car.addWidget(self.stk_electric_car_pv_main, 3, 0, 1, 2)
        self.stacked_main_windows.addWidget(self.stk_electric_car_pv)

        # end electric car stack definition #

        # solar result
        self.frame_3 = QtWidgets.QFrame(self.frame_5)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.gridLayout_25 = QtWidgets.QGridLayout(self.frame_3)
        self.gridLayout_25.setObjectName("gridLayout_25")
        self.frm_final_solarpv_comp = QtWidgets.QFrame(self.frame_3)
        self.frm_final_solarpv_comp.setMinimumSize(QtCore.QSize(220, 150))
        self.frm_final_solarpv_comp.setMaximumSize(QtCore.QSize(16777215, 200))
        self.frm_final_solarpv_comp.setFrameShape(QtWidgets.QFrame.Panel)
        self.frm_final_solarpv_comp.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_final_solarpv_comp.setLineWidth(2)
        self.frm_final_solarpv_comp.setObjectName("frm_final_solarpv_comp")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout(self.frm_final_solarpv_comp)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.frame_2 = QtWidgets.QFrame(self.frm_final_solarpv_comp)
        self.frame_2.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.label_91 = QtWidgets.QLabel(self.frame_2)
        self.label_91.setMinimumSize(QtCore.QSize(30, 30))
        self.label_91.setMaximumSize(QtCore.QSize(30, 30))
        self.label_91.setText("")
        self.label_91.setPixmap(QtGui.QPixmap(":/icons/icons/solar-panel (1).png"))
        self.label_91.setScaledContents(True)
        self.label_91.setObjectName("label_91")
        self.horizontalLayout_11.addWidget(self.label_91)
        self.label_90 = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.label_90.setFont(font)
        self.label_90.setObjectName("label_90")
        self.horizontalLayout_11.addWidget(self.label_90, 0, QtCore.Qt.AlignRight)
        self.verticalLayout_16.addWidget(self.frame_2)
        self.lbl_final_solar_pv_comp_per = QtWidgets.QLabel(self.frm_final_solarpv_comp)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_final_solar_pv_comp_per.setFont(font)
        self.lbl_final_solar_pv_comp_per.setObjectName("lbl_final_solar_pv_comp_per")
        self.verticalLayout_16.addWidget(self.lbl_final_solar_pv_comp_per, 0,
                                         QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom)
        self.lbl_final_solar_pv_comp_kw = QtWidgets.QLabel(self.frm_final_solarpv_comp)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_final_solar_pv_comp_kw.setFont(font)
        self.lbl_final_solar_pv_comp_kw.setObjectName("lbl_final_solar_pv_comp_kw")
        self.verticalLayout_16.addWidget(self.lbl_final_solar_pv_comp_kw, 0,
                                         QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.gridLayout_25.addWidget(self.frm_final_solarpv_comp, 1, 0, 1, 1, QtCore.Qt.AlignLeft)

        # wind result
        self.frm_final_wind_turb_comp = QtWidgets.QFrame(self.frame_3)
        self.frm_final_wind_turb_comp.setMinimumSize(QtCore.QSize(220, 150))
        self.frm_final_wind_turb_comp.setMaximumSize(QtCore.QSize(16777215, 200))
        self.frm_final_wind_turb_comp.setFrameShape(QtWidgets.QFrame.Panel)
        self.frm_final_wind_turb_comp.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_final_wind_turb_comp.setLineWidth(2)
        self.frm_final_wind_turb_comp.setObjectName("frm_final_wind_turb_comp")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout(self.frm_final_wind_turb_comp)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.frame_4 = QtWidgets.QFrame(self.frm_final_wind_turb_comp)
        self.frame_4.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.label_94 = QtWidgets.QLabel(self.frame_4)
        self.label_94.setMinimumSize(QtCore.QSize(30, 30))
        self.label_94.setMaximumSize(QtCore.QSize(30, 30))
        self.label_94.setText("")
        self.label_94.setPixmap(QtGui.QPixmap(":/icons/icons/wind-engine.png"))
        self.label_94.setScaledContents(True)
        self.label_94.setObjectName("label_94")
        self.horizontalLayout_14.addWidget(self.label_94, 0, QtCore.Qt.AlignLeft)
        self.label_95 = QtWidgets.QLabel(self.frame_4)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.label_95.setFont(font)
        self.label_95.setObjectName("label_95")
        self.horizontalLayout_14.addWidget(self.label_95, 0, QtCore.Qt.AlignRight)
        self.verticalLayout_15.addWidget(self.frame_4)
        self.lbl_final_wind_turb_comp_per = QtWidgets.QLabel(self.frm_final_wind_turb_comp)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_final_wind_turb_comp_per.setFont(font)
        self.lbl_final_wind_turb_comp_per.setObjectName("lbl_final_wind_turb_comp_per")
        self.verticalLayout_15.addWidget(self.lbl_final_wind_turb_comp_per, 0,
                                         QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom)
        self.lbl_final_wind_turb_comp_kw = QtWidgets.QLabel(self.frm_final_wind_turb_comp)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_final_wind_turb_comp_kw.setFont(font)
        self.lbl_final_wind_turb_comp_kw.setObjectName("lbl_final_wind_turb_comp_kw")
        self.verticalLayout_15.addWidget(self.lbl_final_wind_turb_comp_kw, 0,
                                         QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.gridLayout_25.addWidget(self.frm_final_wind_turb_comp, 1, 1, 1, 1)

        # battery
        self.verticalLayout_18.addWidget(self.frame_3, 0, QtCore.Qt.AlignTop)
        self.line_11 = QtWidgets.QFrame(self.stk_final_result)
        self.line_11.setGeometry(QtCore.QRect(1032, 9, 16, 589))
        self.line_11.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_11.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_11.setObjectName("line_11")
        self.frame.raise_()
        self.line_8.raise_()
        self.line_11.raise_()
        self.frame_5.raise_()
        self.stacked_main_windows.addWidget(self.stk_final_result)
        self.horizontalLayout_8.addWidget(self.stacked_main_windows)

        # EVCS result
        self.widget_result_evcs = QtWidgets.QWidget()
        self.widget_result_evcs.setObjectName('widget_evcs_result')

        qGLayout_evcs_result = QtWidgets.QGridLayout(self.widget_result_evcs)

        qFrame_evcs_result = QtWidgets.QFrame(self.widget_result_evcs)
        qFrame_evcs_result.setMinimumSize(QtCore.QSize(0, 40))
        qFrame_evcs_result.setMaximumSize(QtCore.QSize(16777215, 70))

        qHLayout_evcs_result = QtWidgets.QHBoxLayout(qFrame_evcs_result)
        qHLayout_evcs_result.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        qHLayout_evcs_result.setContentsMargins(8, 8, -1, -1)
        qHLayout_evcs_result.setSpacing(10)

        qLabel_evcs_result_logo = QtWidgets.QLabel(qFrame_evcs_result)
        qLabel_evcs_result_logo.setMinimumSize(QtCore.QSize(50, 50))
        qLabel_evcs_result_logo.setMaximumSize(QtCore.QSize(50, 50))
        qLabel_evcs_result_logo.setPixmap(QtGui.QPixmap("icons/electric-car.png"))
        qLabel_evcs_result_logo.setScaledContents(True)
        qHLayout_evcs_result.addWidget(
            qLabel_evcs_result_logo, 0, QtCore.Qt.AlignRight
        )

        vLine = QtWidgets.QFrame(qFrame_evcs_result)
        vLine.setFrameShadow(QtWidgets.QFrame.Plain)
        vLine.setLineWidth(2)
        vLine.setFrameShape(QtWidgets.QFrame.VLine)
        qHLayout_evcs_result.addWidget(vLine, 0, QtCore.Qt.AlignLeft)

        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)

        qLabel_evcs_result_title = QtWidgets.QLabel(
            'ELECTRIC VEHICLE CHARGING STATION - RESULT', qFrame_evcs_result
        )
        qLabel_evcs_result_title.setFont(font)
        qHLayout_evcs_result.addWidget(qLabel_evcs_result_title, 0, QtCore.Qt.AlignLeft)
        qGLayout_evcs_result.addWidget(qFrame_evcs_result, 0, 0, 1, 1, QtCore.Qt.AlignLeft)

        hLine = QtWidgets.QFrame(self.widget_result_evcs)
        hLine.setFrameShape(QtWidgets.QFrame.HLine)
        hLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        qGLayout_evcs_result.addWidget(hLine, 1, 0, 1, 2)

        spacerItem = QtWidgets.QSpacerItem(
            20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum
        )
        qGLayout_evcs_result.addItem(spacerItem, 2, 1, 1, 1)

        qTabPages_evcs_result = QtWidgets.QTabWidget()

        # Power Result
        qTab_evcs_power_result = QtWidgets.QWidget()

        self.gridLayout_result_evcs = QtWidgets.QGridLayout(qTab_evcs_power_result)
        self.gridLayout_result_evcs.setContentsMargins(2, 2, 2, 2)
        self.gridLayout_result_evcs.setObjectName("gridLayout_result_evcs")
        self.groupBox_result_evcs = QtWidgets.QGroupBox(qTab_evcs_power_result)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_result_evcs.setFont(font)
        self.groupBox_result_evcs.setObjectName("groupBox_result_evcs")
        self.verticalLayout_result_evcs = QtWidgets.QVBoxLayout(self.groupBox_result_evcs)
        self.verticalLayout_result_evcs.setObjectName("verticalLayout_result_evcs")
        self.frame_cont_result_evcs_1 = QtWidgets.QFrame(self.groupBox_result_evcs)
        self.frame_cont_result_evcs_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_cont_result_evcs_1.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_cont_result_evcs_1.setObjectName("frame_cont_result_evcs_1")
        self.horizontalLayout_result_evcs = QtWidgets.QHBoxLayout(self.frame_cont_result_evcs_1)
        self.horizontalLayout_result_evcs.setSpacing(10)
        self.horizontalLayout_result_evcs.setObjectName("horizontalLayout_result_evcs")
        self.label_result_evcs_solar = QtWidgets.QLabel(self.frame_cont_result_evcs_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_result_evcs_solar.sizePolicy().hasHeightForWidth())
        self.label_result_evcs_solar.setSizePolicy(sizePolicy)
        self.label_result_evcs_solar.setMinimumSize(QtCore.QSize(50, 50))
        self.label_result_evcs_solar.setMaximumSize(QtCore.QSize(50, 50))
        self.label_result_evcs_solar.setText("")
        self.label_result_evcs_solar.setPixmap(QtGui.QPixmap("icons/solar-panel (1).png"))
        self.label_result_evcs_solar.setScaledContents(True)
        self.label_result_evcs_solar.setObjectName("label_result_evcs_solar")
        self.horizontalLayout_result_evcs.addWidget(self.label_result_evcs_solar)
        self.label_29 = QtWidgets.QLabel(self.frame_cont_result_evcs_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_29.sizePolicy().hasHeightForWidth())
        self.label_29.setSizePolicy(sizePolicy)
        self.label_29.setMinimumSize(QtCore.QSize(50, 50))
        self.label_29.setMaximumSize(QtCore.QSize(50, 50))
        self.label_29.setText("")
        self.label_29.setPixmap(QtGui.QPixmap("icons/images (3).png"))
        self.label_29.setScaledContents(True)
        self.label_29.setObjectName("label_29")
        self.horizontalLayout_result_evcs.addWidget(self.label_29)
        self.label_result_evcs_wind_turbine = QtWidgets.QLabel(self.frame_cont_result_evcs_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_result_evcs_wind_turbine.sizePolicy().hasHeightForWidth())
        self.label_result_evcs_wind_turbine.setSizePolicy(sizePolicy)
        self.label_result_evcs_wind_turbine.setMinimumSize(QtCore.QSize(50, 50))
        self.label_result_evcs_wind_turbine.setMaximumSize(QtCore.QSize(50, 50))
        self.label_result_evcs_wind_turbine.setText("")
        self.label_result_evcs_wind_turbine.setPixmap(QtGui.QPixmap("icons/wind-engine.png"))
        self.label_result_evcs_wind_turbine.setScaledContents(True)
        self.label_result_evcs_wind_turbine.setObjectName("label_result_evcs_wind_turbine")
        self.horizontalLayout_result_evcs.addWidget(self.label_result_evcs_wind_turbine)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_result_evcs.addItem(spacerItem)
        self.label_arrow_1 = QtWidgets.QLabel(self.frame_cont_result_evcs_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_arrow_1.sizePolicy().hasHeightForWidth())
        self.label_arrow_1.setSizePolicy(sizePolicy)
        self.label_arrow_1.setMinimumSize(QtCore.QSize(50, 50))
        self.label_arrow_1.setMaximumSize(QtCore.QSize(50, 50))
        self.label_arrow_1.setText("")
        self.label_arrow_1.setPixmap(QtGui.QPixmap("icons/right-arrow (1).png"))
        self.label_arrow_1.setScaledContents(True)
        self.label_arrow_1.setObjectName("label_arrow_1")
        self.horizontalLayout_result_evcs.addWidget(self.label_arrow_1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_result_evcs.addItem(spacerItem1)
        self.label_result_evcs_power_generated = QtWidgets.QLabel(self.frame_cont_result_evcs_1)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label_result_evcs_power_generated.setFont(font)
        self.label_result_evcs_power_generated.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_result_evcs_power_generated.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_result_evcs_power_generated.setObjectName("label_result_evcs_power_generated")
        self.horizontalLayout_result_evcs.addWidget(self.label_result_evcs_power_generated)
        self.label_result_evcs_watts_1 = QtWidgets.QLabel(self.frame_cont_result_evcs_1)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label_result_evcs_watts_1.setFont(font)
        self.label_result_evcs_watts_1.setObjectName("label_result_evcs_watts_1")
        self.horizontalLayout_result_evcs.addWidget(self.label_result_evcs_watts_1)
        self.verticalLayout_result_evcs.addWidget(self.frame_cont_result_evcs_1)
        self.seperator_result_evcs_1 = QtWidgets.QFrame(self.groupBox_result_evcs)
        self.seperator_result_evcs_1.setFrameShape(QtWidgets.QFrame.HLine)
        self.seperator_result_evcs_1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.seperator_result_evcs_1.setObjectName("seperator_result_evcs_1")
        self.verticalLayout_result_evcs.addWidget(self.seperator_result_evcs_1)
        self.frame_cont_result_evcs_2 = QtWidgets.QFrame(self.groupBox_result_evcs)
        self.frame_cont_result_evcs_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_cont_result_evcs_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_cont_result_evcs_2.setObjectName("frame_cont_result_evcs_2")
        self.horizontalLayout_result_evcs_2 = QtWidgets.QHBoxLayout(self.frame_cont_result_evcs_2)
        self.horizontalLayout_result_evcs_2.setSpacing(10)
        self.horizontalLayout_result_evcs_2.setObjectName("horizontalLayout_result_evcs_2")
        self.label_result_evcs_battery_consumed = QtWidgets.QLabel(self.frame_cont_result_evcs_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_result_evcs_battery_consumed.sizePolicy().hasHeightForWidth())
        self.label_result_evcs_battery_consumed.setSizePolicy(sizePolicy)
        self.label_result_evcs_battery_consumed.setMinimumSize(QtCore.QSize(50, 50))
        self.label_result_evcs_battery_consumed.setMaximumSize(QtCore.QSize(50, 50))
        self.label_result_evcs_battery_consumed.setText("")
        self.label_result_evcs_battery_consumed.setPixmap(QtGui.QPixmap("icons/car-battery.png"))
        self.label_result_evcs_battery_consumed.setScaledContents(True)
        self.label_result_evcs_battery_consumed.setObjectName("label_result_evcs_battery_consumed")
        self.horizontalLayout_result_evcs_2.addWidget(self.label_result_evcs_battery_consumed)
        self.label_result_evcs_electric_car = QtWidgets.QLabel(self.frame_cont_result_evcs_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_result_evcs_electric_car.sizePolicy().hasHeightForWidth())
        self.label_result_evcs_electric_car.setSizePolicy(sizePolicy)
        self.label_result_evcs_electric_car.setMinimumSize(QtCore.QSize(50, 50))
        self.label_result_evcs_electric_car.setMaximumSize(QtCore.QSize(50, 50))
        self.label_result_evcs_electric_car.setText("")
        self.label_result_evcs_electric_car.setPixmap(QtGui.QPixmap("icons/electric-car.png"))
        self.label_result_evcs_electric_car.setScaledContents(True)
        self.label_result_evcs_electric_car.setObjectName("label_result_evcs_electric_car")
        self.horizontalLayout_result_evcs_2.addWidget(self.label_result_evcs_electric_car)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_result_evcs_2.addItem(spacerItem2)
        self.label_arrow_2 = QtWidgets.QLabel(self.frame_cont_result_evcs_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_arrow_2.sizePolicy().hasHeightForWidth())
        self.label_arrow_2.setSizePolicy(sizePolicy)
        self.label_arrow_2.setMinimumSize(QtCore.QSize(50, 50))
        self.label_arrow_2.setMaximumSize(QtCore.QSize(50, 50))
        self.label_arrow_2.setText("")
        self.label_arrow_2.setPixmap(QtGui.QPixmap("icons/right-arrow (1).png"))
        self.label_arrow_2.setScaledContents(True)
        self.label_arrow_2.setObjectName("label_arrow_2")
        self.horizontalLayout_result_evcs_2.addWidget(self.label_arrow_2)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_result_evcs_2.addItem(spacerItem3)
        self.label_result_evcs_power_consumed = QtWidgets.QLabel(self.frame_cont_result_evcs_2)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label_result_evcs_power_consumed.setFont(font)
        self.label_result_evcs_power_consumed.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_result_evcs_power_consumed.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_result_evcs_power_consumed.setObjectName("label_result_evcs_power_consumed")
        self.horizontalLayout_result_evcs_2.addWidget(self.label_result_evcs_power_consumed)
        self.label_result_evcs_watts_2 = QtWidgets.QLabel(self.frame_cont_result_evcs_2)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label_result_evcs_watts_2.setFont(font)
        self.label_result_evcs_watts_2.setObjectName("label_result_evcs_watts_2")
        self.horizontalLayout_result_evcs_2.addWidget(self.label_result_evcs_watts_2)
        self.verticalLayout_result_evcs.addWidget(self.frame_cont_result_evcs_2)
        self.seperator_result_evcs_2 = QtWidgets.QFrame(self.groupBox_result_evcs)
        self.seperator_result_evcs_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.seperator_result_evcs_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.seperator_result_evcs_2.setObjectName("seperator_result_evcs_2")
        self.verticalLayout_result_evcs.addWidget(self.seperator_result_evcs_2)
        self.frame_cont_result_evcs_3 = QtWidgets.QFrame(self.groupBox_result_evcs)
        self.frame_cont_result_evcs_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_cont_result_evcs_3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_cont_result_evcs_3.setObjectName("frame_cont_result_evcs_3")
        self.horizontalLayout_result_evcs_3 = QtWidgets.QHBoxLayout(self.frame_cont_result_evcs_3)
        self.horizontalLayout_result_evcs_3.setSpacing(10)
        self.horizontalLayout_result_evcs_3.setObjectName("horizontalLayout_result_evcs_3")
        self.label_result_evcs_power_supplied_1 = QtWidgets.QLabel(self.frame_cont_result_evcs_3)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label_result_evcs_power_supplied_1.setFont(font)
        self.label_result_evcs_power_supplied_1.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_result_evcs_power_supplied_1.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_result_evcs_power_supplied_1.setObjectName("label_result_evcs_power_supplied_1")
        self.horizontalLayout_result_evcs_3.addWidget(self.label_result_evcs_power_supplied_1)
        self.label_result_evcs_watts_3 = QtWidgets.QLabel(self.frame_cont_result_evcs_3)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label_result_evcs_watts_3.setFont(font)
        self.label_result_evcs_watts_3.setObjectName("label_result_evcs_watts_3")
        self.horizontalLayout_result_evcs_3.addWidget(self.label_result_evcs_watts_3)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_result_evcs_3.addItem(spacerItem4)
        self.label_supplied_text_1 = QtWidgets.QLabel(self.frame_cont_result_evcs_3)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_supplied_text_1.setFont(font)
        self.label_supplied_text_1.setObjectName("label_supplied_text_1")
        self.horizontalLayout_result_evcs_3.addWidget(self.label_supplied_text_1)
        self.label_arrow_3 = QtWidgets.QLabel(self.frame_cont_result_evcs_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_arrow_3.sizePolicy().hasHeightForWidth())
        self.label_arrow_3.setSizePolicy(sizePolicy)
        self.label_arrow_3.setMinimumSize(QtCore.QSize(50, 50))
        self.label_arrow_3.setMaximumSize(QtCore.QSize(50, 50))
        self.label_arrow_3.setText("")
        self.label_arrow_3.setPixmap(QtGui.QPixmap("icons/right-arrow (1).png"))
        self.label_arrow_3.setScaledContents(True)
        self.label_arrow_3.setObjectName("label_arrow_3")
        self.horizontalLayout_result_evcs_3.addWidget(self.label_arrow_3)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_result_evcs_3.addItem(spacerItem5)
        self.label_result_evcs_battery = QtWidgets.QLabel(self.frame_cont_result_evcs_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_result_evcs_battery.sizePolicy().hasHeightForWidth())
        self.label_result_evcs_battery.setSizePolicy(sizePolicy)
        self.label_result_evcs_battery.setMinimumSize(QtCore.QSize(50, 50))
        self.label_result_evcs_battery.setMaximumSize(QtCore.QSize(50, 50))
        self.label_result_evcs_battery.setText("")
        self.label_result_evcs_battery.setPixmap(QtGui.QPixmap("icons/car-battery.png"))
        self.label_result_evcs_battery.setScaledContents(True)
        self.label_result_evcs_battery.setObjectName("label_result_evcs_battery")
        self.horizontalLayout_result_evcs_3.addWidget(self.label_result_evcs_battery)
        self.verticalLayout_result_evcs.addWidget(self.frame_cont_result_evcs_3)
        self.seperator_result_evcs_3 = QtWidgets.QFrame(self.groupBox_result_evcs)
        self.seperator_result_evcs_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.seperator_result_evcs_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.seperator_result_evcs_3.setObjectName("seperator_result_evcs_3")
        self.verticalLayout_result_evcs.addWidget(self.seperator_result_evcs_3)
        self.frame_cont_result_evcs_4 = QtWidgets.QFrame(self.groupBox_result_evcs)
        self.frame_cont_result_evcs_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_cont_result_evcs_4.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_cont_result_evcs_4.setObjectName("frame_cont_result_evcs_4")
        self.horizontalLayout_result_evcs_4 = QtWidgets.QHBoxLayout(self.frame_cont_result_evcs_4)
        self.horizontalLayout_result_evcs_4.setSpacing(10)
        self.horizontalLayout_result_evcs_4.setObjectName("horizontalLayout_result_evcs_4")
        self.label_result_evcs_power_supplied_2 = QtWidgets.QLabel(self.frame_cont_result_evcs_4)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label_result_evcs_power_supplied_2.setFont(font)
        self.label_result_evcs_power_supplied_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_result_evcs_power_supplied_2.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_result_evcs_power_supplied_2.setObjectName("label_result_evcs_power_supplied_2")
        self.horizontalLayout_result_evcs_4.addWidget(self.label_result_evcs_power_supplied_2)
        self.label_result_evcs_watts_4 = QtWidgets.QLabel(self.frame_cont_result_evcs_4)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label_result_evcs_watts_4.setFont(font)
        self.label_result_evcs_watts_4.setObjectName("label_result_evcs_watts_4")
        self.horizontalLayout_result_evcs_4.addWidget(self.label_result_evcs_watts_4)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_result_evcs_4.addItem(spacerItem6)
        self.label_supplied_text_2 = QtWidgets.QLabel(self.frame_cont_result_evcs_4)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_supplied_text_2.setFont(font)
        self.label_supplied_text_2.setObjectName("label_supplied_text_2")
        self.horizontalLayout_result_evcs_4.addWidget(self.label_supplied_text_2)
        self.label_arrow_4 = QtWidgets.QLabel(self.frame_cont_result_evcs_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_arrow_4.sizePolicy().hasHeightForWidth())
        self.label_arrow_4.setSizePolicy(sizePolicy)
        self.label_arrow_4.setMinimumSize(QtCore.QSize(50, 50))
        self.label_arrow_4.setMaximumSize(QtCore.QSize(50, 50))
        self.label_arrow_4.setText("")
        self.label_arrow_4.setPixmap(QtGui.QPixmap("icons/right-arrow (1).png"))
        self.label_arrow_4.setScaledContents(True)
        self.label_arrow_4.setObjectName("label_arrow_4")
        self.horizontalLayout_result_evcs_4.addWidget(self.label_arrow_4)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_result_evcs_4.addItem(spacerItem7)
        self.label_result_evcs_transmission = QtWidgets.QLabel(self.frame_cont_result_evcs_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_result_evcs_transmission.sizePolicy().hasHeightForWidth())
        self.label_result_evcs_transmission.setSizePolicy(sizePolicy)
        self.label_result_evcs_transmission.setMinimumSize(QtCore.QSize(50, 50))
        self.label_result_evcs_transmission.setMaximumSize(QtCore.QSize(50, 50))
        self.label_result_evcs_transmission.setText("")
        self.label_result_evcs_transmission.setPixmap(QtGui.QPixmap("icons/solar-panel (1).png"))
        self.label_result_evcs_transmission.setScaledContents(True)
        self.label_result_evcs_transmission.setObjectName("label_result_evcs_transmission")
        self.horizontalLayout_result_evcs_4.addWidget(self.label_result_evcs_transmission)
        self.verticalLayout_result_evcs.addWidget(self.frame_cont_result_evcs_4)
        self.gridLayout_result_evcs.addWidget(self.groupBox_result_evcs, 1, 0, 1, 1)
        self.label_help = QtWidgets.QLabel(qTab_evcs_power_result)
        self.label_help.setAlignment(QtCore.Qt.AlignCenter)
        self.label_help.setObjectName("label_help")
        self.gridLayout_result_evcs.addWidget(self.label_help, 2, 0, 1, 1)
        qTabPages_evcs_result.addTab(qTab_evcs_power_result, 'Power')

        # Cost Result
        qTab_evcs_cost_result = QtWidgets.QWidget()
        qHLayout_evcs_cost_result = QtWidgets.QHBoxLayout(
            qTab_evcs_cost_result
        )
        qHLayout_evcs_cost_result.setContentsMargins(20, 20, 20, 20)

        qFrame_evcs_cost_result = QtWidgets.QFrame(qTab_evcs_cost_result)
        qFrame_evcs_cost_result.setFrameShape(QtWidgets.QFrame.NoFrame)
        qFrame_evcs_cost_result.setFrameShadow(QtWidgets.QFrame.Plain)

        qVLayout_evcs_cost_result = QtWidgets.QVBoxLayout(qFrame_evcs_cost_result)
        qVLayout_evcs_cost_result.setContentsMargins(0, 0, 0, 0)
        qVLayout_evcs_cost_result.setSpacing(0)

        qFrame_evcs_cost_result_1 = QtWidgets.QFrame(qFrame_evcs_cost_result)
        qFrame_evcs_cost_result_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        qFrame_evcs_cost_result_1.setFrameShadow(QtWidgets.QFrame.Plain)

        qGLayout_evcs_cost_result = QtWidgets.QGridLayout(qFrame_evcs_cost_result_1)
        qGLayout_evcs_cost_result.setSpacing(0)

        self.qLabel_evcs_naira_investment = QtWidgets.QLabel(
            qFrame_evcs_cost_result_1
        )
        self.qLabel_evcs_naira_investment.setMinimumSize(QtCore.QSize(45, 45))
        self.qLabel_evcs_naira_investment.setMaximumSize(QtCore.QSize(45, 45))
        self.qLabel_evcs_naira_investment.setPixmap(
            QtGui.QPixmap("icons/naira.png")
        )
        self.qLabel_evcs_naira_investment.setScaledContents(True)
        qGLayout_evcs_cost_result.addWidget(
            self.qLabel_evcs_naira_investment, 0, 0, 1, 1
        )

        qVLayout_evcs_cost_result.addWidget(qFrame_evcs_cost_result_1)
        
        qFrame_evcs_cost_result_2 = QtWidgets.QFrame(qFrame_evcs_cost_result)
        qFrame_evcs_cost_result_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        qFrame_evcs_cost_result_2.setFrameShadow(QtWidgets.QFrame.Plain)

        qGLayout_evcs_cost_result_2 = QtWidgets.QGridLayout(
            qFrame_evcs_cost_result_2
        )

        self.qLabel_evcs_8 = QtWidgets.QLabel(qFrame_evcs_cost_result_2)
        self.qLabel_evcs_8.setMinimumSize(QtCore.QSize(45, 45))
        self.qLabel_evcs_8.setMaximumSize(QtCore.QSize(45, 45))
        self.qLabel_evcs_8.setPixmap(
            QtGui.QPixmap("icons/naira.png")
        )
        self.qLabel_evcs_8.setScaledContents(True)
        qGLayout_evcs_cost_result_2.addWidget(
            self.qLabel_evcs_8, 0, 0, 1, 1
        )

        qVLayout_evcs_cost_result.addWidget(qFrame_evcs_cost_result_2)

        qFrame_evcs_cost_result_3 = QtWidgets.QFrame(qFrame_evcs_cost_result)
        qFrame_evcs_cost_result_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        qFrame_evcs_cost_result_3.setFrameShadow(QtWidgets.QFrame.Plain)

        qHLayout_evcs_cost_result_2 = QtWidgets.QHBoxLayout(qFrame_evcs_cost_result_3)

        self.qLabel_evcs_10 = QtWidgets.QLabel(qFrame_evcs_cost_result_3)
        self.qLabel_evcs_10.setMinimumSize(QtCore.QSize(45, 45))
        self.qLabel_evcs_10.setMaximumSize(QtCore.QSize(45, 45))
        self.qLabel_evcs_10.setPixmap(
            QtGui.QPixmap("icons/naira.png")
        )
        #self.qLabel_evcs_10.setText("NApple")
        self.qLabel_evcs_10.setScaledContents(True)
        qHLayout_evcs_cost_result_2.addWidget(self.qLabel_evcs_10)
        qVLayout_evcs_cost_result.addWidget(qFrame_evcs_cost_result_3)

        qFrame_evcs_cost_result_4 = QtWidgets.QFrame(qFrame_evcs_cost_result)
        qFrame_evcs_cost_result_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        qFrame_evcs_cost_result_4.setFrameShadow(QtWidgets.QFrame.Plain)

        qHLayout_evcs_cost_result_3 = QtWidgets.QHBoxLayout(
            qFrame_evcs_cost_result_4
        )
        self.qLabel_evcs_11 = QtWidgets.QLabel(qFrame_evcs_cost_result_4)
        self.qLabel_evcs_11.setMinimumSize(QtCore.QSize(45, 45))
        self.qLabel_evcs_11.setMaximumSize(QtCore.QSize(45, 45))
        self.qLabel_evcs_11.setPixmap(
            QtGui.QPixmap("icons/naira.png")
        )
        self.qLabel_evcs_11.setScaledContents(True)
        qHLayout_evcs_cost_result_3.addWidget(self.qLabel_evcs_11)
        qVLayout_evcs_cost_result.addWidget(qFrame_evcs_cost_result_4)

        qFrame_evcs_cost_result_19 = QtWidgets.QFrame(qFrame_evcs_cost_result)
        qFrame_evcs_cost_result_19.setFrameShape(QtWidgets.QFrame.NoFrame)
        qFrame_evcs_cost_result_19.setFrameShadow(QtWidgets.QFrame.Plain)

        qHLayout_evcs_cost_result_13 = QtWidgets.QHBoxLayout(
            qFrame_evcs_cost_result_19
        )
        self.qLabel_evcs_24 = QtWidgets.QLabel(qFrame_evcs_cost_result_19)
        self.qLabel_evcs_24.setMinimumSize(QtCore.QSize(45, 45))
        self.qLabel_evcs_24.setMaximumSize(QtCore.QSize(45, 45))
        self.qLabel_evcs_24.setPixmap(
            QtGui.QPixmap("icons/naira.png")
        )
        self.qLabel_evcs_24.setScaledContents(True)
        qHLayout_evcs_cost_result_13.addWidget(self.qLabel_evcs_24)
        qVLayout_evcs_cost_result.addWidget(qFrame_evcs_cost_result_19)

        qFrame_evcs_cost_result_20 = QtWidgets.QFrame(qFrame_evcs_cost_result)
        qFrame_evcs_cost_result_20.setFrameShape(QtWidgets.QFrame.NoFrame)
        qFrame_evcs_cost_result_20.setFrameShadow(QtWidgets.QFrame.Plain)

        qHLayout_evcs_cost_result_14 = QtWidgets.QHBoxLayout(
            qFrame_evcs_cost_result_20
        )
        self.qLabel_evcs_25 = QtWidgets.QLabel(qFrame_evcs_cost_result_20)
        self.qLabel_evcs_25.setMinimumSize(QtCore.QSize(45, 45))
        self.qLabel_evcs_25.setMaximumSize(QtCore.QSize(45, 45))
        self.qLabel_evcs_25.setPixmap(
            QtGui.QPixmap("icons/naira.png")
        )
        self.qLabel_evcs_25.setScaledContents(True)
        qHLayout_evcs_cost_result_14.addWidget(self.qLabel_evcs_25)
        qVLayout_evcs_cost_result.addWidget(qFrame_evcs_cost_result_20)
        qHLayout_evcs_cost_result.addWidget(qFrame_evcs_cost_result)

        qFrame_evcs_cost_result_5 = QtWidgets.QFrame(qTab_evcs_cost_result)
        qFrame_evcs_cost_result_5.setFrameShape(QtWidgets.QFrame.NoFrame)
        qFrame_evcs_cost_result_5.setFrameShadow(QtWidgets.QFrame.Plain)

        qVLayout_evcs_cost_result_2 = QtWidgets.QVBoxLayout(
            qFrame_evcs_cost_result_5
        )
        qVLayout_evcs_cost_result_2.setContentsMargins(0, 0, 0, 0)
        qVLayout_evcs_cost_result_2.setSpacing(0)

        qFrame_evcs_cost_result_6 = QtWidgets.QFrame(qFrame_evcs_cost_result_5)
        qFrame_evcs_cost_result_6.setFrameShape(QtWidgets.QFrame.NoFrame)
        qFrame_evcs_cost_result_6.setFrameShadow(QtWidgets.QFrame.Plain)

        qGLayout_evcs_cost_result_3 = QtWidgets.QGridLayout(
            qFrame_evcs_cost_result_6
        )
        qGLayout_evcs_cost_result_3.setSpacing(0)

        self.qLabel_evcs_12 = QtWidgets.QLabel(qFrame_evcs_cost_result_6)
        self.qLabel_evcs_12.setMinimumSize(QtCore.QSize(45, 45))
        self.qLabel_evcs_12.setMaximumSize(QtCore.QSize(45, 45))
        self.qLabel_evcs_12.setPixmap(QtGui.QPixmap(":/icons/icons/right-arrow (1).png"))
        self.qLabel_evcs_12.setScaledContents(True)
        qGLayout_evcs_cost_result_3.addWidget(self.qLabel_evcs_12, 0, 1, 1, 1)
        qVLayout_evcs_cost_result_2.addWidget(qFrame_evcs_cost_result_6)

        qFrame_evcs_cost_result_7 = QtWidgets.QFrame(qFrame_evcs_cost_result_5)
        qFrame_evcs_cost_result_7.setFrameShape(QtWidgets.QFrame.NoFrame)
        qFrame_evcs_cost_result_7.setFrameShadow(QtWidgets.QFrame.Plain)

        qGLayout_evcs_cost_result_4 = QtWidgets.QGridLayout(
            qFrame_evcs_cost_result_7
        )

        self.qLabel_evcs_13 = QtWidgets.QLabel(qFrame_evcs_cost_result_7)
        self.qLabel_evcs_13.setMinimumSize(QtCore.QSize(45, 45))
        self.qLabel_evcs_13.setMaximumSize(QtCore.QSize(45, 45))
        self.qLabel_evcs_13.setPixmap(
            QtGui.QPixmap(":/icons/icons/right-arrow (1).png")
        )
        self.qLabel_evcs_13.setScaledContents(True)
        qGLayout_evcs_cost_result_4.addWidget(self.qLabel_evcs_13, 0, 1, 1, 1)
        qVLayout_evcs_cost_result_2.addWidget(qFrame_evcs_cost_result_7)

        qFrame_evcs_cost_result_8 = QtWidgets.QFrame(qFrame_evcs_cost_result_5)
        qFrame_evcs_cost_result_8.setFrameShape(QtWidgets.QFrame.NoFrame)
        qFrame_evcs_cost_result_8.setFrameShadow(QtWidgets.QFrame.Plain)
        
        qHLayout_evcs_cost_result_4 = QtWidgets.QHBoxLayout(qFrame_evcs_cost_result_8)
        
        self.qLabel_evcs_14 = QtWidgets.QLabel(qFrame_evcs_cost_result_8)
        self.qLabel_evcs_14.setMinimumSize(QtCore.QSize(45, 45))
        self.qLabel_evcs_14.setMaximumSize(QtCore.QSize(45, 45))
        self.qLabel_evcs_14.setPixmap(QtGui.QPixmap(":/icons/icons/right-arrow (1).png"))
        self.qLabel_evcs_14.setScaledContents(True)
        qHLayout_evcs_cost_result_4.addWidget(self.qLabel_evcs_14)
        qVLayout_evcs_cost_result_2.addWidget(qFrame_evcs_cost_result_8)

        qFrame_evcs_cost_result_9 = QtWidgets.QFrame(qFrame_evcs_cost_result_5)
        qFrame_evcs_cost_result_9.setFrameShape(QtWidgets.QFrame.NoFrame)
        qFrame_evcs_cost_result_9.setFrameShadow(QtWidgets.QFrame.Plain)
        
        qHLayout_evcs_cost_result_5 = QtWidgets.QHBoxLayout(qFrame_evcs_cost_result_9)
        
        self.qLabel_evcs_15 = QtWidgets.QLabel(qFrame_evcs_cost_result_9)
        self.qLabel_evcs_15.setMinimumSize(QtCore.QSize(45, 45))
        self.qLabel_evcs_15.setMaximumSize(QtCore.QSize(45, 45))
        self.qLabel_evcs_15.setPixmap(QtGui.QPixmap(":/icons/icons/right-arrow (1).png"))
        self.qLabel_evcs_15.setScaledContents(True)
        qHLayout_evcs_cost_result_5.addWidget(self.qLabel_evcs_15)
        qVLayout_evcs_cost_result_2.addWidget(qFrame_evcs_cost_result_9)

        qFrame_evcs_cost_result_17 = QtWidgets.QFrame(qFrame_evcs_cost_result_5)
        qFrame_evcs_cost_result_17.setFrameShape(QtWidgets.QFrame.NoFrame)
        qFrame_evcs_cost_result_17.setFrameShadow(QtWidgets.QFrame.Plain)
        
        qHLayout_evcs_cost_result_11 = QtWidgets.QHBoxLayout(qFrame_evcs_cost_result_17)
        
        self.qLabel_evcs_22 = QtWidgets.QLabel(qFrame_evcs_cost_result_17)
        self.qLabel_evcs_22.setMinimumSize(QtCore.QSize(45, 45))
        self.qLabel_evcs_22.setMaximumSize(QtCore.QSize(45, 45))
        self.qLabel_evcs_22.setPixmap(QtGui.QPixmap(":/icons/icons/right-arrow (1).png"))
        self.qLabel_evcs_22.setScaledContents(True)
        qHLayout_evcs_cost_result_11.addWidget(self.qLabel_evcs_22)
        qVLayout_evcs_cost_result_2.addWidget(qFrame_evcs_cost_result_17)

        qFrame_evcs_cost_result_18 = QtWidgets.QFrame(qFrame_evcs_cost_result_5)
        qFrame_evcs_cost_result_18.setFrameShape(QtWidgets.QFrame.NoFrame)
        qFrame_evcs_cost_result_18.setFrameShadow(QtWidgets.QFrame.Plain)
        
        qHLayout_evcs_cost_result_12 = QtWidgets.QHBoxLayout(qFrame_evcs_cost_result_18)
        
        self.qLabel_evcs_23 = QtWidgets.QLabel(qFrame_evcs_cost_result_18)
        self.qLabel_evcs_23.setMinimumSize(QtCore.QSize(45, 45))
        self.qLabel_evcs_23.setMaximumSize(QtCore.QSize(45, 45))
        self.qLabel_evcs_23.setPixmap(QtGui.QPixmap(":/icons/icons/right-arrow (1).png"))
        self.qLabel_evcs_23.setScaledContents(True)
        qHLayout_evcs_cost_result_12.addWidget(self.qLabel_evcs_23)
        qVLayout_evcs_cost_result_2.addWidget(qFrame_evcs_cost_result_18)
        qHLayout_evcs_cost_result.addWidget(qFrame_evcs_cost_result_5)

        qFrame_evcs_cost_result_10 = QtWidgets.QFrame(qFrame_evcs_result)
        qFrame_evcs_cost_result_10.setFrameShape(QtWidgets.QFrame.NoFrame)
        qFrame_evcs_cost_result_10.setFrameShadow(QtWidgets.QFrame.Plain)

        qVLayout_evcs_cost_result_3 = QtWidgets.QVBoxLayout(qFrame_evcs_cost_result_10)
        qVLayout_evcs_cost_result_3.setSpacing(0)
        qVLayout_evcs_cost_result_3.setContentsMargins(0, 0, 0, 0)

        qFrame_evcs_cost_result_11 = QtWidgets.QFrame(qFrame_evcs_cost_result_10)
        qFrame_evcs_cost_result_11.setFrameShape(QtWidgets.QFrame.NoFrame)
        qFrame_evcs_cost_result_11.setFrameShadow(QtWidgets.QFrame.Plain)

        qHLayout_evcs_cost_result_6 = QtWidgets.QHBoxLayout(
            qFrame_evcs_cost_result_11
        )

        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)

        self.qLabel_evcs_16 = QtWidgets.QLabel(
            '#', qFrame_evcs_cost_result_11
        )
        self.qLabel_evcs_16.setFont(font)
        self.qLabel_evcs_16.setAlignment(QtCore.Qt.AlignCenter)
        qHLayout_evcs_cost_result_6.addWidget(self.qLabel_evcs_16)
        qVLayout_evcs_cost_result_3.addWidget(qFrame_evcs_cost_result_11)

        qFrame_evcs_cost_result_12 = QtWidgets.QFrame(qFrame_evcs_cost_result_10)
        qFrame_evcs_cost_result_12.setFrameShape(QtWidgets.QFrame.NoFrame)
        qFrame_evcs_cost_result_12.setFrameShadow(QtWidgets.QFrame.Plain)
        
        qHLayout_evcs_cost_result_7 = QtWidgets.QHBoxLayout(qFrame_evcs_cost_result_12)
        
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)

        self.qLabel_evcs_17 = QtWidgets.QLabel(
            '#', qFrame_evcs_cost_result_12
        )
        self.qLabel_evcs_17.setFont(font)
        self.qLabel_evcs_17.setAlignment(QtCore.Qt.AlignCenter)
        qHLayout_evcs_cost_result_7.addWidget(self.qLabel_evcs_17)
        qVLayout_evcs_cost_result_3.addWidget(qFrame_evcs_cost_result_12)

        qFrame_evcs_cost_result_13 = QtWidgets.QFrame(qFrame_evcs_cost_result_10)
        qFrame_evcs_cost_result_13.setFrameShape(QtWidgets.QFrame.NoFrame)
        qFrame_evcs_cost_result_13.setFrameShadow(QtWidgets.QFrame.Plain)
        
        qHLayout_evcs_cost_result_8 = QtWidgets.QHBoxLayout(qFrame_evcs_cost_result_13)
        
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)

        self.qLabel_evcs_18 = QtWidgets.QLabel(
            '#', qFrame_evcs_cost_result_13
        )
        self.qLabel_evcs_18.setFont(font)
        self.qLabel_evcs_18.setAlignment(QtCore.Qt.AlignCenter)

        qHLayout_evcs_cost_result_8.addWidget(self.qLabel_evcs_18)
        qVLayout_evcs_cost_result_3.addWidget(qFrame_evcs_cost_result_13)
        
        qFrame_evcs_cost_result_14 = QtWidgets.QFrame(qFrame_evcs_cost_result_10)
        qFrame_evcs_cost_result_14.setFrameShape(QtWidgets.QFrame.NoFrame)
        qFrame_evcs_cost_result_14.setFrameShadow(QtWidgets.QFrame.Plain)

        qHLayout_evcs_cost_result_9 = QtWidgets.QHBoxLayout(qFrame_evcs_cost_result_14)
        
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)

        self.qLabel_evcs_19 = QtWidgets.QLabel(
            '#', qFrame_evcs_cost_result_14
        )
        self.qLabel_evcs_19.setFont(font)
        self.qLabel_evcs_19.setAlignment(QtCore.Qt.AlignCenter)
        qHLayout_evcs_cost_result_9.addWidget(self.qLabel_evcs_19)
        qVLayout_evcs_cost_result_3.addWidget(qFrame_evcs_cost_result_14)

        qFrame_evcs_cost_result_15 = QtWidgets.QFrame(qFrame_evcs_cost_result_10)
        qFrame_evcs_cost_result_15.setFrameShape(QtWidgets.QFrame.NoFrame)
        qFrame_evcs_cost_result_15.setFrameShadow(QtWidgets.QFrame.Plain)

        qHLayout_evcs_cost_result_10 = QtWidgets.QHBoxLayout(qFrame_evcs_cost_result_15)
        
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)

        self.qLabel_evcs_20 = QtWidgets.QLabel(
            '#', qFrame_evcs_cost_result_15
        )
        self.qLabel_evcs_20.setFont(font)
        self.qLabel_evcs_20.setAlignment(QtCore.Qt.AlignCenter)
        qHLayout_evcs_cost_result_10.addWidget(self.qLabel_evcs_20)
        qVLayout_evcs_cost_result_3.addWidget(qFrame_evcs_cost_result_15)

        qFrame_evcs_cost_result_16 = QtWidgets.QFrame(qFrame_evcs_cost_result_10)
        qFrame_evcs_cost_result_16.setFrameShape(QtWidgets.QFrame.NoFrame)
        qFrame_evcs_cost_result_16.setFrameShadow(QtWidgets.QFrame.Plain)

        qHLayout_evcs_cost_result_9 = QtWidgets.QHBoxLayout(qFrame_evcs_cost_result_16)
        
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)

        self.qLabel_evcs_21 = QtWidgets.QLabel(
            '#', qFrame_evcs_cost_result_16
        )
        self.qLabel_evcs_21.setFont(font)
        self.qLabel_evcs_21.setAlignment(QtCore.Qt.AlignCenter)
        qHLayout_evcs_cost_result_9.addWidget(self.qLabel_evcs_21)
        qVLayout_evcs_cost_result_3.addWidget(qFrame_evcs_cost_result_16)
        qHLayout_evcs_cost_result.addWidget(qFrame_evcs_cost_result_10)
        
        
        
        qTabPages_evcs_result.addTab(qTab_evcs_cost_result, 'Cost')
        qGLayout_evcs_result.addWidget(qTabPages_evcs_result)
        self.stacked_main_windows.addWidget(self.widget_result_evcs)
        
        # Add Battery Design Page
        self.widget_battery_design = BatteryDesign(self) # QtWidgets.QWidget Parent Class
        self.stacked_main_windows.addWidget(self.widget_battery_design)

        # actions
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.toolBar.setFont(font)
        self.toolBar.setMovable(False)
        self.toolBar.setIconSize(QtCore.QSize(28, 28))
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBar.setFloatable(True)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionNew_Project = QtWidgets.QAction(MainWindow)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/icons/icons/new-file.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNew_Project.setIcon(icon12)
        self.actionNew_Project.setObjectName("actionNew_Project")
        self.actionOpen_Project = QtWidgets.QAction(MainWindow)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(":/icons/icons/open-folder-outline.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen_Project.setIcon(icon13)
        self.actionOpen_Project.setObjectName("actionOpen_Project")

        self.actionAnalyze_Data = QtWidgets.QAction(MainWindow)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap(":/icons/icons/analyze.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAnalyze_Data.setIcon(icon14)
        self.actionAnalyze_Data.setObjectName("actionAnalyze_Data")

        self.actionOptimize = QtWidgets.QAction(MainWindow)
        icon20 = QtGui.QIcon()
        icon20.addPixmap(QtGui.QPixmap(":/icons/icons/analyze.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOptimize.setIcon(icon20)
        self.actionOptimize.setObjectName("actionOptimize")

        self.Analyze_Battery = QtWidgets.QAction(MainWindow)
        icon21 = QtGui.QIcon()
        icon21.addPixmap(QtGui.QPixmap(":/icons/icons/washing-machine (1).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Analyze_Battery.setIcon(icon21)
        self.Analyze_Battery.setObjectName("Analyze_Battery")

        self.actionSave_Project = QtWidgets.QAction(MainWindow)
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap(":/icons/icons/save-outlined-diskette.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave_Project.setIcon(icon15)
        self.actionSave_Project.setObjectName("actionSave_Project")
        self.actionNext = QtWidgets.QAction(MainWindow)
        icon16 = QtGui.QIcon()
        icon16.addPixmap(QtGui.QPixmap(":/icons/icons/right-arrow (1).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNext.setIcon(icon16)
        self.actionNext.setObjectName("actionNext")
        self.actionPrevious = QtWidgets.QAction(MainWindow)
        icon17 = QtGui.QIcon()
        icon17.addPixmap(QtGui.QPixmap(":/icons/icons/left-arrow (1).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPrevious.setIcon(icon17)
        self.actionPrevious.setObjectName("actionPrevious")
        self.actionExit = QtWidgets.QAction(MainWindow)
        icon18 = QtGui.QIcon()
        icon18.addPixmap(QtGui.QPixmap(":/icons/icons/logout.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExit.setIcon(icon18)
        self.actionExit.setObjectName("actionExit")
        self.actionFinal_Report = QtWidgets.QAction(MainWindow)
        icon19 = QtGui.QIcon()
        icon19.addPixmap(QtGui.QPixmap(":/icons/icons/report.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFinal_Report.setIcon(icon19)
        self.actionFinal_Report.setObjectName("actionFinal_Report")
        self.toolBar.addAction(self.actionNew_Project)
        self.toolBar.addAction(self.actionOpen_Project)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionSave_Project)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionAnalyze_Data)
        self.toolBar.addAction(self.actionOptimize)
        self.toolBar.addAction(self.Analyze_Battery)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionPrevious)
        self.toolBar.addAction(self.actionNext)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionFinal_Report)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionExit)

        self.retranslateUi(MainWindow)
        self.tab_summary_report.setCurrentIndex(0)
        self.stacked_main_windows.setCurrentIndex(0)
        self.tlbx_appliances.setCurrentIndex(0)
        self.stk_solar_pv_main.setCurrentIndex(0)
        self.stk_wind_turb_main.setCurrentIndex(0)
        self.stk_electric_car_pv_main.setCurrentIndex(0)  # <- added this for electric car

        # self.stk_biomass_main.setCurrentIndex(0)
        MainWindow.showMaximized()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.dck_project_structure.setWindowTitle(_translate("MainWindow", "EnerghxPlus Structure"))
        self.tree_project_structure.headerItem().setText(0, _translate("MainWindow", "EnerghxPlus"))
        __sortingEnabled = self.tree_project_structure.isSortingEnabled()

        self.tree_project_structure.setSortingEnabled(False)
        self.tree_project_structure.topLevelItem(0).setText(0, _translate("MainWindow", "Rooms"))
        self.tree_project_structure.topLevelItem(1).setText(0, _translate("MainWindow", "Retrofit Appliances"))
        self.tree_project_structure.topLevelItem(2).setText(0, _translate("MainWindow", "Appliance Audit Result"))
        self.tree_project_structure.topLevelItem(3).setText(0, _translate("MainWindow", "Cooling Load Analysis"))
        self.tree_project_structure.topLevelItem(3).child(0).setText(0, _translate("MainWindow", "Result"))
        self.tree_project_structure.topLevelItem(4).setText(0, _translate("MainWindow", "Analysis"))
        self.tree_project_structure.topLevelItem(4).child(0).setText(0, _translate("MainWindow", "Solar PV"))
        self.tree_project_structure.topLevelItem(4).child(0).child(0).setText(0, _translate("MainWindow", "Result"))
        self.tree_project_structure.topLevelItem(4).child(1).setText(0, _translate("MainWindow", "Wind Turbine"))
        self.tree_project_structure.topLevelItem(4).child(1).child(0).setText(0, _translate("MainWindow", "Result"))
        self.tree_project_structure.topLevelItem(4).child(2).setText(0, _translate("MainWindow", "Battery Sizing"))
        self.tree_project_structure.topLevelItem(4).child(2).child(0).setText(0, _translate("MainWindow", "Result"))
        self.tree_project_structure.topLevelItem(4).child(3).setText(0, _translate("MainWindow",
                                                                                   "Electric Vehicle Charging Station"))
        self.tree_project_structure.topLevelItem(4).child(3).child(0).setText(0, _translate("MainWindow", "Result"))
        # self.tree_project_structure.topLevelItem(4).child(3).setText(0, _translate("MainWindow", "System Optimize"))
        # self.tree_project_structure.topLevelItem(4).child(3).child(0).setText(0, _translate("MainWindow", "Result"))
        self.tree_project_structure.topLevelItem(5).setText(0, _translate("MainWindow", "FINAL REPORT"))
        self.tree_project_structure.setSortingEnabled(__sortingEnabled)
        self.txtEd_summary.setHtml(_translate("MainWindow",
                                              "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                              "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                              "p, li { white-space: pre-wrap; }\n"
                                              "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                              "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                              "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt; font-weight:600;\"><br /></p>\n"
                                              "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt; font-weight:600;\"><br /></p>\n"
                                              "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:600;\">NO REPORT YET</span></p></body></html>"))
        self.tab_summary_report.setTabText(self.tab_summary_report.indexOf(self.tb_summary),
                                           _translate("MainWindow", "Summary Report"))
        self.lbl_analysis_type.setText(_translate("MainWindow", "APPLIANCE AUDIT"))

        self.gbox_rooms_office.setTitle(_translate("MainWindow", "OFFICES"))
        self.btn_add_office.setText(_translate("MainWindow", "Add Office"))

        self.gbox_rooms_laboratories.setTitle(_translate("MainWindow", "LABORATORIES"))
        self.btn_add_laboratory.setText(_translate("MainWindow", "Add Laboratory"))
        self.gbox_rooms_lecture_room.setTitle(_translate("MainWindow", "LECTURE ROOMS"))
        self.btn_add_lecture_room.setText(_translate("MainWindow", "Add Lecture Room"))
        self.gbox_rooms_conference_room.setTitle(_translate("MainWindow", "CONFERENCE ROOMS"))
        self.btn_add_conference_rooms.setText(_translate("MainWindow", "Add Conference Room"))
        self.gbox_rooms_others.setTitle(_translate("MainWindow", "OTHERS"))
        self.btn_add_others.setText(_translate("MainWindow", "Add Other"))
        self.lbl_appliance_lbl.setText(_translate("MainWindow", "Appliance Rating"))
        self.lbl_appliance_rating.setText(_translate("MainWindow", "8.9"))
        self.lbl_kw_appliance.setText(_translate("MainWindow", "kW"))
        self.lbl_retrofit_lbl.setText(_translate("MainWindow", "Retrofit Rating"))
        self.lbl_retrofit_rating.setText(_translate("MainWindow", "8.9"))
        self.lbl_kw_retrofit.setText(_translate("MainWindow", "kW"))
        self.gb_retrofit_appliances.setTitle(_translate("MainWindow", "Retrofit Appliances"))
        self.rd_5star_retrofit.setText(_translate("MainWindow", "SIEMEN FAN"))
        self.rd_4star_retrofit.setText(_translate("MainWindow", "GLOATR"))
        self.rd_3star_retrofit.setText(_translate("MainWindow", "REGS"))
        self.rd_2star_retrofit.setText(_translate("MainWindow", "FSDS"))
        self.rd_1star_retrofi.setText(_translate("MainWindow", "SDSD"))
        self.rd_1star_retrofi.setShortcut(_translate("MainWindow", "Esc"))
        self.tlbx_appliances.setItemText(self.tlbx_appliances.indexOf(self.tlbx_app_sample),
                                         _translate("MainWindow", "Page 1"))
        self.groupBox_21.setTitle(_translate("MainWindow", "REPORT"))
        self.tbl_summary_aa_audit.setSortingEnabled(True)
        item = self.tbl_summary_aa_audit.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Appliance"))
        item = self.tbl_summary_aa_audit.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Bill Savings"))
        item = self.tbl_summary_aa_audit.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Energy Usage"))
        item = self.tbl_summary_aa_audit.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Energy Savings"))
        item = self.tbl_summary_aa_audit.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "PayBack Period"))
        item = self.tbl_summary_aa_audit.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Rate of Return"))
        item = self.tbl_summary_cl.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Room"))
        item = self.tbl_summary_cl.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Cooling Load (Btu/hr)"))
        item = self.tbl_summary_cl.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Cooling Load (tons)"))
        item = self.tbl_summary_cl.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Energy Efficiecny Ratio"))
        item = self.tbl_summary_cl.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Coefficient of Performace"))
        item = self.tbl_summary_cl.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "AC Rating"))

        self.label_70.setText(_translate("MainWindow", "SOLAR PV"))

        # labels for evcs result
        self.groupBox_result_evcs.setTitle(_translate("MainWindow", "Output For Power Info"))
        self.label_result_evcs_power_generated.setText(_translate("MainWindow", "#"))
        self.label_result_evcs_watts_1.setText(_translate("MainWindow", ""))
        self.label_result_evcs_power_consumed.setText(_translate("MainWindow", "# "))
        self.label_result_evcs_watts_2.setText(_translate("MainWindow", ""))
        self.label_result_evcs_power_supplied_1.setText(_translate("MainWindow", "#"))
        self.label_result_evcs_watts_3.setText(_translate("MainWindow", ""))
        self.label_supplied_text_1.setText(_translate("MainWindow", "supplied to"))
        self.label_result_evcs_power_supplied_2.setText(_translate("MainWindow", "#"))
        self.label_result_evcs_watts_4.setText(_translate("MainWindow", ""))
        self.label_supplied_text_2.setText(_translate("MainWindow", "supplied to"))
        self.label_help.setText(_translate("MainWindow", "Arrow denotes flow of power"))

        # makes electric car logo not show
        # self.label_electric_car.setText(_translate("MainWindow", "rerer"))
        self.gb_solar_stdt.setTitle(_translate("MainWindow", "SITE DATA"))
        self.label.setText(_translate("MainWindow", "Site Name"))
        self.label_2.setText(_translate("MainWindow", "Type"))
        self.label_3.setText(_translate("MainWindow", "Site"))
        self.label_4.setText(_translate("MainWindow", "Latitude"))
        self.label_5.setText(_translate("MainWindow", "Longtitude"))
        self.label_6.setText(_translate("MainWindow", "Elevation"))
        self.label_7.setText(_translate("MainWindow", "No of Wings"))
        self.label_15.setText(_translate("MainWindow", "Area"))
        self.label_16.setText(_translate("MainWindow", "Pitch"))
        self.cbox_solar_stdt_save.setText(_translate("MainWindow", "Save Site Data"))
        self.gb_solar_indt.setTitle(_translate("MainWindow", "INVERTER DATA"))
        self.label_17.setText(_translate("MainWindow", "Inverter Name"))
        self.label_18.setText(_translate("MainWindow", "Type"))
        self.label_19.setText(_translate("MainWindow", "Max Input Voltage"))
        self.label_23.setText(_translate("MainWindow", "MPPT Units"))
        self.label_24.setText(_translate("MainWindow", "Efficiency"))
        self.label_25.setText(_translate("MainWindow", "MPPT Voltage Upper"))
        self.label_26.setText(_translate("MainWindow", "MPPT Voltage Lower"))
        self.cbox_solar_indt_save.setText(_translate("MainWindow", "Save Inverter Data"))

        self.label_20.setText(_translate("MainWindow", "Module Name"))
        self.label_21.setText(_translate("MainWindow", "Type"))
        self.label_22.setText(_translate("MainWindow", "Rated Power"))
        # self.label_29.setText(_translate("MainWindow", "Open Circuit Voltage"))
        self.label_31.setText(_translate("MainWindow", "Fuse Rating"))
        self.label_27.setText(_translate("MainWindow", "Max Power Voltage"))
        self.label_28.setText(_translate("MainWindow", "Max Power Curent"))
        self.label_30.setText(_translate("MainWindow", "Short Circuit Voltage"))
        self.label_32.setText(_translate("MainWindow", "Max System Voltage"))
        self.gbox_solar_mddt_op_temp.setTitle(_translate("MainWindow", "Operating Temperature"))
        self.label_12.setText(_translate("MainWindow", "Upper"))
        self.label_13.setText(_translate("MainWindow", "Lower"))
        self.gbox_solar_mddt_pow_tol.setTitle(_translate("MainWindow", "Power Tolerance"))
        self.label_8.setText(_translate("MainWindow", "Upper"))
        self.label_9.setText(_translate("MainWindow", "Lower"))
        self.gbox_solar_mddt_temp_coeff.setTitle(_translate("MainWindow", "Temperature Coefficients"))
        self.label_41.setText(_translate("MainWindow", "Power"))
        self.label_42.setText(_translate("MainWindow", "Voltage"))
        self.label_43.setText(_translate("MainWindow", "Current"))
        self.gbox_solar_mddt_dim.setTitle(_translate("MainWindow", "Dimensions"))
        self.label_36.setText(_translate("MainWindow", "Length"))
        self.label_37.setText(_translate("MainWindow", "Breadth"))
        self.label_38.setText(_translate("MainWindow", "Height"))
        self.label_39.setText(_translate("MainWindow", "Weight"))
        self.label_40.setText(_translate("MainWindow", "Efficiency"))
        self.cbox_solar_mddt_save.setText(_translate("MainWindow", "Save Module Data"))
        self.gbox_solar_constants.setTitle(_translate("MainWindow", "CONSTANTS"))
        self.label_54.setText(_translate("MainWindow", "Effective Cell Temperature"))
        self.label_47.setText(_translate("MainWindow", "Ambiance Temperature"))
        self.label_51.setText(_translate("MainWindow", "Assumed DC Loss"))
        self.label_48.setText(_translate("MainWindow", "Tolerance"))
        self.label_52.setText(_translate("MainWindow", "Temperature Effect"))
        self.label_53.setText(_translate("MainWindow", "Safety Margin"))
        self.label_50.setText(_translate("MainWindow", "Assumed AC Loss"))
        self.label_49.setText(_translate("MainWindow", "Dirt Loss"))
        item = self.tbl_solar_insolation.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "Jan"))
        item = self.tbl_solar_insolation.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "Feb"))
        item = self.tbl_solar_insolation.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "Mar"))
        item = self.tbl_solar_insolation.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "Apr"))
        item = self.tbl_solar_insolation.verticalHeaderItem(4)
        item.setText(_translate("MainWindow", "May"))
        item = self.tbl_solar_insolation.verticalHeaderItem(5)
        item.setText(_translate("MainWindow", "Jun"))
        item = self.tbl_solar_insolation.verticalHeaderItem(6)
        item.setText(_translate("MainWindow", "Jul"))
        item = self.tbl_solar_insolation.verticalHeaderItem(7)
        item.setText(_translate("MainWindow", "Aug"))
        item = self.tbl_solar_insolation.verticalHeaderItem(8)
        item.setText(_translate("MainWindow", "Sept"))
        item = self.tbl_solar_insolation.verticalHeaderItem(9)
        item.setText(_translate("MainWindow", "Oct"))
        item = self.tbl_solar_insolation.verticalHeaderItem(10)
        item.setText(_translate("MainWindow", "Nov"))
        item = self.tbl_solar_insolation.verticalHeaderItem(11)
        item.setText(_translate("MainWindow", "Dec"))
        item = self.tbl_solar_insolation.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "0 deg"))
        item = self.tbl_solar_insolation.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "6 deg"))
        item = self.tbl_solar_insolation.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "21 deg"))
        __sortingEnabled = self.tbl_solar_insolation.isSortingEnabled()
        self.tbl_solar_insolation.setSortingEnabled(False)
        item = self.tbl_solar_insolation.item(0, 0)
        item.setText(_translate("MainWindow", "5.23"))
        item = self.tbl_solar_insolation.item(0, 1)
        item.setText(_translate("MainWindow", "5.45"))
        item = self.tbl_solar_insolation.item(0, 2)
        item.setText(_translate("MainWindow", "5.80"))
        item = self.tbl_solar_insolation.item(1, 0)
        item.setText(_translate("MainWindow", "5.43"))
        item = self.tbl_solar_insolation.item(1, 1)
        item.setText(_translate("MainWindow", "5.57"))
        item = self.tbl_solar_insolation.item(1, 2)
        item.setText(_translate("MainWindow", "5.72"))
        item = self.tbl_solar_insolation.item(2, 0)
        item.setText(_translate("MainWindow", "5.39"))
        item = self.tbl_solar_insolation.item(2, 1)
        item.setText(_translate("MainWindow", "5.43"))
        item = self.tbl_solar_insolation.item(2, 2)
        item.setText(_translate("MainWindow", "5.34"))
        item = self.tbl_solar_insolation.item(3, 0)
        item.setText(_translate("MainWindow", "5.13"))
        item = self.tbl_solar_insolation.item(3, 1)
        item.setText(_translate("MainWindow", "5.14"))
        item = self.tbl_solar_insolation.item(3, 2)
        item.setText(_translate("MainWindow", "4.00"))
        item = self.tbl_solar_insolation.item(4, 0)
        item.setText(_translate("MainWindow", "4.68"))
        item = self.tbl_solar_insolation.item(4, 1)
        item.setText(_translate("MainWindow", "4.73"))
        item = self.tbl_solar_insolation.item(4, 2)
        item.setText(_translate("MainWindow", "4.71"))
        item = self.tbl_solar_insolation.item(5, 0)
        item.setText(_translate("MainWindow", "3.97"))
        item = self.tbl_solar_insolation.item(5, 1)
        item.setText(_translate("MainWindow", "4.02"))
        item = self.tbl_solar_insolation.item(5, 2)
        item.setText(_translate("MainWindow", "4.02"))
        item = self.tbl_solar_insolation.item(6, 0)
        item.setText(_translate("MainWindow", "3.88"))
        item = self.tbl_solar_insolation.item(6, 1)
        item.setText(_translate("MainWindow", "3.92"))
        item = self.tbl_solar_insolation.item(6, 2)
        item.setText(_translate("MainWindow", "3.91"))
        item = self.tbl_solar_insolation.item(7, 0)
        item.setText(_translate("MainWindow", "3.92"))
        item = self.tbl_solar_insolation.item(7, 1)
        item.setText(_translate("MainWindow", "3.93"))
        item = self.tbl_solar_insolation.item(7, 2)
        item.setText(_translate("MainWindow", "3.85"))
        item = self.tbl_solar_insolation.item(8, 0)
        item.setText(_translate("MainWindow", "4.03"))
        item = self.tbl_solar_insolation.item(8, 1)
        item.setText(_translate("MainWindow", "4.03"))
        item = self.tbl_solar_insolation.item(8, 2)
        item.setText(_translate("MainWindow", "3.91"))
        item = self.tbl_solar_insolation.item(9, 0)
        item.setText(_translate("MainWindow", "4.50"))
        item = self.tbl_solar_insolation.item(9, 1)
        item.setText(_translate("MainWindow", "4.57"))
        item = self.tbl_solar_insolation.item(9, 2)
        item.setText(_translate("MainWindow", "4.59"))
        item = self.tbl_solar_insolation.item(10, 0)
        item.setText(_translate("MainWindow", "4.90"))
        item = self.tbl_solar_insolation.item(10, 1)
        item.setText(_translate("MainWindow", "5.07"))
        item = self.tbl_solar_insolation.item(10, 2)
        item.setText(_translate("MainWindow", "5.32"))
        item = self.tbl_solar_insolation.item(11, 0)
        item.setText(_translate("MainWindow", "5.12"))
        item = self.tbl_solar_insolation.item(11, 1)
        item.setText(_translate("MainWindow", "5.36"))
        item = self.tbl_solar_insolation.item(11, 2)
        item.setText(_translate("MainWindow", "5.77"))
        self.tbl_solar_insolation.setSortingEnabled(__sortingEnabled)
        self.gb_solar_months.setTitle(_translate("MainWindow", "Select Months"))
        self.cbox_solar_months_selectall.setText(_translate("MainWindow", "Select All"))
        self.cbox_solar_months_jan.setText(_translate("MainWindow", "January"))
        self.cbox_solar_months_feb.setText(_translate("MainWindow", "February"))
        self.cbox_solar_months_mar.setText(_translate("MainWindow", "March"))
        self.cbox_solar_months_apr.setText(_translate("MainWindow", "April"))
        self.cbox_solar_months_may.setText(_translate("MainWindow", "May"))
        self.cbox_solar_months_jun.setText(_translate("MainWindow", "June"))
        self.cbox_solar_months_jul.setText(_translate("MainWindow", "July"))
        self.cbox_solar_months_aug.setText(_translate("MainWindow", "August"))
        self.cbox_solar_months_sept.setText(_translate("MainWindow", "September"))
        self.cbox_solar_months_oct.setText(_translate("MainWindow", "October"))
        self.cbox_solar_months_nov.setText(_translate("MainWindow", "November"))
        self.cbox_solar_months_dec.setText(_translate("MainWindow", "December"))
        item = self.tbl_solar_output_result.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "Actual Power"))
        item = self.tbl_solar_output_result.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "Annual Energy"))
        item = self.tbl_solar_output_result.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "Specific Energy"))
        item = self.tbl_solar_output_result.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "Installed Capacity"))
        item = self.tbl_solar_output_result.verticalHeaderItem(4)
        item.setText(_translate("MainWindow", "Total No of PV Modules"))
        item = self.tbl_solar_output_result.verticalHeaderItem(5)
        item.setText(_translate("MainWindow", "No of PV Modules per wing"))
        item = self.tbl_solar_output_result.verticalHeaderItem(6)
        item.setText(_translate("MainWindow", "Max No of Modules"))
        item = self.tbl_solar_output_result.verticalHeaderItem(7)
        item.setText(_translate("MainWindow", "Min No of Modules"))
        item = self.tbl_solar_output_result.verticalHeaderItem(8)
        item.setText(_translate("MainWindow", "Min Daily PV Energy Output"))
        item = self.tbl_solar_output_result.verticalHeaderItem(9)
        item.setText(_translate("MainWindow", "Min Voltage"))
        item = self.tbl_solar_output_result.verticalHeaderItem(10)
        item.setText(_translate("MainWindow", "Voltage Inverter"))
        item = self.tbl_solar_output_result.verticalHeaderItem(11)
        item.setText(_translate("MainWindow", "F_dirt"))
        item = self.tbl_solar_output_result.verticalHeaderItem(12)
        item.setText(_translate("MainWindow", "F_man"))
        item = self.tbl_solar_output_result.verticalHeaderItem(13)
        item.setText(_translate("MainWindow", "F_temp"))
        item = self.tbl_solar_output_result.verticalHeaderItem(14)
        item.setText(_translate("MainWindow", "Area"))
        item = self.tbl_solar_output_result.verticalHeaderItem(15)
        item.setText(_translate("MainWindow", "V_oc"))
        item = self.tbl_solar_output_result.verticalHeaderItem(16)
        item.setText(_translate("MainWindow", "System Efficiency"))
        item = self.tbl_solar_output_result.verticalHeaderItem(17)
        item.setText(_translate("MainWindow", "Eff AC Cables"))
        item = self.tbl_solar_output_result.verticalHeaderItem(18)
        item.setText(_translate("MainWindow", "Eff DC Cables"))
        item = self.tbl_solar_output_result.verticalHeaderItem(19)
        item.setText(_translate("MainWindow", "Eff Inverter"))
        item = self.tbl_solar_output_result.verticalHeaderItem(20)
        item.setText(_translate("MainWindow", "Performance Ratio"))
        item = self.tbl_solar_output_result.verticalHeaderItem(21)
        item.setText(_translate("MainWindow", "Average PSH"))
        item = self.tbl_solar_output_result.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Result"))
        item = self.tbl_solar_output_psh.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "January"))
        item = self.tbl_solar_output_psh.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "February"))
        item = self.tbl_solar_output_psh.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "March"))
        item = self.tbl_solar_output_psh.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "April"))
        item = self.tbl_solar_output_psh.verticalHeaderItem(4)
        item.setText(_translate("MainWindow", "May"))
        item = self.tbl_solar_output_psh.verticalHeaderItem(5)
        item.setText(_translate("MainWindow", "June"))
        item = self.tbl_solar_output_psh.verticalHeaderItem(6)
        item.setText(_translate("MainWindow", "July"))
        item = self.tbl_solar_output_psh.verticalHeaderItem(7)
        item.setText(_translate("MainWindow", "August"))
        item = self.tbl_solar_output_psh.verticalHeaderItem(8)
        item.setText(_translate("MainWindow", "September"))
        item = self.tbl_solar_output_psh.verticalHeaderItem(9)
        item.setText(_translate("MainWindow", "October"))
        item = self.tbl_solar_output_psh.verticalHeaderItem(10)
        item.setText(_translate("MainWindow", "November"))
        item = self.tbl_solar_output_psh.verticalHeaderItem(11)
        item.setText(_translate("MainWindow", "December"))
        item = self.tbl_solar_output_psh.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "PSH"))
        self.gb_solar_output.setTitle(_translate("MainWindow", "Bar Chat Visualization"))
        self.tb_solar_output_expand_fig.setText(_translate("MainWindow", "Expand Figure"))
        self.label_72.setText(_translate("MainWindow", "WIND TURBINE"))
        self.gb_wind_turb_stdt.setTitle(_translate("MainWindow", "SITE DATA"))
        self.label_10.setText(_translate("MainWindow", "Name"))
        self.label_33.setText(_translate("MainWindow", "Longitiude"))
        self.label_11.setText(_translate("MainWindow", "Latitude"))
        self.gb_wind_turb_ardt.setTitle(_translate("MainWindow", "Air Data"))
        self.label_45.setText(_translate("MainWindow", "Air Density"))
        self.label_44.setText(_translate("MainWindow", "Temperature"))
        self.label_34.setText(_translate("MainWindow", "Altitude"))
        self.label_35.setText(_translate("MainWindow", "Pressure"))
        self.gb_wind_turb_wddt.setTitle(_translate("MainWindow", "Wind Distribution Data"))
        self.label_46.setText(_translate("MainWindow", "Scale Parameter"))
        self.label_57.setText(_translate("MainWindow", "Velocity"))
        self.label_55.setText(_translate("MainWindow", "Height"))
        self.label_56.setText(_translate("MainWindow", "Shape Parameter"))
        self.cbox_wind_turb_stdt_save.setText(_translate("MainWindow", "Save Site Data"))
        self.gb_wind_turb_tbin.setTitle(_translate("MainWindow", "TURBINE INFO"))
        self.label_60.setText(_translate("MainWindow", "Rated Power"))
        self.label_58.setText(_translate("MainWindow", "Cut-In Wind Speed"))
        self.label_61.setText(_translate("MainWindow", "Cut-Out Wind Speed"))
        self.label_59.setText(_translate("MainWindow", "Rotor Diameter"))
        self.label_64.setText(_translate("MainWindow", "Hub Height"))
        self.label_63.setText(_translate("MainWindow", "Units"))

        self.label_62.setText(_translate("MainWindow", "Blade Length"))
        self.label_65.setText(_translate("MainWindow", "Number of Blades"))
        self.label_66.setText(_translate("MainWindow", "Turbine Name"))
        self.cbox_wind_turb_tbin_save.setText(_translate("MainWindow", "Save Turbine Info"))
        self.label_213.setText(_translate("MainWindow", "POWER"))
        self.lbl_wind_turb_output_pow.setText(_translate("MainWindow", "-"))
        self.label_214.setText(_translate("MainWindow", "Watt"))
        self.label_210.setText(_translate("MainWindow", "EFFICIENCY"))
        self.lbl_wind_turb_output_eff.setText(_translate("MainWindow", "-"))
        self.label_211.setText(_translate("MainWindow", "%"))
        self.gb_final_solar_pv.setTitle(_translate("MainWindow", "SOLAR PV"))
        self.lbl_solar_pv_pow.setText(_translate("MainWindow", "4500 KW"))
        self.gb_final_wind_turb.setTitle(_translate("MainWindow", "WIND TURBINE"))
        self.lbl_wind_turb_pow.setText(_translate("MainWindow", "8.25 Hp"))
        self.btn_referesh_final_result.setText(_translate("MainWindow", "Referesh Result"))
        self.lbl_final_pow_consumed.setText(_translate("MainWindow", "4500 KW"))
        self.lbl_power_available_lbl.setText(_translate("MainWindow", "Power Available"))
        self.lbl_power_consumed_lbl.setText(_translate("MainWindow", "Power Consumed"))
        self.lbl_final_pow_available.setText(_translate("MainWindow", "4500 KW"))
        self.label_90.setText(_translate("MainWindow", "Solar PV"))

        self.lbl_final_solar_pv_comp_per.setText(_translate("MainWindow", "89%"))
        self.lbl_final_solar_pv_comp_kw.setText(_translate("MainWindow", "(7564 KW)"))
        self.label_95.setText(_translate("MainWindow", "Wind Turbine"))
        self.lbl_final_wind_turb_comp_per.setText(_translate("MainWindow", "89%"))
        self.lbl_final_wind_turb_comp_kw.setText(_translate("MainWindow", "(7564 KW)"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionNew_Project.setText(_translate("MainWindow", "New Project"))
        self.actionOpen_Project.setText(_translate("MainWindow", "Open Project"))
        self.actionAnalyze_Data.setText(_translate("MainWindow", "Analyze Data"))
        self.actionOptimize.setText(_translate("MainWindow", "Optimize Data"))
        self.Analyze_Battery.setText(_translate("MainWindow", "Design Battery"))
        self.actionSave_Project.setText(_translate("MainWindow", "Save Project"))
        self.actionNext.setText(_translate("MainWindow", "Next"))
        self.actionPrevious.setText(_translate("MainWindow", "Previous"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionFinal_Report.setText(_translate("MainWindow", "Final Report"))
        MainWindow.setWindowTitle('Energhx Plus 3.0')
        MainWindow.setWindowIcon(QtGui.QIcon("icons/renewable-energy.png"))
        self.lbl_analysis_type.setVisible(True)
        self.tree_project_structure.expandAll()
        self.actionFinal_Report.setVisible(False)
        self.actionPrevious.setEnabled(False)
        self.actionAnalyze_Data.setEnabled(True)
        self.actionOptimize.setEnabled(True)
        self.Analyze_Battery.setEnabled(True)

        with open('JSON files/sp_site_data.json') as f:
            self.site_data = json.load(f)
        self.cmbx_solar_stdt_name.addItems([''] + list(self.site_data.keys()))

        with open('JSON files/sp_inverter_spec.json') as f:
            self.inverter_spec = json.load(f)
        self.cmbx_solar_indt_name.addItems([''] + list(self.inverter_spec.keys()))


        with open('JSON files/sp_module_spec.json') as f:
            self.module_spec = json.load(f)
        self.cmbx_solar_mddt_name.addItems([''] + list(self.module_spec.keys()))

        with open('JSON files/wt_site_data.json') as f:
            self.wt_site_data = json.load(f)
        self.cmbx_wind_turb_site_name.addItems([''] + list(self.wt_site_data.keys()))

        with open('JSON files/evcs_site_data.json') as f:
            self.evcs_site_data = json.load(f)
            print(self.evcs_site_data)
        self.qComboBox_e_h_location.addItems([''] + list(self.evcs_site_data.keys()))

        with open('JSON files/wt_turbine_data.json') as f:
            self.wt_t_data = json.load(f)
        self.cmbx_wind_turb_tbin_name.addItems([''] + list(self.wt_t_data.keys()))

        with open('JSON files/retrofit_appliances.json') as f:
            self.retrofit_appliances = json.load(f)

        if self.rooms != {}:
            self.load_saved()

        self.btn_add_conference_rooms.clicked.connect(lambda: self.add_new_room(self.btn_add_conference_rooms))
        self.btn_add_office.clicked.connect(lambda: self.add_new_room(self.btn_add_office))
        self.btn_add_lecture_room.clicked.connect(lambda: self.add_new_room(self.btn_add_lecture_room))
        self.btn_add_laboratory.clicked.connect(lambda: self.add_new_room(self.btn_add_laboratory))
        self.btn_add_others.clicked.connect(lambda: self.add_new_room(self.btn_add_others))
        self.tree_project_structure.selectionModel().selectionChanged.connect(self.tree_view_item_changed)

        self.actionNext.triggered.connect(self.next_page)
        self.actionPrevious.triggered.connect(self.prev_page)
        self.actionAnalyze_Data.triggered.connect(self.analyze)
        self.actionOptimize.triggered.connect(self.optimize)
        self.Analyze_Battery.triggered.connect(self.analyse_battery)

        self.solar_output_figure = plt.figure()
        self.solar_output_figure_ax = self.solar_output_figure.add_subplot(111)
        layout = QtWidgets.QVBoxLayout(self.tb_solar_output_barchart)
        layout.addWidget(FigureCanvas(self.solar_output_figure))
        self.tb_solar_output_barchart.setLayout(layout)

        self.wid_summary_aa_figure = plt.figure()
        self.wid_summary_aa_figure_ax = self.wid_summary_aa_figure.add_subplot(111)
        layout = QtWidgets.QVBoxLayout(self.wid_summary_aa_graph)
        layout.addWidget(FigureCanvas(self.wid_summary_aa_figure))
        self.wid_summary_aa_graph.setLayout(layout)

        self.wid_summary_cl_figure = plt.figure()
        self.wid_summary_cl_figure_ax = self.wid_summary_cl_figure.add_subplot(111)
        layout = QtWidgets.QVBoxLayout(self.wid_summary_cl_graph)
        layout.addWidget(FigureCanvas(self.wid_summary_cl_figure))
        self.wid_summary_cl_graph.setLayout(layout)

        self.cmbx_solar_stdt_name.currentTextChanged.connect(self.solar_pv_site_name_changed)
        self.cmbx_solar_indt_name.currentTextChanged.connect(self.solar_pv_inverter_name_changed)
        self.cmbx_solar_mddt_name.currentTextChanged.connect(self.solar_pv_module_name_changed)
        self.cmbx_wind_turb_site_name.currentTextChanged.connect(self.wind_turbine_site_name_changed)
        # self.qComboBox_e_h_location.currentTextChanged.connect(self.evcs_site_name_changed)
        self.cmbx_wind_turb_tbin_name.currentTextChanged.connect(self.wind_turbine_turbine_name_changed)

        self.hslider_solar_const_assumed_ac_loss.valueChanged.connect(
            lambda: self.slider_value_changed(self.hslider_solar_const_assumed_ac_loss))
        self.txt_solar_const_assumed_ac_loss.textChanged.connect(
            lambda: self.slider_text_value_change(self.txt_solar_const_assumed_ac_loss))

        self.hslider_solar_const_assumed_dc_loss.valueChanged.connect(
            lambda: self.slider_value_changed(self.hslider_solar_const_assumed_dc_loss))
        self.txt_solar_const_assumed_dc_loss.textChanged.connect(
            lambda: self.slider_text_value_change(self.txt_solar_const_assumed_dc_loss))

        self.hslider_solar_const_dirt_loss.valueChanged.connect(
            lambda: self.slider_value_changed(self.hslider_solar_const_dirt_loss))
        self.txt_solar_const_dirt_loss.textChanged.connect(
            lambda: self.slider_text_value_change(self.txt_solar_const_dirt_loss))

        self.hslider_solar_const_safety_margin.valueChanged.connect(
            lambda: self.slider_value_changed(self.hslider_solar_const_safety_margin))
        self.txt_solar_const_safety_margin.textChanged.connect(
            lambda: self.slider_text_value_change(self.txt_solar_const_safety_margin))

        self.hslider_solar_const_temp_effect.valueChanged.connect(
            lambda: self.slider_value_changed(self.hslider_solar_const_temp_effect))
        self.txt_solar_const_temp_effect.textChanged.connect(
            lambda: self.slider_text_value_change(self.txt_solar_const_temp_effect))

        self.hslider_solar_const_tol.valueChanged.connect(
            lambda: self.slider_value_changed(self.hslider_solar_const_tol))
        self.txt_solar_const_tol.textChanged.connect(lambda: self.slider_text_value_change(self.txt_solar_const_tol))

        for c_box in self.gb_solar_months.children():
            if isinstance(c_box, QtWidgets.QCheckBox):
                if c_box.text() == 'Select All':
                    continue
                c_box.clicked.connect(self.select_month)
        self.cbox_solar_months_selectall.clicked.connect(self.select_all_month)

        self.gb_final_solar_pv.clicked.connect(self.final_report_open)
        self.gb_final_wind_turb.clicked.connect(self.final_report_open)

        self.actionFinal_Report.triggered.connect(self.final_report_open)

        self.final_audit_figure = plt.figure()
        self.final_audit_figure_ax = self.final_audit_figure.add_subplot(111)
        layout = QtWidgets.QVBoxLayout(self.wid_final_audit_graph)
        layout.addWidget(FigureCanvas(self.final_audit_figure))

        self.composition_figure = plt.figure(figsize=(10, 3))
        self.composition_figure_ax = self.composition_figure.add_subplot(111)
        layout = QtWidgets.QVBoxLayout(self.wid_final_comp_graph)
        layout.addWidget(FigureCanvas(self.composition_figure))
        self.wid_final_comp_graph.setLayout(layout)

        # self.actionSave_Project.triggered.connect(self.save)

        # self.actionExit.triggered.connect(self.exit)
        # self.actionOpen_Project.triggered.connect(self.open)
        # self.actionNew_Project.triggered.connect(self.new_project)

    def load_saved(self):
        appliances = {}
        for room in self.rooms:
            self.load_new_buttons(room, self.rooms[room]['room_type'], eval('self.' + self.rooms[room]['button']))
            appliances.update(self.rooms[room]['appliances'])
        self.load_saved_toolBox(appliances, self.saved_data['retrofit'])

        if 'solar_pv' in self.saved_data:
            try:
                self.cmbx_solar_stdt_name.setCurrentText(self.saved_data['solar_pv']['site_data']['name'])
                self.populate_solar_pv_site_data(self.saved_data['solar_pv']['site_data']['data'])
            except KeyError:
                pass
            try:
                self.cmbx_solar_indt_name.setCurrentText(self.saved_data['solar_pv']['inverter_data']['name'])
                self.populate_solar_pv_inverter_data(self.saved_data['solar_pv']['inverter_data']['data'])
            except KeyError:
                pass
            try:
                self.cmbx_solar_mddt_name.setCurrentText(self.saved_data['solar_pv']['module_data']['name'])
                self.populate_solar_pv_module_data(self.saved_data['solar_pv']['module_data']['data'])
            except KeyError:
                pass
            try:
                self.populate_solar_pv_constants(self.saved_data['solar_pv']['constants']['data'])
            except KeyError:
                pass

        if 'wind_turbine' in self.saved_data:
            try:
                self.cmbx_wind_turb_site_name.setCurrentText(self.saved_data['wind_turbine']['site_data']['name'])
                self.populate_wind_turbine_site_data(self.saved_data['wind_turbine']['site_data']['data'])
            except KeyError:
                pass
            try:
                self.cmbx_wind_turb_tbin_name.setCurrentText(self.saved_data['wind_turbine']['turbine']['name'])
                self.populate_wind_turbine_turbine_data(self.saved_data['wind_turbine']['turbine']['data'])
            except KeyError:
                pass

        for c_box in self.gb_solar_months.children():
            if isinstance(c_box, QtWidgets.QCheckBox):
                c_box.setChecked(True)

    def populate_solar_pv_constants(self, data):
        try:
            self.dspbox_solar_const_amb_temp.setValue(data['amb_temp'])

            self.hslider_solar_const_tol.setValue(data['tolerance'] * 100)
            self.txt_solar_const_tol.setText(str(data['tolerance']))

            self.hslider_solar_const_dirt_loss.setValue(data['dirt_loss'] * 100)
            self.txt_solar_const_dirt_loss.setText(str(data['dirt_loss']))

            self.hslider_solar_const_assumed_dc_loss.setValue(data['assumed_dc_loss'] * 100)
            self.txt_solar_const_assumed_dc_loss.setText(str(data['assumed_dc_loss']))

            self.hslider_solar_const_assumed_ac_loss.setValue(data['assumed_ac_loss'] * 100)
            self.txt_solar_const_assumed_ac_loss.setText(str(data['assumed_ac_loss']))

            self.hslider_solar_const_temp_effect.setValue(data['temp_effect'] * 100)
            self.txt_solar_const_temp_effect.setText(str(data['temp_effect']))

            self.hslider_solar_const_safety_margin.setValue(data['safety_marg'] * 100)
            self.txt_solar_const_safety_margin.setText(str(data['tolerance']))

            self.dspbox_solar_const_eff_cel_temp.setValue(data['eff_cell_temp'])
        except Exception as e:
            print('Error Loading Solar PV Constants -->> ', type(e), str(e))

    def add_new_room(self, button):
        try:
            room_type = button.parent().title()
            room_name, ok_pressed = QtWidgets.QInputDialog.getText(self.centralwidget, 'Room Detail',
                                                                   "Enter a Name for the " + room_type)

            if ok_pressed:
                i = 1
                room_name_temp = room_name
                while room_name_temp in self.rooms:
                    room_name_temp = room_name + ' (' + str(i) + ')'
                    i += 1
                room_name = room_name_temp

                parent_gb = button.parent()
                tb = QtWidgets.QToolButton(parent_gb)
                icon2 = QtGui.QIcon()
                icon2.addPixmap(QtGui.QPixmap(":/icons/icons/" + room_type.lower() + ".png"), QtGui.QIcon.Normal,
                                QtGui.QIcon.Off)
                tb.setIcon(icon2)
                tb.setIconSize(QtCore.QSize(35, 35))
                tb.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
                tb.setAutoRaise(True)
                tb.setObjectName(room_name)
                tb.setText(room_name)
                tb.setCursor(QtCore.Qt.PointingHandCursor)
                tb.clicked.connect(lambda: self.room_popup(room_name, room_type))
                tb.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
                parent_gb.layout().insertWidget(parent_gb.layout().count() - 1, tb)
                parent_gb.layout().itemAt(parent_gb.layout().count() - 1).setAlignment(
                    QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                self.rooms[room_name] = {'room_type': room_type, 'button': button.objectName(), 'appliances': {},
                                         'cooling_load': {'result': {}, 'saved_data': {}}}
        except Exception as e:
            print('Error Adding New Room -->> ', type(e), str(e))

    def analyse_battery(self):
        '''
        try:
            self.focus_on_main_window = False

            # battery_design = BatteryDesign(self)

            self.battery_design = BatteryDesign(self)
            self.battery_design.showMaximized()


        except Exception as e:
            print('Error Battery Analyse Action -->> ', type(e), str(e))
        '''
        self.navigate_pages("Battery Design")

    def room_popup(self, room_name, room_type):
        try:
            self.pop_up_window = QtWidgets.QMainWindow(self.centralwidget)

            if Ui_MainWindow.current_index == 0:
                self.pop_up = appliance_popup.Ui_MainWindow()
                self.pop_up.setupUi(self.pop_up_window, room_name, room_type, self.rooms[room_name]['appliances'])
                self.pop_up.appliances_added.connect(self.appliances_added)
            elif Ui_MainWindow.current_index == 3:
                self.pop_up = cl_popup.Ui_MainWindow()
                self.pop_up.setupUi(
                    self.pop_up_window, room_name, room_type,
                    self.rooms[room_name]['appliances'],
                    self.rooms[room_name]['cooling_load']['saved_data'],
                    self.data_pages['Cooling Load Analysis']['optimize']
                )
                self.pop_up.close.connect(self.cl_window_closed)
            self.pop_up_window.show()
        except Exception as e:
            print('Error Opening Room -->> ', type(e), str(e))

    def load_new_buttons(self, room_name, room_type, button):
        parent_gb = button.parent()
        tb = QtWidgets.QToolButton(parent_gb)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/icons/" + room_type.lower() + ".png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        tb.setIcon(icon2)
        tb.setIconSize(QtCore.QSize(35, 35))
        tb.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        tb.setAutoRaise(True)
        tb.setObjectName(room_name)
        tb.setText(room_name)
        tb.setCursor(QtCore.Qt.PointingHandCursor)
        tb.clicked.connect(lambda: self.room_popup(room_name, room_type))
        tb.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        parent_gb.layout().insertWidget(parent_gb.layout().count() - 1, tb)
        parent_gb.layout().itemAt(parent_gb.layout().count() - 1).setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

    def load_saved_toolBox(self, appliances, retrofit={}):
        for i in range(self.tlbx_appliances.count()):
            self.tlbx_appliances.widget(i).setParent(None)
        self.create_toolBox_page(appliances, retrofit)

    def create_toolBox_page(self, appliances, retrofit={}):
        pprint(retrofit)
        try:
            for app_name in appliances:
                pow_rating = appliances[app_name]['power_rating']
                if retrofit != {}:
                    try:
                        clicked = retrofit[app_name]['index']
                        name = retrofit[app_name]['name']
                        power_rating = retrofit[app_name]['value']
                        self.create_toolBox_page_2(app_name, pow_rating, clicked, name, power_rating)
                    except (KeyError, TypeError):
                        power_rating = self.retrofit_appliances[app_name][str(retrofit[app_name])]['power_rating']
                        clicked = retrofit[app_name]
                        self.create_toolBox_page_2(app_name, pow_rating, clicked, power_rating=power_rating)
                else:
                    self.create_toolBox_page_2(app_name, pow_rating)
        except Exception as e:
            print('Error Loading before creating tool_box -->>', type(e), str(e))

    def create_toolBox_page_2(self, app_name, pow_rating, clicked=None, name='', power_rating=0.0):
        try:
            if app_name not in Ui_MainWindow.appliances:
                tlbx_app = QtWidgets.QWidget(self.tlbx_appliances)

                frame_1 = QtWidgets.QFrame(tlbx_app)
                frame_1.setMinimumSize(QtCore.QSize(130, 0))
                frame_1.setMaximumSize(QtCore.QSize(130, 16777215))
                font = QtGui.QFont()
                font.setFamily("Segoe UI Semibold")
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                frame_1.setFont(font)
                frame_1.setFrameShape(QtWidgets.QFrame.StyledPanel)
                frame_1.setFrameShadow(QtWidgets.QFrame.Raised)
                layout_appliance = QtWidgets.QVBoxLayout(frame_1)

                lbl_appliance_lbl = QtWidgets.QLabel(frame_1)
                lbl_appliance_lbl.setText('Appliance Rating')
                font = QtGui.QFont()
                font.setPointSize(10)
                lbl_appliance_lbl.setFont(font)
                layout_appliance.addWidget(lbl_appliance_lbl, 0, QtCore.Qt.AlignHCenter)

                lbl_appliance_rating = QtWidgets.QLabel(frame_1)
                lbl_appliance_rating.setText(str(pow_rating))
                font = QtGui.QFont()
                font.setFamily("MS Shell Dlg 2")
                font.setPointSize(24)
                lbl_appliance_rating.setFont(font)
                layout_appliance.addWidget(lbl_appliance_rating, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom)

                lbl_kw_appliance = QtWidgets.QLabel(frame_1)
                lbl_kw_appliance.setText('kW')
                font = QtGui.QFont()
                font.setPointSize(12)
                lbl_kw_appliance.setFont(font)
                layout_appliance.addWidget(lbl_kw_appliance, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
                frame_1.setLayout(layout_appliance)

                frame_2 = QtWidgets.QFrame(tlbx_app)
                frame_2.setMinimumSize(QtCore.QSize(130, 0))
                frame_2.setMaximumSize(QtCore.QSize(130, 16777215))
                font = QtGui.QFont()
                font.setFamily("Segoe UI Semibold")
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                frame_2.setFont(font)
                frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
                frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
                layout_retrofit = QtWidgets.QVBoxLayout(frame_2)

                lbl_retrofit_lbl = QtWidgets.QLabel(frame_2)
                lbl_retrofit_lbl.setText('Retrofit Rating')
                font = QtGui.QFont()
                font.setPointSize(10)
                lbl_retrofit_lbl.setFont(font)
                layout_retrofit.addWidget(lbl_retrofit_lbl, 0, QtCore.Qt.AlignHCenter)

                lbl_retrofit_rating = QtWidgets.QLabel(frame_2)
                lbl_retrofit_rating.setText(str(pow_rating if power_rating == 0.0 else power_rating))
                font = QtGui.QFont()
                font.setFamily("MS Shell Dlg 2")
                font.setPointSize(24)
                lbl_retrofit_rating.setFont(font)
                layout_retrofit.addWidget(lbl_retrofit_rating, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom)

                lbl_kw_retrofit = QtWidgets.QLabel(frame_2)
                lbl_kw_retrofit.setText('kW')
                font = QtGui.QFont()
                font.setPointSize(12)
                lbl_kw_retrofit.setFont(font)
                layout_retrofit.addWidget(lbl_kw_retrofit, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
                frame_2.setLayout(layout_retrofit)

                v_line = QtWidgets.QFrame(tlbx_app)
                v_line.setFrameShape(QtWidgets.QFrame.VLine)
                v_line.setFrameShadow(QtWidgets.QFrame.Sunken)

                gb_retrofit_appliances = QtWidgets.QGroupBox(tlbx_app)
                font = QtGui.QFont()
                font.setBold(True)
                font.setWeight(75)
                gb_retrofit_appliances.setFont(font)
                gb_retrofit_appliances.setTitle('Retrofit Appliance')

                stack = QtWidgets.QStackedWidget(gb_retrofit_appliances)
                temp = {'0': 'one', '1': 'one', '2': 'two', '3': 'three', '4': 'four', '5': 'five'}

                font = QtGui.QFont()
                font.setFamily("Segoe UI Semibold")
                font.setBold(True)

                widget1 = QtWidgets.QWidget(stack)

                widget1.setFont(font)

                layout1 = QtWidgets.QVBoxLayout(widget1)
                if app_name in self.retrofit_appliances:
                    for rating in self.retrofit_appliances[app_name]:
                        rd_star_retrofit = QtWidgets.QRadioButton(widget1)
                        rd_star_retrofit.setText(self.retrofit_appliances[app_name][rating]['name'])
                        icon9 = QtGui.QIcon()
                        icon9.addPixmap(QtGui.QPixmap(":/icons/icons/" + temp[rating] + " star.png"),
                                        QtGui.QIcon.Normal,
                                        QtGui.QIcon.Off)
                        rd_star_retrofit.setIcon(icon9)
                        rd_star_retrofit.setIconSize(QtCore.QSize(90, 20))
                        if int(rating) == clicked:
                            rd_star_retrofit.setChecked(True)
                        rd_star_retrofit.clicked.connect(
                            lambda: self.retrofit_appliance_chosen(app_name, stack, lbl_retrofit_rating, rating_spnbx,
                                                                   name_txtbx.text()))
                        layout1.addWidget(rd_star_retrofit)

                rd_star_retrofit = QtWidgets.QRadioButton(widget1)
                rd_star_retrofit.setText('Custom Retrofit Appliance')
                rd_star_retrofit.clicked.connect(
                    lambda: self.retrofit_appliance_chosen(app_name, stack, lbl_retrofit_rating, rating_spnbx,
                                                           name_txtbx.text()))
                layout1.addWidget(rd_star_retrofit)
                widget1.setLayout(layout1)

                widget2 = QtWidgets.QWidget(stack)
                widget2.setFont(font)
                label = QtWidgets.QLabel(widget2)
                label.setText('Name of Appliance')
                label.setAlignment(QtCore.Qt.AlignLeft)
                name_txtbx = QtWidgets.QLineEdit(widget2)
                name_txtbx.setFixedSize(150, 25)
                name_txtbx.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
                name_txtbx.textChanged.connect(lambda: self.name_changed(app_name, name_txtbx.text()))

                label2 = QtWidgets.QLabel(widget2)
                label2.setText('Power Rating')
                label2.setAlignment(QtCore.Qt.AlignLeft)
                rating_spnbx = QtWidgets.QDoubleSpinBox(widget2)
                rating_spnbx.setFixedSize(150, 25)
                rating_spnbx.setMaximum(999.99)
                rating_spnbx.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
                rating_spnbx.valueChanged.connect(
                    lambda: self.rating_changed(app_name, rating_spnbx.value(), lbl_retrofit_rating))

                if clicked == 6:
                    rd_star_retrofit.setChecked(True)
                    name_txtbx.setText(name)
                    rating_spnbx.setValue(power_rating)
                btn = QtWidgets.QPushButton(widget2)
                fonty = QtGui.QFont()
                fonty.setPointSize(8)
                fonty.setUnderline(True)
                fonty.setFamily("Segoe UI Semibold")
                btn.setFont(fonty)
                btn.setText('Choose Other Appliances')
                btn.clicked.connect(lambda: self.go_back_to_rating(stack))
                btn.setCursor(QtCore.Qt.PointingHandCursor)

                layout2 = QtWidgets.QVBoxLayout(widget2)
                layout2.addStretch()
                layout2.addWidget(label)
                layout2.addWidget(name_txtbx)
                layout2.addStretch()
                layout2.addWidget(label2)
                layout2.addWidget(rating_spnbx)
                layout2.addStretch()
                layout2.addWidget(btn, QtCore.Qt.AlignLeft)

                widget2.setLayout(layout2)

                stack.addWidget(widget1)

                stack.addWidget(widget2)
                stack.setCurrentIndex(0)

                layout_gb = QtWidgets.QVBoxLayout(tlbx_app)
                layout_gb.addWidget(stack)
                gb_retrofit_appliances.setLayout(layout_gb)

                h_box = QtWidgets.QHBoxLayout()
                h_box.addWidget(frame_1)
                h_box.addWidget(v_line)
                h_box.addWidget(frame_2)
                h_box.addWidget(gb_retrofit_appliances)
                tlbx_app.setLayout(h_box)
                self.tlbx_appliances.addItem(tlbx_app, app_name)
                Ui_MainWindow.appliances.append(app_name)
        except Exception as e:
            print('Error creating toolbox -->> ', type(e), str(e))

    def name_changed(self, app_name, name):
        try:
            self.retrofit_details[app_name]['name'] = name
        except Exception as e:
            print('Error Changing Name Label -->>', type(e), str(e))

    def rating_changed(self, app_name, value, lbl):
        try:
            self.retrofit_details[app_name]['value'] = value
            lbl.setText(str(value))
        except Exception as e:
            print('Error Changing Rating Label -->>', type(e), str(e))

    def go_back_to_rating(self, stack):
        try:
            stack.setCurrentIndex(0)
        except Exception as e:
            print('Error going back to ratings -->>', type(e), str(e))

    def retrofit_appliance_chosen(self, app_name, stack, lbl_retrofit_rating, double_spin=None, name=None):
        try:
            layout = stack.widget(0).layout()
            for i in range(layout.count()):
                if layout.itemAt(i).widget().isChecked():
                    if layout.itemAt(i).widget().text() == 'Custom Retrofit Appliance':
                        stack.setCurrentIndex(1)
                        self.retrofit_details[app_name] = {'index': 6, 'value': 0.0, 'name': '', 'custom': True}
                    else:
                        self.retrofit_details[app_name] = (i + 1)
                        lbl_retrofit_rating.setText(str(self.retrofit_appliances[app_name][str(5 - i)]['power_rating']))
                        break
        except Exception as e:
            print('Error retrieving clicked retrofit -->> ', type(e), str(e))

    def appliances_added(self, room_name, appliances):
        try:
            self.create_toolBox_page(appliances)
            self.rooms[room_name]['appliances'] = appliances
            self.pop_up_window.close()
        except Exception as e:
            print('Error Adding Appliance from Dashboard -->> ', type(e), str(e))

    def read_analyze_appliance_data(self):
        temp_appliances = {}
        for room in self.rooms:
            for app in self.rooms[room]['appliances']:
                power_rating = self.rooms[room]['appliances'][app]['power_rating']
                units = self.rooms[room]['appliances'][app]['units']
                op_hours = self.rooms[room]['appliances'][app]['operating_hours']

                temp_app = app
                i = 1
                while temp_app in temp_appliances:
                    if self.rooms[room]['appliances'][app]['power_rating'] == temp_appliances[app]['power_rating']:
                        units += temp_appliances[app]['units']
                        op_hours += temp_appliances[app]['operating_hours']
                        break
                    else:
                        temp_app = app + ' (' + str(i) + ')'
                temp_appliances[temp_app] = {}
                temp_appliances[temp_app]['power_rating'] = power_rating
                temp_appliances[temp_app]['units'] = units
                temp_appliances[temp_app]['operating_hours'] = op_hours
                temp_appliances[temp_app]['operating_hours'] = op_hours

        appliances = {}
        retrofit = {}
        for app_det in temp_appliances:
            pow_rating = 0
            try:
                pow_rating = self.retrofit_details[app_det]['value']
            except TypeError:
                star = self.retrofit_details[app_det]
                pow_rating = self.retrofit_appliances[app_det][str(6 - star)]['power_rating']
            if pow_rating < temp_appliances[app_det]['power_rating']:
                appliances[app_det] = temp_appliances[app_det]
                retrofit[app_det] = {
                    'power_rating': pow_rating,
                    'units': temp_appliances[app_det]['units'],
                    'operating_hours': temp_appliances[app_det]['operating_hours']
                }
        return {'appliances': appliances, 'retrofit': retrofit}

    def optimize(self):
        self.data_pages['Cooling Load Analysis']['optimize'] = True
        self.navigate_pages('Cooling Load Analysis')

    def aa_analyze(self):
        try:
            data = self.read_analyze_appliance_data()
            app_audit = ApplianceAudit(data['appliances'])
            result = app_audit.analyse(data['retrofit'])
            pprint(result)
            self.populate_app_result(result)
            self.plot_appliance_audit_graph(result)
        except Exception as e:
            print('Error with Appliance Audit Analysis -->> ', type(e), str(e))

    def cl_window_closed(self, cl_room, cl_data):
        try:
            self.rooms[cl_room]['cooling_load'] = cl_data
            self.tbl_summary_cl.setRowCount(0)
            # self.populate_cl_result()
            self.pop_up_window.close()
        except Exception as e:
            print('Error Closing Cooling Load Ananlysis Window -->> ', type(e), str(e))

    def populate_cl_result(self):
        try:
            for room in self.rooms:
                n = self.tbl_summary_cl.rowCount()
                self.tbl_summary_cl.insertRow(n)

                item1 = QtWidgets.QTableWidgetItem(str(room))
                item1.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
                self.tbl_summary_cl.setItem(n, 0, item1)

                item2 = QtWidgets.QTableWidgetItem(str(round(self.rooms[room]['cooling_load']['result']['cl_btu'], 2)))
                item2.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tbl_summary_cl.setItem(n, 1, item2)

                item3 = QtWidgets.QTableWidgetItem(str(round(self.rooms[room]['cooling_load']['result']['cl_tons'], 2)))
                item3.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tbl_summary_cl.setItem(n, 2, item3)

                item4 = QtWidgets.QTableWidgetItem(str(round(self.rooms[room]['cooling_load']['result']['eer'], 2)))
                item4.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tbl_summary_cl.setItem(n, 3, item4)

                item5 = QtWidgets.QTableWidgetItem(str(round(self.rooms[room]['cooling_load']['result']['cop'], 2)))
                item5.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tbl_summary_cl.setItem(n, 4, item5)

                item6 = QtWidgets.QTableWidgetItem(str(self.rooms[room]['cooling_load']['result']['rating']) + ' star')
                item6.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tbl_summary_cl.setItem(n, 5, item6)

            self.plot_cooling_load_graph()
        except Exception as e:
            print('Error Loading Cooling Load Table -->> ', type(e), str(e))

    def populate_app_result(self, result):
        try:
            self.tbl_summary_aa_audit.setRowCount(0)

            for app_name in result:
                row_pos = self.tbl_summary_aa_audit.rowCount()
                self.tbl_summary_aa_audit.insertRow(row_pos)
                item1 = QtWidgets.QTableWidgetItem(str(app_name).upper())
                item2 = QtWidgets.QTableWidgetItem(str(round(result[app_name]['BS'], 4)))
                item3 = QtWidgets.QTableWidgetItem(str(round(result[app_name]['EC'], 4)))
                item4 = QtWidgets.QTableWidgetItem(str(round(result[app_name]['EC retrofit'], 4)))
                item5 = QtWidgets.QTableWidgetItem(str(round(result[app_name]['ES'], 4)))
                item6 = QtWidgets.QTableWidgetItem(str(round(result[app_name]['LCC'], 4)))
                item7 = QtWidgets.QTableWidgetItem(str(round(result[app_name]['PWF'], 4)))
                item8 = QtWidgets.QTableWidgetItem(str(round(result[app_name]['Pay Back'], 4)))
                item9 = QtWidgets.QTableWidgetItem(str(round(result[app_name]['ROR'], 4)))

                item1.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
                item2.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                item3.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                item4.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                item5.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                item6.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                item7.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                item8.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                item9.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

                self.tbl_summary_aa_audit.setItem(row_pos, 0, item1)
                self.tbl_summary_aa_audit.setItem(row_pos, 1, item2)
                self.tbl_summary_aa_audit.setItem(row_pos, 2, item3)
                self.tbl_summary_aa_audit.setItem(row_pos, 3, item4)
                self.tbl_summary_aa_audit.setItem(row_pos, 4, item5)
                self.tbl_summary_aa_audit.setItem(row_pos, 5, item6)
                self.tbl_summary_aa_audit.setItem(row_pos, 6, item7)
                self.tbl_summary_aa_audit.setItem(row_pos, 7, item8)
                self.tbl_summary_aa_audit.setItem(row_pos, 8, item9)
        except Exception as e:
            print('Error Populating Appliances Result Table -->> ', type(e), str(e))

    def navigate_pages(self, page_title):
        print("navigate pages ", page_title)
        try:
            Ui_MainWindow.current_index = list(self.data_pages.keys()).index(page_title)
            self.stacked_main_windows.setCurrentIndex(self.data_pages[page_title]['main'])
            # self.stacked_main_windows.setCurrentIndex(0)
            print("count: ", self.stacked_main_windows.count())
            print(self.data_pages[page_title]['main'])

            self.stk_solar_pv_main.setCurrentIndex(self.data_pages[page_title]['solar'])
            self.stk_wind_turb_main.setCurrentIndex(self.data_pages[page_title]['wind'])
            # probably need to add this line when am done with my interface
            self.stk_electric_car_pv_main.setCurrentIndex(self.data_pages[page_title]['electric_car'])

            self.actionPrevious.setEnabled(self.data_pages[page_title]['prev'])
            self.actionNext.setEnabled(self.data_pages[page_title]['next'])
            self.actionAnalyze_Data.setEnabled(self.data_pages[page_title]['analyze'])
            self.actionOptimize.setEnabled(self.data_pages[page_title]['optimize'])
            self.Analyze_Battery.setEnabled(True)


            if page_title == 'Room':
                self.lbl_analysis_type.setVisible(True)
                self.lbl_analysis_type.setText('APPLIANCE AUDIT')
            elif page_title == 'Cooling Load Analysis':
                self.lbl_analysis_type.setVisible(True)
                if self.data_pages[page_title]['optimize']:
                    self.lbl_analysis_type.setText('ENERGY CONSUMPTION ANALYSIS')
                else:
                    self.lbl_analysis_type.setText('COOLING LOAD ANALYSIS')


                def get_room_type_count(room_type):
                    i = 0
                    for room in self.rooms:
                        if self.rooms[room]['room_type'].lower() == room_type:
                            i += 1
                    return i

                self.gbox_rooms_office.setVisible(False) if get_room_type_count(
                    'offices') == 0 else self.btn_add_office.setVisible(False)
                self.gbox_rooms_laboratories.setVisible(False) if get_room_type_count(
                    'laboratories') == 0 else self.btn_add_laboratory.setVisible(False)
                self.gbox_rooms_lecture_room.setVisible(False) if get_room_type_count(
                    'lecture rooms') == 0 else self.btn_add_lecture_room.setVisible(False)
                self.gbox_rooms_conference_room.setVisible(False) if get_room_type_count(
                    'conference rooms') == 0 else self.btn_add_conference_rooms.setVisible(False)
                self.gbox_rooms_others.setVisible(False) if get_room_type_count(
                    'others') == 0 else self.btn_add_others.setVisible(False)
            else:
                if page_title == "Rooms":    # use this to fix the coding analysis issue on the application
                    self.lbl_analysis_type.setText('APPLIANCE AUDIT')
                self.lbl_analysis_type.setVisible(True)
                self.btn_add_others.setVisible(True)
                self.btn_add_office.setVisible(True)
                self.btn_add_conference_rooms.setVisible(True)
                self.btn_add_laboratory.setVisible(True)
                self.btn_add_lecture_room.setVisible(True)

                self.gbox_rooms_office.setVisible(True)
                self.gbox_rooms_laboratories.setVisible(True)
                self.gbox_rooms_lecture_room.setVisible(True)
                self.gbox_rooms_conference_room.setVisible(True)
                self.gbox_rooms_others.setVisible(True)
        except Exception as e:
            print('Error Navigating through Pages -->> ', type(e), str(e))

    def next_page(self):
        try:
            Ui_MainWindow.current_index += 1
            if Ui_MainWindow.current_index == 4:
                self.populate_cl_result()
            page_title = list(self.data_pages.keys())[Ui_MainWindow.current_index]
            self.navigate_pages(page_title)
        except Exception as e:
            print('Error Moving to Next Page -->> ', type(e), str(e))

    def prev_page(self):
        try:
            Ui_MainWindow.current_index -= 1
            page_title = list(self.data_pages.keys())[Ui_MainWindow.current_index]
            self.navigate_pages(page_title)
        except Exception as e:
            print('Error Moving to Previous Page -->> ', type(e), str(e))

    def tree_view_item_changed(self):
        try:
            item = self.tree_project_structure.currentIndex()
            item_clicked = item.data()

            if item_clicked == 'Cooling Load Analysis':
                self.data_pages['Cooling Load Analysis']['optimize'] = False

            if item_clicked == 'Result':
                parent = item.parent()
                if parent.data() == 'Solar PV':
                    item_clicked = 'Result1'
                elif parent.data() == 'Wind Turbine':
                    item_clicked = 'Result2'
                elif parent.data() == 'Cooling Load Analysis':
                    item_clicked = 'Result'
                elif parent.data() == 'Electric Vehicle Charging Station':
                    # electic vehicle station recently added
                    item_clicked = 'Result3'
            self.navigate_pages(item_clicked)
        except Exception as e:
            print('Tree View Item Changed Error -->> ', type(e), str(e))

    def analyze(self):
        try:
            print("index: ", Ui_MainWindow.current_index)
            if Ui_MainWindow.current_index == 1:
                self.aa_analyze()
            elif Ui_MainWindow.current_index == 7 or Ui_MainWindow.current_index == 5:  # analyze solar pv has an index of 5
                self.analyze_solar_pv()
            elif Ui_MainWindow.current_index == 9:
                self.analyze_wind_turbine()
                self.actionFinal_Report.setVisible(True)
            elif Ui_MainWindow.current_index == 12:
                # this triggers the result page for electric car
                # but b4 i analyze i ensure that

                solar_power = self.qDoubleSB_e_h_solar_power_gen.value()  # solar power
                biomass_power = self.qDoubleSB_e_h_biomass_power_gen.value()  # biomass power
                wind_power = self.qDoubleSB_e_h_wind_power_gen.value()  # wind power
                charge_slow_rating = self.qDoubleSB_rating_s_charger.value()  # charger slow rating
                charge_medium_rating = self.qDoubleSB_rating_m_charger.value()  # charger medium rating
                charge_fast_rating = self.qDoubleSB_rating_f_charger.value()  # charger fast rating
                no_of_slow_chargers = self.qDoubleSB_num_s_charger.value()
                no_of_medium_chargers = self.qDoubleSB_num_m_charger.value()
                no_of_fast_chargers = self.qDoubleSB_num_f_charger.value()
                max_bess_capacity = self.qDoubleSB_e_h_max_bess_capacity.value()
                ev_charger_name = self.qComboBox_e_h_charger_name.text()

                # all_mandatory_fields_are_filled = (solar_power and biomass_power and wind_power and
                #                                    charge_slow_rating and charge_medium_rating and charge_fast_rating
                #                                    and no_of_fast_chargers and no_of_slow_chargers and no_of_medium_chargers
                #                                    and max_bess_capacity and ev_charger_name)
                self.analyze_electric_car()
                # if all_mandatory_fields_are_filled:
                #     self.analyze_electric_car()
                # else:
                #     msg = QtWidgets.QMessageBox()
                #     msg.setIcon(QtWidgets.QMessageBox.Information)
                #     msg.setText("Please Fill all Fields")
                #     msg.setInformativeText("Please Fill all nescessary fields required for calculation")
                #     msg.setWindowTitle("fill all fields")
                #     msg.exec_()
                #     return
            self.next_page()
        except Exception as e:
            print('Error Analyze Action -->> ', type(e), str(e))

    def plot_appliance_audit_graph(self, appliances):
        try:
            energy_usage = []
            energy_savings = []
            bill_savings = []
            labels = []

            for appliance in appliances:
                labels.append(appliance)
                energy_usage.append(appliances[appliance]['EC retrofit'])
                energy_savings.append(appliances[appliance]['ES'])
                bill_savings.append(appliances[appliance]['BS'])

            self.wid_summary_aa_figure_ax.clear()
            if not appliances:
                self.wid_summary_aa_figure_ax.yaxis.set_visible(False)
                self.wid_summary_aa_figure_ax.spines['left'].set_visible(False)
            else:
                p1 = self.wid_summary_aa_figure_ax.bar(labels, energy_usage, 0.3)
                p2 = self.wid_summary_aa_figure_ax.bar(labels, energy_savings, 0.3, bottom=energy_usage)
                self.wid_summary_aa_figure_ax.spines['bottom'].set_linewidth(1)
                self.wid_summary_aa_figure_ax.spines['left'].set_linewidth(1)
                self.wid_summary_aa_figure_ax.spines['left'].set_visible(True)
                self.wid_summary_aa_figure_ax.spines['top'].set_visible(False)
                self.wid_summary_aa_figure_ax.spines['right'].set_visible(False)

                self.wid_summary_aa_figure_ax.legend((p1[0], p2[0]), ('Energy Usage', 'Energy Savings'))

                self.wid_summary_aa_figure.canvas.draw()
        except Exception as e:
            print('Error graphing Appliance Audit Summary -->> ', type(e), str(e))

    def plot_bar_chart(self, labels, data, canvas, ax):
        try:
            ax.clear()
            if not data:
                ax.yaxis.set_visible(False)
                ax.spines['left'].set_visible(False)
            else:
                ax.bar(labels, data, 0.2, color='#097703')
                ax.spines['bottom'].set_linewidth(1)
                ax.spines['left'].set_linewidth(1)
                ax.spines['left'].set_visible(True)
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                canvas.canvas.draw()
        except Exception as e:
            print('Bar Chart Error', type(e), str(e))

    def plot_cooling_load_graph(self):
        try:
            cl_tons = []
            eer = []
            cop = []
            labels = []

            for room in self.rooms:
                labels.append(room)
                cl_tons.append(self.rooms[room]['cooling_load']['result']['cl_tons'])
                eer.append(self.rooms[room]['cooling_load']['result']['eer'])
                cop.append(self.rooms[room]['cooling_load']['result']['cop'])

            self.wid_summary_cl_figure_ax.clear()
            if not cl_tons:
                self.wid_summary_cl_figure_ax.yaxis.set_visible(False)
                self.wid_summary_cl_figure_ax.spines['left'].set_visible(False)
            else:
                p1 = self.wid_summary_cl_figure_ax.bar(range(len(labels)), cl_tons, 0.3, color='r', bottom=0)

                p2 = self.wid_summary_cl_figure_ax.bar([i + 0.3 for i in range(len(labels))], eer, 0.3, color='y',
                                                       bottom=0)
                self.wid_summary_cl_figure_ax.spines['bottom'].set_linewidth(1)
                self.wid_summary_cl_figure_ax.spines['left'].set_linewidth(1)
                self.wid_summary_cl_figure_ax.spines['left'].set_visible(True)
                self.wid_summary_cl_figure_ax.spines['top'].set_visible(False)
                self.wid_summary_cl_figure_ax.spines['right'].set_visible(False)

                self.wid_summary_cl_figure_ax.legend((p1[0], p2[0]), ('Cooling Load (Tons)', ' EER'))

                self.wid_summary_cl_figure.canvas.draw()

        except Exception as e:
            print('Error graphing Cooling Load Summary -->> ', type(e), str(e))

    def solar_pv_site_name_changed(self):
        try:
            site_name = self.cmbx_solar_stdt_name.currentText()
            if site_name in self.site_data:
                temp_site_data = self.site_data[site_name]
                self.populate_solar_pv_site_data(temp_site_data)
        except Exception as e:
            print('Solar PV Site Name Changed', type(e), str(e))

    def populate_solar_pv_site_data(self, temp_site_data):
        self.txt_solar_stdt_type.setText(temp_site_data['installation_type'])
        self.txt_solar_stdt_site.setText(temp_site_data['site'])
        self.txt_solar_stdt_lat.setText(str(temp_site_data['latitude']))
        self.txt_solar_stdt_long.setText(str(temp_site_data['longitude']))
        self.txt_solar_stdt_elev.setText(str(temp_site_data['elevation']))
        self.spbox_solar_stdt_no_wings.setValue(temp_site_data['no_wings'])
        self.txt_solar_stdt_area.setText(str(temp_site_data['area']))
        self.spbox_solar_stdt_pitch.setValue(temp_site_data['pitch'])

    def solar_pv_inverter_name_changed(self):
        inverter_name = self.cmbx_solar_indt_name.currentText()

        if inverter_name in self.inverter_spec:
            inverter_spec = self.inverter_spec[inverter_name]
            self.populate_solar_pv_inverter_data(inverter_spec)

    def populate_solar_pv_inverter_data(self, temp_inverter_spec):
        try:
            self.txt_solar_indt_type.setText(temp_inverter_spec['type'])
            self.txt_solar_indt_max_mpptv.setText(str(temp_inverter_spec['max_inp_volt']))
            self.spbox_solar_indt_mppt_units.setValue(temp_inverter_spec['mppt_units'])
            self.txt_solar_indt_eff.setText(str(temp_inverter_spec['eff']))
            self.txt_solar_indt_mpptv_l.setText(str(temp_inverter_spec['mppt_volt_range_l']))
            self.txt_solar_indt_mpptv_u.setText(str(temp_inverter_spec['mppt_volt_range_u']))
        except Exception as e:
            print(type(e), str(e))

    def solar_pv_module_name_changed(self):
        try:
            module_name = self.cmbx_solar_mddt_name.currentText()
            if module_name in self.module_spec:
                module_spec = self.module_spec[module_name]
                self.populate_solar_pv_module_data(module_spec)
        except Exception as e:
            print('Solar PV Module Name Changed', type(e), str(e))

    def populate_solar_pv_module_data(self, module_spec):
        self.txt_solar_mddt_type.setText(module_spec['cell_type'])
        self.txt_solar_mddt_rated_power.setText(str(module_spec['rated power']))
        self.txt_solar_mddt_max_pow_volt.setText(str(module_spec['max_p_volt']))
        self.txt_solar_mddt_max_pow_curr.setText(str(module_spec['max_p_cur']))
        self.txt_solar_mddt_open_circuit_volt.setText(str(module_spec['open_c_vol']))
        self.txt_solar_mddt_short_circuit_volt.setText(str(module_spec['short_c_cur']))
        self.txt_solar_mddt_fuse_rating.setText(str(module_spec['fuse_rating']))
        self.txt_solar_mddt_max_sys_volt.setText(str(module_spec['max_sys_volt']))
        self.txt_solar_mddt_op_temp_l.setText(str(module_spec['op_temp_l']))
        self.txt_solar_mddt_op_temp_u.setText(str(module_spec['op_temp_u']))
        self.txt_solar_mddt_pow_tol_l.setText(str(module_spec['pow_tol_l']))
        self.txt_solar_mddt_pow_tol_u.setText(str(module_spec['pow_tol_u']))

        self.txt_solar_mddt_temp_coeff_p.setText(str(module_spec['Temp Coeff']['temp_coeff_p']))
        self.txt_solar_mddt_temp_coeff_v.setText(str(module_spec['Temp Coeff']['temp_coeff_v']))
        self.txt_solar_mddt_temp_coeff_c.setText(str(module_spec['Temp Coeff']['temp_coeff_i']))

        self.txt_solar_mddt_dim_l.setText(str(module_spec['mod_dim']['length']))
        self.txt_solar_mddt_dim_b.setText(str(module_spec['mod_dim']['breadth']))
        self.txt_solar_mddt_dim_h.setText(str(module_spec['mod_dim']['height']))

        self.txt_solar_mddt_eff.setText(str(module_spec['mod_eff']))
        self.txt_solar_mddt_weight.setText(str(module_spec['weight']))

    def slider_value_changed(self, slider):
        try:
            constant_layout = self.gbox_solar_constants.layout()
            index = constant_layout.indexOf(slider)
            row, column, row_span, column_span = constant_layout.getItemPosition(index)
            constant_layout.itemAtPosition(row, column + 1).widget().setText(str(slider.value() / 100))
        except Exception as e:
            print('Slider Changed', type(e), str(e))

    def slider_text_value_change(self, textbox):
        try:
            constant_layout = self.gbox_solar_constants.layout()
            index = constant_layout.indexOf(textbox)
            row, column, row_span, column_span = constant_layout.getItemPosition(index)
            constant_layout.itemAtPosition(row, column - 1).widget().setValue(float(textbox.text()) * 100)
        except Exception as e:
            print(type(e), str(e))

    def select_all_month(self):
        try:
            for c_box in self.gb_solar_months.children():
                if isinstance(c_box, QtWidgets.QCheckBox):
                    c_box.setChecked(self.cbox_solar_months_selectall.checkState())
        except Exception as e:
            print(type(e), str(e))

    def select_month(self):
        self.cbox_solar_months_selectall.setChecked(True)
        for c_box in self.gb_solar_months.children():
            if isinstance(c_box, QtWidgets.QCheckBox):
                if c_box.text() == 'Select All':
                    continue
                if not c_box.isChecked():
                    self.cbox_solar_months_selectall.setChecked(False)
                    break

    def wind_turbine_site_name_changed(self):
        try:
            site_name = self.cmbx_wind_turb_site_name.currentText()

            if site_name in self.wt_site_data:
                site_dict = self.wt_site_data[site_name]
                self.populate_wind_turbine_site_data(site_dict)
        except Exception as e:
            print(type(e), str(e))

    def evcs_site_name_changed(self):
        try:
            site_name = self.qComboBox_e_h_location.currentText()
            if site_name in self.evcs_site_data:
                site_dict = self.evcs_site_data[site_name]
                self.populate_electric_car_with_site_data(site_dict)
        except Exception as e:
            print(type(e), str(e))

    def populate_wind_turbine_site_data(self, site_dict):
        self.txt_wind_turb_stdt_long.setText(str(site_dict['location']['long']))
        self.txt_wind_turb_stdt_lat.setText(str(site_dict['location']['lat']))

        self.txt_wind_turb_ardt_den.setText(str(site_dict['air_data']['air_density']))
        self.txt_wind_turb_ardt_temp.setText(str(site_dict['air_data']['temp']))
        self.txt_wind_turb_ardt_alt.setText(str(site_dict['air_data']['altitude']))
        self.txt_wind_turb_ardt_press.setText(str(site_dict['air_data']['pressure']))

        self.txt_wind_turb_wddt_vel.setText(str(site_dict['wind_dist_data']['velocity']))
        self.txt_wind_turb_wddt_height.setText(str(site_dict['wind_dist_data']['height']))
        self.txt_wind_turb_wddt_shape_param.setText(str(site_dict['wind_dist_data']['w_shape_param']))
        self.txt_wind_turb_wddt_scale_param.setText(str(site_dict['wind_dist_data']['w_scale_param']))

    def wind_turbine_turbine_name_changed(self):
        try:
            t_name = self.cmbx_wind_turb_tbin_name.currentText()

            if t_name in self.wt_t_data:
                t_dict = self.wt_t_data[t_name]
                self.populate_wind_turbine_turbine_data(t_dict)
        except Exception as e:
            print(type(e), str(e))

    def populate_wind_turbine_turbine_data(self, t_dict):
        self.txt_wind_turb_tbin_rated_pow.setText(str(t_dict['rated_power']))
        self.txt_wind_turb_tbin_cut_in.setText(str(t_dict['cut_in_wind_speed']))
        self.txt_wind_turb_tbin_cut_out.setText(str(t_dict['cut_out_wind_speed']))
        self.txt_wind_turb_tbin_rotor_diam.setText(str(t_dict['rotor_diameter']))
        self.txt_wind_turb_tbin_hub_height.setText(str(t_dict['hub_height']))
        self.spbx_wind_turb_tbin_units.setValue(t_dict['units'])

        self.txt_wind_turb_tbin_blade_length.setText(str(t_dict['blade_length']))
        self.spbx_wind_turb_tbin_no_blades.setValue(t_dict['no_blades'])

    def read_solar_pv_site_data(self):
        try:
            site_data = {}
            site_name = self.cmbx_solar_stdt_name.currentText()
            site_data[site_name] = {}

            site_data[site_name]['installation_type'] = self.txt_solar_stdt_type.text()
            site_data[site_name]['site'] = self.txt_solar_stdt_site.text()
            site_data[site_name]['latitude'] = float(self.txt_solar_stdt_lat.text())
            site_data[site_name]['longitude'] = float(self.txt_solar_stdt_long.text())
            site_data[site_name]['elevation'] = float(self.txt_solar_stdt_elev.text())
            site_data[site_name]['no_wings'] = self.spbox_solar_stdt_no_wings.value()
            site_data[site_name]['area'] = float(self.txt_solar_stdt_area.text())
            site_data[site_name]['pitch'] = self.spbox_solar_stdt_pitch.value()

            return site_data
        except Exception as e:
            print(type(e), str(e))

    def read_electric_car_pv_site_data(self):
        try:
            site_data = {}
            # site_name = self.cmbx_solar_stdt_name.currentText()

            site_name = "UNILAG"
            site_data[site_name] = {}

            site_data[site_name]["ev_charger_name"] = self.qComboBox_e_h_charger_name.text()
            site_data[site_name]['solar_power'] = float(self.qDoubleSB_e_h_solar_power_gen.value())  # solar power
            site_data[site_name]['biomass_power'] = float(self.qDoubleSB_e_h_biomass_power_gen.value())  # biomass power
            site_data[site_name]['wind_power'] = float(self.qDoubleSB_e_h_wind_power_gen.value())  # wind power
            site_data[site_name]['charger_slow_rating'] = float(
                self.qDoubleSB_rating_s_charger.value())  # charger slow rating
            site_data[site_name]['charger_medium_rating'] = float(
                self.qDoubleSB_rating_m_charger.value())  # charger medium rating
            site_data[site_name]['charger_fast_rating'] = float(
                self.qDoubleSB_rating_f_charger.value())  # charger fast rating
            site_data[site_name]['slow_charger_numbers'] = int(self.qDoubleSB_num_s_charger.value())
            site_data[site_name]['medium_charger_numbers'] = int(self.qDoubleSB_num_m_charger.value())
            site_data[site_name]['fast_charger_numbers'] = int(self.qDoubleSB_num_f_charger.value())
            site_data[site_name]['max_bess_capacity'] = float(self.qDoubleSB_e_h_max_bess_capacity.value())
            site_data[site_name]["save"] = self.qCheckBox_e_h_save_power.isChecked()
            print(site_data)
            return site_data
        except Exception as e:
            print(type(e), str(e))


    def read_electric_car_pv_cost_data(self):
        data = dict()
        data["condenser_cost"] = self.qComboBox_e_h_cost_condeser.value()
        data["cooling_tower"] = self.qDoubleSB_e_h_cost_cooling_tower.value()
        data["pump_cost"] = self.qDoubleSB_e_h_cost_pump.value()
        data["stack_cost"] = self.qDoubleSB_e_h_cost_stack.value()
        data["wind_turbine_cost"] = self.qDoubleSB_e_h_cost_wind_turbine.value()
        data["num_wind_turbine_cost"] = self.qSpinBox_e_h_cost_num_wind_turbine.value()
        data["charging_rate_cost"] = self.qDoubleSB_e_h_cost_charging_rate.value()
        data["cost_time_s_charger"] = self.qSpinBox_e_h_cost_time_s_charger.value()
        data["cost_time_m_charger"] = self.qSpinBox_e_h_cost_time_m_charger.value()
        data["cost_time_f_charger"] = self.qSpinBox_e_h_cost_time_f_charger.value()
        data["cost_tariff_rate"] = self.qDoubleSB_e_h_cost_tariff_rate.value()
        data["cost_time_2_grid"] = self.qSpinBox_e_h_cost_time_to_grid.value()
        data["maintenance_cost"] = self.qDoubleSB_e_h_cost_maintenance.value()
        data["save_cost"] = self.qCheckBox_e_h_save_cost.isChecked()
        data["cost_location"] = self.qComboBox_e_h_cost_location.currentText()
        data["cost_of_land"] = self.qDoubleSB_e_h_cost_land.value()
        data["charger_name"] = self.qComboBox_e_h_cost_charger_name.currentText()
        data["cost_s_charger"] = self.qDoubleSB_e_h_cost_s_charger.value()
        data["cost_m_charger"] = self.qDoubleSB_e_h_cost_m_charger.value()
        data["cost_f_charger"] = self.qDoubleSB_e_h_cost_f_charge.value()
        data["cost_battery_name"] = self.qComboBox_e_h_cost_battery_name.currentText()
        data["cost_battery"] = self.qDoubleSB_e_h_cost_battery.value()
        data["cost_num_battery"] = self.qDoubleSB_e_h_cost_num_battery.value()
        data["solar_panel_name"] = self.qComboBox_e_h_cost_solar_panel_name.currentText()
        data["solar_panel_cost"] = self.qDoubleSB_e_h_cost_solar_panel.value()
        data["solar_panel_number"] = self.qSpinBox_e_h_cost_num_solar_panel.value()
        data["cost_combustor"] = self.qDoubleSB_e_h_cost_combustor.value()
        data["boiler_cost"] = self.qDoubleSB_e_h_cost_boiler.value()
        data["steam_turbine_cost"] = self.qDoubleSB_e_h_cost_steam_turbine.value()
        data["generator_cost"] = self.qDoubleSB_e_h_cost_generator.value()


        print("data =>", data)
        return data

    def read_solar_pv_inverter_data(self):
        try:
            inverter_data = {}
            inverter_name = self.cmbx_solar_indt_name.currentText()

            inverter_data[inverter_name] = {}

            inverter_data[inverter_name]['type'] = self.txt_solar_indt_type.text()
            inverter_data[inverter_name]['max_inp_volt'] = float(self.txt_solar_indt_max_mpptv.text())
            inverter_data[inverter_name]['mppt_volt_range_u'] = float(self.txt_solar_indt_mpptv_u.text())
            inverter_data[inverter_name]['mppt_volt_range_l'] = float(self.txt_solar_indt_mpptv_l.text())
            inverter_data[inverter_name]['mppt_units'] = self.spbox_solar_indt_mppt_units.value()
            inverter_data[inverter_name]['eff'] = float(self.txt_solar_indt_eff.text())

            return inverter_data
        except Exception as e:
            print('Value Error', type(e), str(e))

    def read_solar_pv_module_data(self):
        try:
            module_spec = {}
            module_name = self.cmbx_solar_mddt_name.currentText()
            module_spec[module_name] = {}
            module_spec[module_name]['cell_type'] = self.txt_solar_mddt_type.text()
            module_spec[module_name]['rated power'] = float(self.txt_solar_mddt_rated_power.text())
            module_spec[module_name]['max_p_volt'] = float(self.txt_solar_mddt_max_pow_volt.text())
            module_spec[module_name]['max_p_cur'] = float(self.txt_solar_mddt_max_pow_curr.text())
            module_spec[module_name]['open_c_vol'] = float(self.txt_solar_mddt_open_circuit_volt.text())
            module_spec[module_name]['short_c_cur'] = float(self.txt_solar_mddt_short_circuit_volt.text())
            module_spec[module_name]['fuse_rating'] = float(self.txt_solar_mddt_fuse_rating.text())
            module_spec[module_name]['max_sys_volt'] = float(self.txt_solar_mddt_max_sys_volt.text())
            module_spec[module_name]['op_temp_l'] = float(self.txt_solar_mddt_op_temp_l.text())
            module_spec[module_name]['op_temp_u'] = float(self.txt_solar_mddt_op_temp_u.text())
            module_spec[module_name]['pow_tol_l'] = float(self.txt_solar_mddt_pow_tol_l.text())
            module_spec[module_name]['pow_tol_u'] = float(self.txt_solar_mddt_pow_tol_u.text())

            module_spec[module_name]['Temp Coeff'] = {}
            module_spec[module_name]['Temp Coeff']['temp_coeff_p'] = float(self.txt_solar_mddt_temp_coeff_p.text())
            module_spec[module_name]['Temp Coeff']['temp_coeff_v'] = float(self.txt_solar_mddt_temp_coeff_v.text())
            module_spec[module_name]['Temp Coeff']['temp_coeff_i'] = float(self.txt_solar_mddt_temp_coeff_c.text())

            module_spec[module_name]['mod_dim'] = {}

            module_spec[module_name]['mod_dim']['length'] = float(self.txt_solar_mddt_dim_l.text())
            module_spec[module_name]['mod_dim']['breadth'] = float(self.txt_solar_mddt_dim_b.text())
            module_spec[module_name]['mod_dim']['height'] = float(self.txt_solar_mddt_dim_h.text())

            module_spec[module_name]['mod_eff'] = float(self.txt_solar_mddt_eff.text())
            module_spec[module_name]['weight'] = float(self.txt_solar_mddt_weight.text())

            return module_spec
        except Exception as e:
            print(type(e), str(e))

    def read_constants(self):
        try:
            constants = dict()

            constants['amb_temp'] = float(self.dspbox_solar_const_amb_temp.value())
            constants['tolerance'] = float(self.hslider_solar_const_tol.value() / 100)
            constants['dirt_loss'] = float(self.hslider_solar_const_dirt_loss.value() / 100)
            constants['assumed_dc_loss'] = float(self.hslider_solar_const_assumed_dc_loss.value() / 100)
            constants['assumed_ac_loss'] = float(self.hslider_solar_const_assumed_ac_loss.value() / 100)
            constants['temp_effect'] = float(self.hslider_solar_const_temp_effect.value() / 100)
            constants['safety_marg'] = float(self.hslider_solar_const_safety_margin.value() / 100)
            constants['eff_cell_temp'] = float(self.dspbox_solar_const_eff_cel_temp.value())

            temp_months = []
            for c_box in self.gb_solar_months.children():
                if isinstance(c_box, QtWidgets.QCheckBox) and c_box.isChecked():
                    if c_box.text() != 'Select All':
                        temp_months.append(c_box.objectName().split('_')[-1])
            constants['months'] = temp_months

            return constants
        except Exception as e:
            print(type(e), str(e))

    def read_insolation_data(self):
        try:
            insolation = dict()
            row_count = self.tbl_solar_insolation.rowCount()
            column_count = self.tbl_solar_insolation.columnCount()
            for column in range(column_count):
                insolation_key = self.tbl_solar_insolation.horizontalHeaderItem(column).text().strip()
                insolation[insolation_key] = {}
                for row in range(row_count):
                    month_key = self.tbl_solar_insolation.verticalHeaderItem(row).text().lower().strip()
                    value = float(self.tbl_solar_insolation.item(row, column).text())
                    insolation[insolation_key][month_key] = value
            return insolation
        except Exception as e:
            print(type(e), str(e))

    def analyze_solar_pv(self):
        try:
            site_data = self.read_solar_pv_site_data()
            inverter_data = self.read_solar_pv_inverter_data()
            module_data = self.read_solar_pv_module_data()
            constants = self.read_constants()
            insolation = self.read_insolation_data()
            pprint(insolation)
            print("*"*1)
            if self.cbox_solar_stdt_save.isChecked():
                with open('JSON files/sp_site_data.json', 'w') as f:
                    f.write(json.dumps({**self.inverter_spec, **site_data}, indent=4, sort_keys=False))
            print("*" * 2)
            if self.cbox_solar_indt_save.isChecked():
                with open('JSON files/sp_inverter_spec.json', 'w') as f:
                    f.write(json.dumps({**self.inverter_spec, **inverter_data}, indent=4, sort_keys=False))
            print("*" * 3)
            if self.cbox_solar_mddt_save.isChecked():
                with open('JSON files/sp_module_spec.json', 'w') as f:
                    f.write(json.dumps({**self.inverter_spec, **module_data}, indent=4, sort_keys=False))
            print("*" * 4)
            site_name = self.cmbx_solar_stdt_name.currentText()
            print("site_name: ", site_name)
            print("*" * 5)
            module_name = self.cmbx_solar_mddt_name.currentText()
            print("*" * 6)
            inverter_name = self.cmbx_solar_indt_name.currentText()
            print("*" * 7)
            self.saved_data['solar_pv'] = {
                'site_data': {'name': site_name, 'data': site_data[site_name]} if site_data else dict(),
                'module_data': {'name': module_name, 'data': module_data[module_name]} if module_data else dict(),
                'inverter_data': {'name': inverter_name, 'data': inverter_data[inverter_name]} if inverter_data else dict(),
                'constants': {'data': constants}
            }
            print("*" * 8)
            if not site_data or not module_data or not inverter_name:
                return
            print("*" * 9)
            spv = SolarPV(site_data=site_data[site_name], module_spec=module_data[module_name],
                          inverter_spec=inverter_data[inverter_name],
                          constants=constants, insolation=insolation)
            print("*"*10)
            data = spv.analyze()
            print("*"*11)
            self.energy_sources['solar_pv'] = data
            print("*"*12)
            self.populate_solar_pv_output()
            print("*"*13)
            self.stk_solar_pv_main.setCurrentIndex(3)
            return True
        except Exception as e:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText(str(type(e)))
            msg.setInformativeText(str(e))
            msg.setWindowTitle("An Error Occured")
            msg.exec_()
            print('fhjg', type(e), str(e))
            print(e)
        finally:
            self.saved_data['solar_pv'] = {
                'site_data': {'name': "", 'data': {}},
                'module_data': {'name': "", 'data': {}},
                'inverter_data': {'name': "", 'data': {}},
                'constants': {'data': {}}
            }

    def analyze_electric_car(self):
        try:
            site_data = self.read_electric_car_pv_site_data()  # change this to read electric power data
            cost_data = self.read_electric_car_pv_cost_data()  # change this to read electric cost data

            print("c -> ", cost_data)

            electric_car = ElectricCar(site_data=site_data, cost_data=cost_data)

            data = electric_car.analyse()
            print("data: ", data)
            self.saved_data["electric_car"] = dict()
            self.saved_data["electric_car"]["site_data"] = site_data
            self.saved_data["electric_car"]["analyzed_output"] = data

            print("checkbox, ", self.qCheckBox_e_h_save_power.isChecked())
            if self.qCheckBox_e_h_save_power.isChecked():

                if os.path.isfile('JSON files/evcs_site_data.json'):
                    with open("JSON files/evcs_site_data.json", "r+") as file:
                        old_data = json.load(file)
                        old_data.update(site_data)
                        file.truncate(0)
                        file.seek(0)
                        print("o: ", old_data)
                        print("here")
                        json.dump(old_data, file, indent=4, sort_keys=False)
                        print("done")
                else:
                    # just write the data to a new file
                    with open("JSON files/evcs_site_data.json", "w+") as file:
                        json.dump(site_data, file, indent=4, sort_keys=False)


            self.populate_solar_pv_output()  # change this to populate to electric car output
            self.populate_electric_car_pv_output(data)
            self.populate_electric_car_cost_output(data.get("cost_data"))
            self.stk_electric_car_pv_main.setCurrentIndex(8)  # set index to result page
            return True
        except Exception as e:
            print('fhjg', type(e), str(e))

    def populate_electric_car_with_site_data(self, data):

        self.qDoubleSB_e_h_solar_power_gen.setValue(str(data.get("solar_power")))
        self.qDoubleSB_e_h_biomass_power_gen.setValue(str(data.get("biomass_power")))
        self.qDoubleSB_e_h_wind_power_gen.setValue(str(data.get("wind_power")))
        self.qDoubleSB_rating_s_charger.setValue(data.get("charger_slow_rating"))
        self.qDoubleSB_rating_m_charger.setValue(data.get("charger_medium_rating"))
        self.qDoubleSB_rating_f_charger.setValue(data.get("charger_fast_rating"))
        self.qDoubleSB_num_s_charger.setValue(data.get("slow_charger_numbers"))
        self.qDoubleSB_num_m_charger.setValue(data.get("medium_charger_numbers"))
        self.qDoubleSB_num_f_charger.setValue(data.get("fast_charger_numbers"))
        self.self.qCheckBox_e_h_save_power.setChecked(True)
        self.qDoubleSB_e_h_max_bess_capacity.setText(str(data.get("max_bess_capacity")))

    def optimize_solar_pv(self):
        try:
            site_data = self.read_solar_pv_site_data()
            inverter_data = self.read_solar_pv_inverter_data()
            module_data = self.read_solar_pv_module_data()
            constants = self.read_constants()
            insolation = self.read_insolation_data()
            pprint(insolation)
            if self.cbox_solar_stdt_save.isChecked():
                with open('JSON files/sp_site_data.json', 'w') as f:
                    f.write(json.dumps(
                        {**self.inverter_spec, **site_data}, indent=4, sort_keys=False))

            if self.cbox_solar_indt_save.isChecked():
                with open('JSON files/sp_inverter_spec.json', 'w') as f:
                    f.write(json.dumps(
                        {**self.inverter_spec, **inverter_data}, indent=4, sort_keys=False))

            if self.cbox_solar_mddt_save.isChecked():
                with open('JSON files/sp_module_spec.json', 'w') as f:
                    f.write(json.dumps(
                        {**self.inverter_spec, **module_data}, indent=4, sort_keys=False))

            site_name = self.cmbx_solar_stdt_name.currentText()
            module_name = self.cmbx_solar_mddt_name.currentText()
            inverter_name = self.cmbx_solar_indt_name.currentText()

            self.saved_data['solar_pv'] = {
                'site_data': {'name': site_name, 'data': site_data[site_name]},
                'module_data': {'name': module_name, 'data': module_data[module_name]},
                'inverter_data': {'name': inverter_name, 'data': inverter_data[inverter_name]},
                'constants': {'data': constants}
            }

            if not site_data or not module_data or not inverter_name:
                return

            spv = SolarPV(site_data=site_data[site_name], module_spec=module_data[module_name],
                          inverter_spec=inverter_data[inverter_name],
                          constants=constants, insolation=insolation)

            data = spv.analyze()
            self.energy_sources['solar_pv'] = data
            self.populate_solar_pv_output()
            self.stk_solar_pv_main.setCurrentIndex(3)
            return True
        except Exception as e:
            print('fhjg', type(e), str(e))

    def populate_solar_pv_output(self):
        try:
            row_count = self.tbl_solar_output_result.rowCount()
            for row in range(row_count):
                row_name = self.tbl_solar_output_result.verticalHeaderItem(row).text().lower()
                item = QtWidgets.QTableWidgetItem(str(round(self.energy_sources['solar_pv'][row_name], 2)))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tbl_solar_output_result.setItem(row, 0, item)

            row_count = self.tbl_solar_output_psh.rowCount()
            for row in range(row_count):
                row_name = self.tbl_solar_output_psh.verticalHeaderItem(row).text().lower()
                months = {'january': 'jan', 'february': 'feb', 'march': 'mar', 'april': 'apr', 'may': 'may',
                          'june': 'jun', 'july': 'jul', 'august': 'aug', 'september': 'sept', 'october': 'oct',
                          'november': 'nov', 'december': 'dec'}
                item = QtWidgets.QTableWidgetItem(
                    str(round(self.energy_sources['solar_pv']['psh'][months[row_name]], 2)))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tbl_solar_output_psh.setItem(row, 0, item)

            label = list(self.energy_sources['solar_pv']['psh'].keys())
            data = list(self.energy_sources['solar_pv']['psh'].values())
            self.plot_bar_chart(label, data, self.solar_output_figure, self.solar_output_figure_ax)
        except Exception as e:
            print(type(e), str(e))

    def populate_electric_car_pv_output(self, result):
        self.label_result_evcs_power_generated.setText("%s" % result.get("output_a"))
        if result.get("deficient_power") <= 0:
            self.label_result_evcs_power_consumed.setText("%s" % result.get("output_b"))
        else:
            self.label_result_evcs_power_consumed.setText(
                "%s (deficient power: -%s)" % (result.get("output_b"), result.get("deficient_power")))
        self.label_result_evcs_power_supplied_1.setText("%s" % result.get("output_c"))
        self.label_result_evcs_power_supplied_2.setText("%s" % result.get("output_d"))
        self.label_result_evcs_watts_1.setText("Watts")
        self.label_result_evcs_watts_2.setText("Watts")
        self.label_result_evcs_watts_3.setText("Watts")
        self.label_result_evcs_watts_4.setText("Watts")
        return

    def populate_electric_car_cost_output(self, cost_data):
        text_4_label_16 = "N%d is the investment cost required to build the charging station." % (cost_data.get("output_e"))
        if (cost_data.get("output_e")==cost_data.get("output_f")):
            text_4_label_17 = "There is no maintenance cost."
        else:
            text_4_label_17 = "N%d is the total cost required to build the charging station including investment and maintenance cost." % (cost_data.get("output_f"))
        text_4_label_18 = "N%d is the revenue generated from charging the entered number of electric vehicles." % (cost_data.get("output_g"))
        text_4_label_19 = "N%d is the revenue generated from transmitting excess power to the grid." % (cost_data.get("output_h"))
        text_4_label_20 = "N%d is the total revenue generated from the charging station." % (cost_data.get("output_i"))
        if cost_data.get("output_j") > 0:
            text_4_label_21 = "N%d is the net profit obtained from operating the charging station." % (cost_data.get("output_j"))
        elif cost_data.get("output_j") < 0:
            text_4_label_21 = "N%d is the net loss obtained from operating the charging station." % (
                cost_data.get("output_j"))
        else:
            text_4_label_21 = "There is no net profilt/loss."

        self.qLabel_evcs_16.setText(text_4_label_16)
        self.qLabel_evcs_17.setText(text_4_label_17)
        self.qLabel_evcs_18.setText(text_4_label_18)
        self.qLabel_evcs_19.setText(text_4_label_19)
        self.qLabel_evcs_20.setText(text_4_label_20)
        self.qLabel_evcs_21.setText(text_4_label_21)


    def read_wind_turb_site_data(self):
        try:
            temp_site_dict = dict()
            site_name = self.cmbx_wind_turb_site_name.currentText()
            temp_site_dict[site_name] = {'location': {}, 'air_data': {}, 'wind_dist_data': {}}

            temp_site_dict[site_name]['location']['lat'] = float(self.txt_wind_turb_stdt_lat.text())
            temp_site_dict[site_name]['location']['long'] = float(self.txt_wind_turb_stdt_long.text())

            temp_site_dict[site_name]['air_data']['air_density'] = float(self.txt_wind_turb_ardt_den.text())
            temp_site_dict[site_name]['air_data']['temp'] = float(self.txt_wind_turb_ardt_temp.text())
            temp_site_dict[site_name]['air_data']['altitude'] = float(self.txt_wind_turb_ardt_alt.text())
            temp_site_dict[site_name]['air_data']['pressure'] = float(self.txt_wind_turb_ardt_press.text())

            temp_site_dict[site_name]['wind_dist_data']['w_shape_param'] = float(
                self.txt_wind_turb_wddt_shape_param.text())
            temp_site_dict[site_name]['wind_dist_data']['w_scale_param'] = float(
                self.txt_wind_turb_wddt_scale_param.text())
            temp_site_dict[site_name]['wind_dist_data']['velocity'] = float(self.txt_wind_turb_wddt_vel.text())
            temp_site_dict[site_name]['wind_dist_data']['height'] = float(self.txt_wind_turb_wddt_height.text())
            return temp_site_dict
        except Exception as e:
            print(type(e), str(e))

    def read_wind_turb_tbin_data(self):
        try:
            temp_t_dict = dict()
            t_name = self.cmbx_wind_turb_tbin_name.currentText()
            temp_t_dict[t_name] = {}

            temp_t_dict[t_name]['rated_power'] = float(self.txt_wind_turb_tbin_rated_pow.text())
            temp_t_dict[t_name]['cut_in_wind_speed'] = float(self.txt_wind_turb_tbin_cut_in.text())
            temp_t_dict[t_name]['cut_out_wind_speed'] = float(self.txt_wind_turb_tbin_cut_out.text())
            temp_t_dict[t_name]['rotor_diameter'] = float(self.txt_wind_turb_tbin_rotor_diam.text())
            temp_t_dict[t_name]['hub_height'] = float(self.txt_wind_turb_tbin_hub_height.text())
            temp_t_dict[t_name]['units'] = self.spbx_wind_turb_tbin_units.value()
            temp_t_dict[t_name]['blade_length'] = float(self.txt_wind_turb_tbin_blade_length.text())
            temp_t_dict[t_name]['no_blades'] = self.spbx_wind_turb_tbin_no_blades.value()

            return temp_t_dict
        except Exception as e:
            print(type(e), str(e))

    def analyze_wind_turbine(self):
        site_name = self.cmbx_wind_turb_site_name.currentText()
        t_name = self.cmbx_wind_turb_tbin_name.currentText()

        site_data = self.read_wind_turb_site_data()
        t_data = self.read_wind_turb_tbin_data()

        self.saved_data['wind_turbine'] = {
            'site_data': {'name': site_name, 'data': site_data[site_name]},
            'turbine': {'name': t_name, 'data': t_data[t_name]}
        }

        if not site_data or not t_data:
            return

        w_t = WindTurbine(site_data=site_data[site_name], t_data=t_data[t_name])
        data = w_t.analyse()

        self.lbl_wind_turb_output_pow.setText(str(round(data['power'], 2)))
        self.lbl_wind_turb_output_eff.setText(str(round(data['efficiency'], 2)))
        self.stk_wind_turb_main.setCurrentIndex(1)
        self.energy_sources['wind_turbine'] = data
        return True

    def optimize_wind_turbine(self):
        site_name = self.cmbx_wind_turb_site_name.currentText()
        t_name = self.cmbx_wind_turb_tbin_name.currentText()

        site_data = self.read_wind_turb_site_data()
        t_data = self.read_wind_turb_tbin_data()

        self.saved_data['wind_turbine'] = {
            'site_data': {'name': site_name, 'data': site_data[site_name]},
            'turbine': {'name': t_name, 'data': t_data[t_name]}
        }

        if not site_data or not t_data:
            return

        w_t = WindTurbine(site_data=site_data[site_name], t_data=t_data[t_name])
        data = w_t.analyse()

        self.lbl_wind_turb_output_pow.setText(str(round(data['power'], 2)))
        self.lbl_wind_turb_output_eff.setText(str(round(data['efficiency'], 2)))
        self.stk_wind_turb_main.setCurrentIndex(1)
        self.energy_sources['wind_turbine'] = data
        return True

    def final_report_open(self):
        try:
            total_app_pow = 0
            for room in self.rooms:
                for appliance in self.rooms[room]['appliances']:
                    total_app_pow += (self.rooms[room]['appliances'][appliance]['power_rating'] *
                                      self.rooms[room]['appliances'][appliance]['units'] *
                                      self.rooms[room]['appliances'][appliance]['operating_hours'])

            self.lbl_solar_pv_pow.setText(str(round(self.energy_sources['solar_pv']['actual power'], 2)))
            self.lbl_wind_turb_pow.setText(str(round(self.energy_sources['wind_turbine']['power'], 2)))

            pow_solar = self.energy_sources['solar_pv']['actual power'] if self.gb_final_solar_pv.isChecked() else 0
            pow_wind = self.energy_sources['wind_turbine']['power'] if self.gb_final_wind_turb.isChecked() else 0

            total_energy_demand = total_app_pow

            total_energy_available = pow_solar + pow_wind

            pow_solar_per = round((pow_solar / total_energy_available) * 100, 1)
            pow_wind_per = round((pow_wind / total_energy_available) * 100, 1)

            print('Appliance Power', total_app_pow)
            print('Power Demanded', total_energy_demand)
            print('Power Available', total_energy_available)
            print('Power Solar PV', pow_solar)
            print('Power Wind Turbine', pow_wind)
            print('Power Composition Solar PV', pow_solar_per)
            print('Power Composition Wind Turbine', pow_wind_per)

            self.lbl_final_pow_consumed.setText(str(round(total_energy_demand, 2)))
            self.lbl_final_pow_available.setText(str(round(total_energy_available, 2)))

            self.lbl_final_solar_pv_comp_kw.setText(str(round(pow_solar, 2)) + 'W')
            self.lbl_final_solar_pv_comp_per.setText(str(round(pow_solar_per, 2)) + '%')

            self.lbl_final_wind_turb_comp_kw.setText(str(round(pow_wind, 2)) + 'W')
            self.lbl_final_wind_turb_comp_per.setText(str(round(pow_wind_per, 2)) + '%')

            if total_energy_demand > total_energy_available:
                self.lbl_final_pow_trend.setPixmap(QtGui.QPixmap(":/icons/icons/low.png"))
            else:
                self.lbl_final_pow_trend.setPixmap(QtGui.QPixmap(":/icons/icons/high.png"))

            self.plot_final_audit_barchart(total_energy_available, total_energy_demand)

            self.plot_donught_chart(['Wind', 'Solar'], [pow_wind, pow_solar])

            self.next_page()
        except Exception as e:
            print('Error', type(e), str(e))

    def plot_final_audit_barchart(self, power_available, power_required):
        try:
            self.final_audit_figure_ax.clear()
            self.final_audit_figure.subplots_adjust(left=0, wspace=0.2, hspace=0.3)
            self.final_audit_figure.patch.set_facecolor('#f0f0f0')
            self.final_audit_figure_ax.patch.set_facecolor('#f0f0f0')
            self.final_audit_figure.set_alpha(0.0)
            self.final_audit_figure_ax.set_alpha(0.0)

            color = '#097703'
            if power_required > power_available:
                color = '#840202'
            self.final_audit_figure_ax.barh('Power Available', power_available, 0.5, color=color)

            self.final_audit_figure_ax.barh('Power Required', power_required, 0.5, color='#097703')
            self.final_audit_figure.canvas.draw()

            self.final_audit_figure.canvas.draw()

            self.final_audit_figure_ax.xaxis.set_visible(False)
            self.final_audit_figure_ax.yaxis.set_visible(True)

            self.final_audit_figure_ax.spines['top'].set_visible(False)
            self.final_audit_figure_ax.spines['bottom'].set_visible(False)
            self.final_audit_figure_ax.spines['right'].set_visible(False)
            self.final_audit_figure_ax.spines['left'].set_linewidth(1)

        except Exception as e:
            print(type(e), str(e))

    def plot_donught_chart(self, labels, sizes):
        try:
            self.composition_figure_ax.clear()

            colors = ['#097703', '#095403', '#090003']
            self.composition_figure_ax.pie(sizes, startangle=90, colors=colors)
            self.composition_figure_ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            self.composition_figure.canvas.draw()

            self.final_audit_figure.subplots_adjust(left=0, bottom=0)
            self.final_audit_figure_ax.patch.set_facecolor('#f0f0f0')
            self.final_audit_figure_ax.patch.set_facecolor('#f0f0f0')
            self.final_audit_figure_ax.set_alpha(0.0)
            self.final_audit_figure_ax.set_alpha(0.0)
        except Exception as e:
            print(type(e), str(e))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, {'rooms': {}, 'retrofit': {}})
    MainWindow.showMaximized()
    app.setWindowIcon(QtGui.QIcon("icons/renewable-energy.png"))
    sys.exit(app.exec_())
