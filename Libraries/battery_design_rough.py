# the system module
import sys

# Battery Design
from math import cos, pi, ceil

import resource

# from third party
import numpy as np
from scipy.integrate import quad

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QGroupBox, QGridLayout, QPushButton,
    QLabel, QComboBox, QDoubleSpinBox, QLineEdit
)

from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt, QSize

import matplotlib.pylab as plt
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
import matplotlib

matplotlib.use('QT5Agg')

# m_v = total vehicle mass (kg)
# a_v = vehicle acceleration (m / s2)
# g = gravitational acceleration
# ∝_s = road slope angle
# c_rr = road rolling resistance coefficient
# c_d = air drag coefficient
# rho = air density (kg / m3)
# A = vehicle frontal area (m2)
# v_v = vehicle speed (m / s)
# T_d = total length of drive cycle (km)

v_n = 'T-ride'
m_v = 1908
a_v = 10
g = 9.81
alpha_s = 0
c_rr = .011
c_d = .36
rho = 1.202
A = 2.42
v_v = 55.5

total_length_of_drive_cycle = 23.266
auxilliary_energy = 9.241
efficiency_of_the_powertrain = 0.9
vehicle_drive_range = 250

# battery params
battery_cost = [2500, 1990, 1500, 2115, 1980, 3750]
length_of_battery_options = len(battery_cost)
battery_cell_capacity = [3.2, 2.6, 20, 15.6, 2.5, 19.5]
battery_cell_mass = [.0485, 0.05, 0.51, 0.317, 0.076, 0.496]
battery_cell_voltage = [3.6, 3.7, 2.3, 3.6, 3.3, 3.3]
battery_nominal_voltage = [400] * length_of_battery_options
battery_cell_volume = [0.00002, 0.00002, 0.00026, 0.00016, 0.00003, 0.00025]
battery_cell_continous_rate = [1, 1, 1, 2, 10, 1]
battery_cell_peak_rate = [1, 2, 1, 3, 24, 10]
battery_types = ["Panasonic", "Molicel", "Toshiba", "Kokam", "A123-Sys", "A121-Sys"]


