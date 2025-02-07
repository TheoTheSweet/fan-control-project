from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSpinBox, QTableWidget,
    QTableWidgetItem, QHeaderView, QScrollArea
)
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


# This class is used to create a widget that displays a log plot of a specific data series.
class LogPlotWidget(QWidget):
    def __init__(self, log_data, index, y_min, y_max, y_label, parent=None):
        super().__init__(parent)
        self.log_data = log_data
        self.index = index
        self.y_min = y_min
        self.y_max = y_max
        self.y_label = y_label

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.update_plot()

    # This method updates the log data that the plot is based on.
    def update_log_data(self, log_data):
        self.log_data = log_data

    # This method updates the plot with the latest data from the log.
    def update_plot(self):
        self.ax.clear()

        # Extract time and data values from the log
        times = [log[0] for log in self.log_data]
        values = [log[1][self.index] for log in self.log_data]

        # Set the x-axis range
        if times:
            x_min = times[0] - 5
            x_max = times[-1] + 5
            self.ax.set_xlim(x_min, x_max)

        # Set the y-axis range
        self.ax.set_ylim(self.y_min, self.y_max)

        # Plot the data
        self.ax.plot(times, values)
        self.ax.set_xlabel("Elapsed Time (s)")
        self.ax.set_ylabel(self.y_label)

        # Redraw the canvas
        self.canvas.draw()


