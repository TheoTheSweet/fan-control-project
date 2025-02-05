import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
import pyqtgraph as pg


class UI(QWidget):
    def __init__(self, backend):
        super().__init__()
        self.backend = backend
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Fan Control System')
        layout = QVBoxLayout()

        # Labels for fan speeds and temperatures
        self.fan_speed_label = QLabel('Fan Speeds:')
        layout.addWidget(self.fan_speed_label)
        self.temp_label = QLabel('Subsystem Temperatures:')
        layout.addWidget(self.temp_label)

        # Graphs for fan speed and temperature
        self.temp_graph = pg.PlotWidget(title="Temperature Graph")
        self.fan_speed_graph = pg.PlotWidget(title="Fan Speed Graph")
        layout.addWidget(self.temp_graph)
        layout.addWidget(self.fan_speed_graph)

        # Button to export CSV
        self.export_button = QPushButton('Export CSV')
        self.export_button.clicked.connect(self.export_csv)
        layout.addWidget(self.export_button)

        self.setLayout(layout)
        self.show()

    def update_ui(self):
        fan_speeds, temperatures = self.backend.get_data_for_ui()
        self.fan_speed_label.setText(f"Fan Speeds: {fan_speeds}")
        self.temp_label.setText(f"Subsystem Temperatures: {temperatures}")

        # Update graphs
        self.temp_graph.plot(temperatures)
        self.fan_speed_graph.plot(fan_speeds)

    def export_csv(self):
        self.backend.request_csv()