class BatteryDesign(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.title = 'EnergyHx 3.0 - Battery Analysis'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480

        self.parent = parent
        self.initUI()

        # save the data
        self.data = {
            'm_v': m_v, 'a_v': a_v, 'alpha_s': alpha_s, 'c_rr': c_rr, 'c_d': c_d,
            'rho': rho, 'A': A, 'v_v': v_v
        }

        # self.setWindowModality(Qt.ApplicationModal)

    def closeEvent(self, event):
        self.parent.focus_on_main_window = True
        self.hide()
        event.ignore()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createGridLayout()
        self.createGridLayout2()
        self.createGridLayout3()
        windowLayout = QGridLayout()
        windowLayout.setColumnStretch(1, 4)
        windowLayout.setColumnStretch(2, 4)
        windowLayout.addWidget(self.horizontalGroupBox)
        windowLayout.addWidget(self.horizontalGroupBox2)
        windowLayout.addWidget(self.horizontalGroupBox3)

        self.setLayout(windowLayout)

    def optimize(self):
        m_v, a_v, alpha_s, c_rr, c_d, rho, A, v_v = [
            self.data[key] for key in 'm_v, a_v, alpha_s, c_rr, c_d, rho, A, v_v'.split(', ')
        ]

        print(self.data)
        d1, d2, message = getMinimum(m_v, a_v, alpha_s, c_rr, c_d, rho, A, v_v)

        # create axis
        ax = self.figure.add_subplot(211)

        # clear old graph
        ax.clear()

        ax.set_title('Graph of Battery Pack Cost against Battery Types')
        ax.set_ylabel('Battery Pack Cost')
        ax.bar(battery_types, d1)

        ax = self.figure.add_subplot(212)

        # clear old graph
        ax.clear()

        ax.set_title('Graph of Battery Pack Energy against Battery Types')
        ax.set_ylabel('Battery Pack Energy')
        ax.bar(battery_types, d2)

        # space the graphs
        self.figure.subplots_adjust(hspace=.5)

        # refresh canvas
        self.plotWidget.draw()

        # optimization report
        self.label_opt_result.setText(message)

    def createGridLayout(self):
        self.horizontalGroupBox = QGroupBox("Vehicle Paramters")
        layout = QGridLayout()
        layout.setColumnStretch(1, 4)
        layout.setColumnStretch(2, 4)

        font = QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)

        self.label = QLabel()
        self.label.setMaximumSize(QSize(50, 50))
        self.label.setScaledContents(True)
        self.label.setPixmap(QPixmap(":icons/icons/renewable-energy.png"))
        layout.addWidget(self.label, 0, 0)
        label = QLabel("Electric Vehicle")
        label.setFont(font)
        layout.addWidget(label, 0, 1)

        self.vnlabel = QLineEdit(self)
        self.vnlabel.setText(v_n)
        layout.addWidget(QLabel("Vehicle Name:"), 1, 0)
        layout.addWidget(self.vnlabel, 1, 1)
        self.vnlabel.textEdited.connect(
            lambda text: self.data.update({'v_n': text})
        )

        numEntry = QDoubleSpinBox(self)
        numEntry.setMaximum(10000)
        numEntry.setValue(m_v)
        layout.addWidget(QLabel("Vehicle Mass (kg):"), 2, 0)
        layout.addWidget(numEntry, 2, 1)
        numEntry.valueChanged.connect(
            lambda text: self.data.update({'m_v': text})
        )

        numEntry = QDoubleSpinBox(self)
        numEntry.setMaximum(10000)
        numEntry.setValue(a_v)
        layout.addWidget(QLabel("vehicle Acceleration (m/s2):"), 3, 0)
        layout.addWidget(numEntry, 3, 1)
        numEntry.valueChanged.connect(
            lambda text: self.data.update({'a_v': text})
        )

        numEntry = QDoubleSpinBox(self)
        numEntry.setMaximum(10000)
        numEntry.setValue(alpha_s)
        layout.addWidget(QLabel("Road slope angle:"), 4, 0)
        layout.addWidget(numEntry, 4, 1)
        numEntry.valueChanged.connect(
            lambda text: self.data.update({'alpha_s': text})
        )

        numEntry = QDoubleSpinBox(self)
        numEntry.setMaximum(10000)
        numEntry.setValue(c_rr)
        layout.addWidget(
            QLabel("Road rolling resistance coefficient:"), 5, 0)
        layout.addWidget(numEntry, 5, 1)
        numEntry.valueChanged.connect(
            lambda text: self.data.update({'c_rr': text})
        )

        numEntry = QDoubleSpinBox(self)
        numEntry.setMaximum(10000)
        numEntry.setValue(c_d)
        layout.addWidget(QLabel("Air drag coefficient:"), 6, 0)
        layout.addWidget(numEntry, 6, 1)
        numEntry.valueChanged.connect(
            lambda text: self.data.update({'c_d': text})
        )

        numEntry = QDoubleSpinBox(self)
        numEntry.setMaximum(10000)
        numEntry.setValue(rho)
        layout.addWidget(QLabel("Air density (kg / m3):"), 7, 0)
        layout.addWidget(numEntry, 7, 1)
        numEntry.valueChanged.connect(
            lambda text: self.data.update({'rho': text})
        )

        numEntry = QDoubleSpinBox(self)
        numEntry.setMaximum(10000)
        numEntry.setValue(A)
        layout.addWidget(QLabel("vehicle frontal area (m2):"), 8, 0)
        layout.addWidget(numEntry, 8, 1)
        numEntry.valueChanged.connect(
            lambda text: self.data.update({'A': text})
        )

        numEntry = QDoubleSpinBox(self)
        numEntry.setMaximum(10000)
        numEntry.setValue(v_v)
        layout.addWidget(QLabel("Vehicle Speed (m/s):"), 9, 0)
        layout.addWidget(numEntry, 9, 1)
        numEntry.valueChanged.connect(
            lambda text: self.data.update({'v_v': text})
        )

        numEntry = QDoubleSpinBox(self)
        numEntry.setMaximum(10000)
        numEntry.setValue(total_length_of_drive_cycle)
        layout.addWidget(QLabel("Total length of drive cycle:"), 10, 0)
        layout.addWidget(numEntry, 10, 1)
        numEntry.valueChanged.connect(
            lambda text: self.data.update(
                {'total_length_of_drive_cycle': text})
        )

        numEntry = QDoubleSpinBox(self)
        numEntry.setMaximum(10000)
        numEntry.setValue(auxilliary_energy)
        layout.addWidget(QLabel("Auxilliary Energy:"), 11, 0)
        layout.addWidget(numEntry, 11, 1)
        numEntry.valueChanged.connect(
            lambda text: self.data.update(
                {'auxilliary_energy': text})
        )

        numEntry = QDoubleSpinBox(self)
        numEntry.setMaximum(10000)
        numEntry.setValue(efficiency_of_the_powertrain)
        layout.addWidget(QLabel("Efficiency of the powertrain:"), 12, 0)
        layout.addWidget(numEntry, 12, 1)
        numEntry.valueChanged.connect(
            lambda text: self.data.update(
                {'efficiency_of_the_powertrain': text})
        )

        numEntry = QDoubleSpinBox(self)
        numEntry.setMaximum(10000)
        numEntry.setValue(vehicle_drive_range)
        layout.addWidget(QLabel("Vehicle Drive Range:"), 13, 0)
        layout.addWidget(numEntry, 13, 1)
        numEntry.valueChanged.connect(
            lambda text: self.data.update(
                {'vehicle_drive_range': text})
        )

        self.horizontalGroupBox.setLayout(layout)

    def batterySelected(self, index):
        self.data.update({'index': index})

        self.numEntry_bcp.setValue(battery_cell_capacity[index])
        self.numEntry_bcv.setValue(battery_cell_voltage[index])
        self.numEntry_bcm.setValue(battery_cell_mass[index])
        self.numEntry_bcr.setValue(battery_cell_continous_rate[index])
        self.numEntry_bvv.setValue(battery_cell_volume[index])
        self.numEntry_bpr.setValue(battery_cell_peak_rate[index])

    def createGridLayout2(self):
        self.horizontalGroupBox2 = QGroupBox("Battery Parameters")
        layout = QGridLayout()
        layout.setColumnStretch(1, 4)
        layout.setColumnStretch(2, 4)

        font = QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)

        self.label = QLabel()
        self.label.setMaximumSize(QSize(50, 50))
        self.label.setScaledContents(True)
        self.label.setPixmap(QPixmap(":icons/icons/washing-machine (1).png"))
        layout.addWidget(self.label, 0, 0)
        label = QLabel("Battery")
        label.setFont(font)
        layout.addWidget(label, 0, 1)

        self.options = QComboBox()
        self.options.addItems(battery_types)
        layout.addWidget(QLabel("Options:"), 1, 0)
        layout.addWidget(self.options, 1, 1)
        self.options.currentIndexChanged.connect(self.batterySelected)

        index = 0

        self.numEntry_bcp = QDoubleSpinBox()
        self.numEntry_bcp.setValue(battery_cell_capacity[index])
        layout.addWidget(QLabel("Battery Cell Capacity:"), 2, 0)
        layout.addWidget(self.numEntry_bcp, 2, 1)
        self.numEntry_bcp.valueChanged.connect(
            lambda text: self.data.update(
                {'battery_cell_capacity': text})
        )

        self.numEntry_bcv = QDoubleSpinBox(self)
        self.numEntry_bcv.setValue(battery_cell_voltage[index])
        layout.addWidget(QLabel("Battery Cell Voltage:"), 3, 0)
        layout.addWidget(self.numEntry_bcv, 3, 1)
        self.numEntry_bcv.valueChanged.connect(
            lambda text: self.data.update(
                {'Battery_cell_voltage': text})
        )

        self.numEntry_bcm = QDoubleSpinBox(self)
        self.numEntry_bcm.setValue(battery_cell_mass[index])
        layout.addWidget(QLabel("Battery Cell Mass:"), 4, 0)
        layout.addWidget(self.numEntry_bcm, 4, 1)
        self.numEntry_bcm.valueChanged.connect(
            lambda text: self.data.update(
                {'Battery_cell_mass': text})
        )

        self.numEntry_bvv = QDoubleSpinBox(self)
        self.numEntry_bvv.setValue(battery_cell_volume[index])
        layout.addWidget(QLabel("Battery Cell Volume:"), 5, 0)
        layout.addWidget(self.numEntry_bvv, 5, 1)
        self.numEntry_bvv.valueChanged.connect(
            lambda text: self.data.update(
                {'Battery_cell_volume': text})
        )

        self.numEntry_bcr = QDoubleSpinBox(self)
        self.numEntry_bcr.setValue(battery_cell_continous_rate[index])
        layout.addWidget(QLabel("Battery Cell Continous rate:"), 6, 0)
        layout.addWidget(self.numEntry_bcr, 6, 1)
        self.numEntry_bcr.valueChanged.connect(
            lambda text: self.data.update(
                {'Battery_cell_continous_rate': text})
        )

        self.numEntry_bpr = QDoubleSpinBox(self)
        self.numEntry_bpr.setValue(battery_cell_peak_rate[index])
        layout.addWidget(QLabel("Battery Cell Peak rate:"), 7, 0)
        layout.addWidget(self.numEntry_bpr, 7, 1)
        self.numEntry_bpr.valueChanged.connect(
            lambda text: self.data.update(
                {'Battery_cell_peak_rate': text})
        )

        btn = QPushButton("Analyse")
        layout.addWidget(btn, 8, 1)
        btn.clicked.connect(self.analyse)
        self.horizontalGroupBox2.setLayout(layout)

    def createGridLayout3(self):
        self.horizontalGroupBox3 = QGroupBox("Results")

        layout = QGridLayout()
        # layout.setColumnStretch(1, 4)
        # layout.setColumnStretch(2, 4)

        font = QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)

        self.label = QLabel()
        self.label.setMaximumSize(QSize(50, 50))
        self.label.setScaledContents(True)
        self.label.setPixmap(QPixmap(":icons/icons/report.png"))
        layout.addWidget(self.label, 0, 1)
        # label = QLabel("Results")
        self.horizontalGroupBox3.setFont(font)
        # layout.addWidget(label, 0, 1)

        self.label_ec = QLabel("Energy Consumed by Vehicle")
        layout.addWidget(self.label_ec, 1, 1)

        self.label_bpe = QLabel("Battery Pack Energy")
        layout.addWidget(self.label_bpe, 2, 1)

        self.label_tnc = QLabel("Battery Pack Energy")
        layout.addWidget(self.label_tnc, 3, 1)

        self.label_mbp = QLabel("Battery Pack Energy")
        layout.addWidget(self.label_mbp, 4, 1)

        btn = QPushButton("Optimize")
        btn.setMinimumSize(QSize(200, 45))
        btn.setMaximumSize(QSize(200, 16777215))
        icon1 = QIcon()
        icon1.addPixmap(QPixmap(":/icons/icons/analyze.png"), QIcon.Normal, QIcon.Off)
        btn.setIcon(icon1)
        btn.setIconSize(QSize(30, 30))
        btn.setAutoDefault(False)
        btn.setDefault(True)
        btn.setFlat(False)
        layout.addWidget(btn, 5, 1, 1, 1, Qt.AlignRight)
        btn.clicked.connect(self.optimize)

        self.figure = Figure()

        # plot
        self.plotWidget = FigureCanvas(self.figure)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.plotWidget, 6, 1)

        self.label_opt_result = QLabel("Optimum Battery Option")
        layout.addWidget(self.label_opt_result, 7, 1)

        self.horizontalGroupBox3.setLayout(layout)

    def analyse(self):
        index = self.options.currentIndex()
        energy_cons, batt_pack_energy, tot_num_of_cells, mass_of_batt_pack = solve(
            index)

        self.label_ec.setText('Energy Consumed = {:.4f}'.format(energy_cons))
        self.label_bpe.setText(
            'Battery Pack energy = {:.4f}'.format(batt_pack_energy))
        self.label_tnc.setText(
            'Total Number of cells = {:.4f}'.format(tot_num_of_cells))
        self.label_mbp.setText(
            'Mass of Battery Pack = {:.4f}'.format(mass_of_batt_pack))