# This is the main UI class that controls the application's user interface.
class UI(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.backend = main_app.backend
        self.init_ui()

    # This method initializes the UI with the main menu layout.
    def init_ui(self):
        self.setWindowTitle('Robotic Subsystem Fan Control and Data Log')

        # Clear the existing layout
        old_layout = self.layout()
        if old_layout is not None:
            QWidget().setLayout(old_layout)  # Detach the old layout from the widget

        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                color: #333333;
            }
            QPushButton {
                background-color: #8B7355;
                color: white;
                border-radius: 10px;
                padding: 5px;
            }
            QTableWidget {
                background-color: white;
                border-radius: 10px;
            }
        """)
        layout = QVBoxLayout()

        # Title and description
        title = QLabel('Robotic Subsystem Fan Control and Data Log')
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

        description = QLabel('This application simulates fan control for the cooling of robotic subsystems. You can '
                             'set the number of fans and subsystems, along with the maximum RPM for each fan. The '
                             'application will track the temperature and fan speed data over time. Press "Load '
                             'Configuration" after setting the parameters.')
        description.setStyleSheet("font-size: 14px;")
        layout.addWidget(description, alignment=Qt.AlignmentFlag.AlignCenter)

        # Input fields for number of fans and subsystems
        input_layout = QHBoxLayout()

        self.fan_spinbox = QSpinBox()
        self.fan_spinbox.setRange(1, 20)
        self.fan_spinbox.setPrefix("# of fans: ")
        self.fan_spinbox.setStyleSheet("font-size: 14px;")
        self.fan_spinbox.valueChanged.connect(self.update_fan_list)
        input_layout.addWidget(self.fan_spinbox)

        self.subsystem_spinbox = QSpinBox()
        self.subsystem_spinbox.setRange(1, 20)
        self.subsystem_spinbox.setPrefix("# of subsystems: ")
        self.subsystem_spinbox.setStyleSheet("font-size: 14px;")
        input_layout.addWidget(self.subsystem_spinbox)

        layout.addLayout(input_layout)

        # Fan RPM input table
        self.fan_table = QTableWidget()
        self.fan_table.setColumnCount(2)
        self.fan_table.setHorizontalHeaderLabels(["Fan", "Max RPM"])
        self.fan_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.fan_table)
        layout.addWidget(scroll_area)

        # Buttons
        button_layout = QHBoxLayout()
        self.load_button = QPushButton('Load Configuration')
        self.load_button.setStyleSheet("background-color: #007bff; color: white; font-size: 14px;")
        self.load_button.clicked.connect(self.load_configuration)
        button_layout.addWidget(self.load_button)

        self.quit_button = QPushButton('Quit')
        self.quit_button.setStyleSheet("background-color: #dc3545; color: white; font-size: 14px;")
        self.quit_button.clicked.connect(self.quit_application)
        button_layout.addWidget(self.quit_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        # Initialize fan list with one fan
        self.update_fan_list()

    # This method updates the fan list based on the number of fans specified in the input field.
    def update_fan_list(self):
        num_fans = self.fan_spinbox.value()
        self.fan_table.setRowCount(num_fans)
        for i in range(num_fans):
            if self.fan_table.item(i, 0) is None:
                self.fan_table.setItem(i, 0, QTableWidgetItem(f"Fan {i + 1}"))
            if self.fan_table.cellWidget(i, 1) is None:
                rpm_spinbox = QSpinBox()
                rpm_spinbox.setRange(1, 10000)
                rpm_spinbox.setValue(2000)
                self.fan_table.setCellWidget(i, 1, rpm_spinbox)

    # This method loads the configuration specified in the input fields and initializes the application.
    def load_configuration(self):
        try:
            num_fans = self.fan_spinbox.value()
            num_subsystems = self.subsystem_spinbox.value()
            max_rpms = [int(self.fan_table.cellWidget(i, 1).text()) for i in range(num_fans)]
            print(f"Loading configuration: num_fans={num_fans}, num_subsystems={num_subsystems}, max_rpms={max_rpms}")
            self.main_app.initialize(num_fans, num_subsystems, max_rpms)
            self.backend = self.main_app.backend  # Update the backend reference
        except Exception as e:
            print(f"Error loading configuration: {e}")

    # This method quits the application.
    def quit_application(self):
        QApplication.quit()

    # This method sets up the UI for the data tracking state.
    def setup_data_tracking_ui(self):
        print("Setting up UI for data tracking")
        self.setWindowTitle('Temperature/Fan Speed Data')

        # Clear the existing layout
        old_layout = self.layout()
        if old_layout is not None:
            QWidget().setLayout(old_layout)  # Detach the old layout from the widget

        new_layout = QVBoxLayout()

        # Title
        title = QLabel('Temperature/Fan Speed Data')
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        new_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

        # Info labels
        info_layout = QHBoxLayout()
        self.num_fans_label = QLabel(f"# of fans: {self.backend.num_fans}")
        self.num_fans_label.setStyleSheet("font-size: 14px;")
        info_layout.addWidget(self.num_fans_label)

        self.num_subsystems_label = QLabel(f"# of subsystems: {self.backend.num_subsystems}")
        self.num_subsystems_label.setStyleSheet("font-size: 14px;")
        info_layout.addWidget(self.num_subsystems_label)

        self.elapsed_time_label = QLabel("Elapsed time: 00:00:00")
        self.elapsed_time_label.setStyleSheet("font-size: 14px;")
        info_layout.addWidget(self.elapsed_time_label)

        new_layout.addLayout(info_layout)

        # Data tables
        data_layout = QHBoxLayout()

        # Fan speed data
        fan_speed_layout = QVBoxLayout()
        fan_speed_title = QLabel("Fan Speed Data")
        fan_speed_title.setStyleSheet("font-size: 18px; font-weight: bold;")
        fan_speed_layout.addWidget(fan_speed_title)

        self.fan_speed_table = QTableWidget()
        self.fan_speed_table.setColumnCount(4)
        self.fan_speed_table.setHorizontalHeaderLabels(["Fan", "Max RPM", "Current RPM", "Graph"])
        self.fan_speed_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.fan_speed_table.horizontalHeader().resizeSection(0, self.fan_speed_table.columnWidth(0) + 20)  # Add buffer
        self.fan_speed_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)

        scroll_area_fan = QScrollArea()
        scroll_area_fan.setWidgetResizable(True)
        scroll_area_fan.setWidget(self.fan_speed_table)
        fan_speed_layout.addWidget(scroll_area_fan)

        data_layout.addLayout(fan_speed_layout)

        # put the fan speeds and graphs into the table
        self.fan_speed_table.setRowCount(self.backend.num_fans)
        for i in range(self.backend.num_fans):
            self.fan_speed_table.setItem(i, 0, QTableWidgetItem(f"Fan {i + 1}"))
            self.fan_speed_table.setItem(i, 1, QTableWidgetItem(str(self.backend.max_rpms[i])))
            self.fan_speed_table.setItem(i, 2, QTableWidgetItem("0.000"))
            log_plot_widget = LogPlotWidget(self.backend.speed_log, i, 0, self.backend.max_rpms[i], "Fan Speed (RPM)")
            self.fan_speed_table.setCellWidget(i, 3, log_plot_widget)
            self.fan_speed_table.setRowHeight(i, 400)  # Set row height to 400 pixels

        # Temperature data
        temp_layout = QVBoxLayout()
        temp_title = QLabel("Temperature Data")
        temp_title.setStyleSheet("font-size: 18px; font-weight: bold;")
        temp_layout.addWidget(temp_title)

        self.temp_table = QTableWidget()
        self.temp_table.setColumnCount(3)
        self.temp_table.setHorizontalHeaderLabels(["Subsystem", "Current Temp", "Graph"])
        self.temp_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.temp_table.horizontalHeader().resizeSection(0, self.temp_table.columnWidth(0) + 20)  # Add buffer
        self.temp_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)

        scroll_area_temp = QScrollArea()
        scroll_area_temp.setWidgetResizable(True)
        scroll_area_temp.setWidget(self.temp_table)
        temp_layout.addWidget(scroll_area_temp)

        data_layout.addLayout(temp_layout)

        # put the temperatures and graphs into the table
        self.temp_table.setRowCount(self.backend.num_subsystems)
        for i in range(self.backend.num_subsystems):
            self.temp_table.setItem(i, 0, QTableWidgetItem(f"Subsystem {i + 1}"))
            self.temp_table.setItem(i, 1, QTableWidgetItem("0.000"))
            log_plot_widget = LogPlotWidget(self.backend.temp_log, i, 25, 85, "Temperature (°C)")
            self.temp_table.setCellWidget(i, 2, log_plot_widget)
            self.temp_table.setRowHeight(i, 400)  # Set row height to 400 pixels

        new_layout.addLayout(data_layout)

        # Buttons
        button_layout = QHBoxLayout()
        self.export_button = QPushButton('Export to CSV')
        self.export_button.setStyleSheet("background-color: #007bff; color: white; font-size: 14px;")
        self.export_button.clicked.connect(self.export_csv)
        button_layout.addWidget(self.export_button)

        self.return_button = QPushButton('Return to Configuration')
        self.return_button.setStyleSheet("background-color: #28a745; color: white; font-size: 14px;")  # Green color
        self.return_button.clicked.connect(self.return_to_configuration)
        button_layout.addWidget(self.return_button)

        self.quit_button = QPushButton('Quit')
        self.quit_button.setStyleSheet("background-color: #dc3545; color: white; font-size: 14px;")
        self.quit_button.clicked.connect(self.quit_application)
        button_layout.addWidget(self.quit_button)

        new_layout.addLayout(button_layout)
        self.setLayout(new_layout)

    # This method returns the application to the configuration state.
    def return_to_configuration(self):
        self.main_app.change_state("menu")

    # This method exports the temperature and fan speed data to a CSV file.
    def export_csv(self):
        if self.backend:
            filename = self.backend.request_csv()
            print(f"CSV file created: {filename}")

    # This method updates the UI with the latest data from the backend.
    def update_ui(self):
        try:
            if self.backend is None:
                return

            # Update fan speed table
            fan_speeds = self.backend.fan_speeds
            for i in range(self.fan_speed_table.rowCount()):
                if i < len(fan_speeds):
                    self.fan_speed_table.setItem(i, 2, QTableWidgetItem(f"{fan_speeds[i]:.3f}"))
                    log_plot_widget = self.fan_speed_table.cellWidget(i, 3)
                    if log_plot_widget:
                        log_plot_widget.update_log_data(self.backend.speed_log)
                        log_plot_widget.update_plot()

            # Update temperature table
            temperatures = self.backend.subsystem_temperatures
            for i in range(self.temp_table.rowCount()):
                if i < len(temperatures):
                    self.temp_table.setItem(i, 1, QTableWidgetItem(f"{temperatures[i]:.3f}"))
                    log_plot_widget = self.temp_table.cellWidget(i, 2)
                    if log_plot_widget:
                        log_plot_widget.update_log_data(self.backend.temp_log)
                        log_plot_widget.update_plot()

            # Update elapsed time
            elapsed_time = self.main_app.get_elapsed_time()
            self.elapsed_time_label.setText(f"Elapsed time: {elapsed_time}")
        except Exception as e:
            print(f"Error updating UI: {e}")