def total_energy_consumed_integrand(t, m_v, a_v, alpha_s, c_rr, c_d, rho, A, v_v):
    # converts degrees to rad
    def degree_to_radian(deg): return deg * pi / 180

    return (m_v * a_v) + (m_v * g * (alpha_s)) + (m_v * g * cos(degree_to_radian(alpha_s)) * c_rr) + (
                0.5 * c_d * rho * A * v_v ** 2)


total_energy_consumed = quad(total_energy_consumed_integrand, 0, 10, args=(
    m_v, a_v, alpha_s, c_rr, c_d, rho, A, v_v))[0]

# battery pack energy
battery_pack_energy = [
    ((total_energy_consumed / total_length_of_drive_cycle) + auxilliary_energy) *
    (2 - efficiency_of_the_powertrain) * vehicle_drive_range * (battery_cell_capacity[i]) *
    (battery_cell_voltage[i]) for i in range(length_of_battery_options)
]

# total number of cells in battery pack
total_number_of_cells_in_battery_pack = [
    battery_pack_energy[i] / (battery_cell_capacity[i] * battery_cell_voltage[i]) for i in
    range(length_of_battery_options)
]

total_battery_cost = [
    total_number_of_cells_in_battery_pack[i] * battery_cost[i] for i in range(length_of_battery_options)
]


def solve(optimal_index):
    # battery pack mass
    m_bp = battery_pack_energy[optimal_index] / (
                battery_cell_capacity[optimal_index] * battery_cell_voltage[optimal_index]) * battery_cell_mass[
               optimal_index]

    # battery pack capacity
    C_bp = (total_number_of_cells_in_battery_pack[optimal_index] *
            battery_cell_voltage[optimal_index] * battery_cell_capacity[optimal_index]) / \
           battery_nominal_voltage[optimal_index]

    # volume of battery cell
    volume_of_battery_pack = total_number_of_cells_in_battery_pack[optimal_index] * \
                             battery_cell_volume[optimal_index]

    return (
        total_energy_consumed,
        battery_pack_energy[optimal_index],
        total_number_of_cells_in_battery_pack[optimal_index],
        m_bp
    )


def getMinimum(m_v, a_v, alpha_s, c_rr, c_d, rho, A, v_v):
    # find the min cost
    minimum_battery_cost = optimal_index = None
    for i in range(length_of_battery_options):
        if total_energy_consumed > battery_pack_energy[i]:
            continue

        if minimum_battery_cost is None:
            minimum_battery_cost = total_battery_cost[i]
            optimal_index = i

        elif minimum_battery_cost > total_battery_cost[i]:
            minimum_battery_cost = total_battery_cost[i]
            optimal_index = i

    if optimal_index is not None:
        # battery pack mass
        energy_cons, batt_pack_energy, tot_num_of_cells, mass_of_batt_pack = solve(optimal_index)

        message = 'optimal type is {}: cost = {:,.4f}, energy = {:,.4f} Joules'.format(
            battery_types[optimal_index], minimum_battery_cost, batt_pack_energy
        )

        print(message)
        print(total_battery_cost)
        print(battery_pack_energy)

        return total_battery_cost, battery_pack_energy, message

    else:
        message = 'No suitable choice found!'
        print(message)
        return [], [], message


def get_site_data(m_v, a_v, alpha_s, c_rr, c_d, rho, A, v_v):
    data_dict = dict()
    # create a dictionary to hold the values needed for analyze function
    data_dict['m_v'] = m_v
    data_dict['a_v'] = a_v
    data_dict['alpha_s'] = alpha_s
    data_dict['c_rr'] = c_rr
    data_dict['c_d'] = c_d
    data_dict['rho'] = rho
    data_dict['A'] = A
    data_dict['v_v'] = v_v
    return data_dict

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = BatteryDesign()
    get_site_data(12, 8, 15, 3, 6, 7, 11, 1)
    ex.show()
    # ex.showMaximized()
    sys.exit(app.exec_())
